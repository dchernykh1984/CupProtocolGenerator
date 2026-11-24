"""The window, driven through its real handlers with the site and Google faked."""

from __future__ import annotations

import pytest
from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QApplication, QMessageBox

from app import config as settings
from app.config import Config, Source, StageConfig
from app.main_window import MainWindow
from app.site_api import SiteApiError
from tests.test_pipeline import JUMPS, FakeSite

SAVED = Config(
    token="cup",
    stages=[
        StageConfig("Sprint", Source.SITE),
        StageConfig("Jump", Source.SHEET, link=JUMPS, rule="place_higher_better"),
    ],
)


@pytest.fixture(scope="module")
def qt_app():
    return QApplication.instance() or QApplication([])


@pytest.fixture
def window(qt_app, tmp_path):
    site = FakeSite()
    path = tmp_path / "config.json"
    settings.save(SAVED, path)
    made = MainWindow(api_factory=lambda url: site, config_path=path)
    made.site = site  # type: ignore[attr-defined]
    yield made
    made.deleteLater()


def _titles(window) -> list[str]:
    return [window.stages.tabText(i) for i in range(window.stages.count())]


def test_the_saved_settings_fill_the_window(window):
    assert window.config() == SAVED
    assert [window.tabs.tabText(i) for i in range(window.tabs.count())] == [
        "Cup",
        "Stages",
        "Log",
    ]
    assert _titles(window) == ["Sprint", "Jump"]
    assert window.token.echoMode() == window.token.EchoMode.Password


def test_a_stage_shows_the_fields_of_its_source(window):
    sprint, jump = window.stage_tabs()
    assert sprint.form.isRowVisible(sprint.section)
    assert sprint.form.isRowVisible(sprint.leader_laps_only)
    assert not sprint.form.isRowVisible(sprint.link)
    assert jump.form.isRowVisible(jump.link)
    assert not jump.form.isRowVisible(jump.token)
    assert not jump.form.isRowVisible(jump.leader_laps_only)
    sprint.source.setCurrentIndex(sprint.source.findData(Source.SHEET.value))
    assert sprint.form.isRowVisible(sprint.link)


def test_a_new_stage_is_a_copy_of_the_current_one_to_its_left_or_right(window):
    window.stages.setCurrentIndex(0)
    window.add_right.click()
    window.stages.setCurrentIndex(0)
    window.add_left.click()
    assert _titles(window) == ["Sprint", "Sprint", "Sprint", "Jump"]
    assert window.config().stages[0] == SAVED.stages[0]


def test_a_stage_is_deleted_but_never_the_last_one(window):
    window.stages.setCurrentIndex(0)
    sprint = window.stage_tabs()[0]
    destroyed: list[bool] = []
    sprint.destroyed.connect(lambda: destroyed.append(True))
    window.delete_stage.click()
    QApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
    assert destroyed == [True]  # freed, not only taken off the screen
    assert _titles(window) == ["Jump"]
    window.delete_stage.click()
    assert _titles(window) == ["Jump"]
    assert window.log.toPlainText() == "A cup needs at least one stage."
    assert window.status.text() == "A cup needs at least one stage."


def test_renaming_a_stage_renames_its_tab(window):
    jump = window.stage_tabs()[1]
    jump.name.setText("Standing jump")
    assert _titles(window)[1] == "Standing jump"
    jump.name.setText("")
    assert _titles(window)[1] == "Stage 2"


def test_an_unnamed_stage_is_titled_by_its_place_as_the_protocol_names_it(window):
    window.apply(Config(token="cup", stages=[StageConfig("Sprint"), StageConfig()]))
    assert _titles(window) == ["Sprint", "Stage 2"]
    window.stages.setCurrentIndex(0)
    window.add_left.click()  # a copy of Sprint goes first: the unnamed one is third now
    assert _titles(window) == ["Sprint", "Sprint", "Stage 3"]
    window.stages.setCurrentIndex(0)
    window.delete_stage.click()
    assert _titles(window) == ["Sprint", "Stage 2"]


def test_a_rule_this_build_does_not_know_falls_back_to_the_first(window):
    window.apply(Config(rule="best_three", stages=[StageConfig(rule="laps")]))
    assert window.config().rule == "sum_smallest_wins"
    assert window.config().stages[0].rule == "place_lower_better"


def test_a_build_shows_its_report_and_lets_the_protocol_be_published(window):
    window.on_build()
    text = window.log.toPlainText()
    assert "Jump: bibs no protocol names: 99" in text
    assert "Built: 2 table(s)" in text
    # The log keeps every line; the Cup tab says how it went and where to look.
    assert window.status.text() == "Built: 2 table(s), 2 error(s): see the Log tab"
    assert window.publish_button.isEnabled()
    assert QApplication.overrideCursor() is None  # the wait cursor is gone again
    assert settings.load(window._config_path) == SAVED  # saved on build


def test_the_status_line_shows_a_message_as_it_is_written(window):
    window.on_build()  # a status line in use, after a build
    # A quoted "<" never becomes markup: a link or the site's reason is shown as it is.
    assert window.status.textFormat() == Qt.TextFormat.PlainText


def test_a_build_without_errors_says_only_what_it_built(window):
    window.apply(Config(token="cup", stages=[StageConfig("Sprint")]))
    window.on_build()
    assert window.status.text() == "Built: 2 table(s)"
    assert window.log.toPlainText() == "Sprint: 3 results\nBuilt: 2 table(s)"


def test_a_changed_setting_asks_for_a_new_build_before_publishing(window):
    window.on_build()
    window.stage_tabs()[0].section.setValue(3)
    assert not window.publish_button.isEnabled()
    window.on_publish()  # nothing built: nothing sent
    assert window.site.uploads == []


def test_placing_everybody_is_kept_and_asks_for_a_new_build(window):
    window.on_build()
    window.place_everybody.setChecked(True)
    assert not window.publish_button.isEnabled()
    window.on_build()
    boys = window._built.document["sections"][0]["rows"]
    assert [row["cells"]["place"] for row in boys] == ["1", "1", "3"]
    assert settings.load(window._config_path).place_everybody
    window.place_everybody.setChecked(False)
    window.apply(Config(place_everybody=True))
    assert window.place_everybody.isChecked()  # a saved broadcast comes back


def test_the_laps_rule_is_kept_per_stage_and_asks_for_a_new_build(window):
    window.on_build()
    sprint = window.stage_tabs()[0]
    assert sprint.leader_laps_only.isChecked()
    sprint.leader_laps_only.setChecked(False)  # a Number of Tries race
    assert not window.publish_button.isEnabled()
    window.on_build()
    assert settings.load(window._config_path).stages[0].leader_laps_only is False
    window.apply(Config(stages=[StageConfig(leader_laps_only=False)]))
    assert not window.stage_tabs()[0].leader_laps_only.isChecked()  # it comes back


def test_a_build_that_fails_says_why_and_publishes_nothing(window):
    window.token.setText("")
    window.on_build()
    assert window.log.toPlainText() == "Not built: Enter the cup event's upload token"
    assert window.status.text() == "Not built: Enter the cup event's upload token"
    assert QApplication.overrideCursor() is None
    assert not window.publish_button.isEnabled()


def test_a_build_that_fails_after_one_that_worked_leaves_nothing_to_publish(window):
    window.on_build()
    assert window.publish_button.isEnabled()
    window.site.document = {}  # the stage protocol lost its data
    window.on_build()
    assert window.status.text().startswith("Not built: Sprint: protocol 4 has no data")
    assert not window.publish_button.isEnabled()
    window.on_publish()  # a click that slipped through sends nothing
    assert window.site.uploads == []


def test_an_unexpected_failure_is_said_in_the_log(window, monkeypatch):
    def broken(*args, **kwargs):
        raise ValueError("a rule broke")

    monkeypatch.setattr("app.pipeline.build", broken)
    window.on_build()
    assert window.log.toPlainText() == "Not built, unexpected ValueError: a rule broke"
    assert QApplication.overrideCursor() is None
    monkeypatch.undo()
    window.on_build()
    monkeypatch.setattr("app.pipeline.publish", broken)
    window.on_publish()
    assert window.log.toPlainText().endswith(
        "Not published, unexpected ValueError: a rule broke"
    )


def test_publishing_sends_the_built_protocol_and_says_where(window):
    window.publish_section.setValue(3)
    window.on_build()
    window.publish_button.click()
    assert window.site.uploads[-1]["section"] == 3
    assert window.log.toPlainText().endswith("Published to section 3")
    assert window.status.text() == "Published to section 3"


def test_a_refused_protocol_and_a_failed_upload_are_reported(window, monkeypatch):
    window.on_build()
    monkeypatch.setattr(window.site, "upload", lambda *a, **k: "bad cell")
    window.on_publish()
    assert window.log.toPlainText().endswith(
        "The site did not take the protocol: bad cell"
    )

    def fail(*args, **kwargs):
        raise SiteApiError("HTTP 400: no section 2")

    monkeypatch.setattr(window.site, "upload", fail)
    window.on_publish()
    assert window.log.toPlainText().endswith("Not published: HTTP 400: no section 2")


def _unwritable(monkeypatch):
    def refuse(config, path=None):
        raise PermissionError(13, "Permission denied", str(path))

    monkeypatch.setattr(settings, "save", refuse)


def test_settings_that_cannot_be_saved_are_said_and_the_build_still_runs(
    window, monkeypatch
):
    _unwritable(monkeypatch)
    window.on_build()
    assert window.log.toPlainText().startswith("ERROR: settings not saved:")
    assert window.status.text().endswith("error(s): see the Log tab")
    assert window.publish_button.isEnabled()  # what was built is still publishable
    window.token.setText("")
    window.on_build()  # a build that fails says both
    assert "ERROR: settings not saved:" in window.log.toPlainText()


def test_closing_with_settings_that_cannot_be_saved_warns(window, monkeypatch):
    _unwritable(monkeypatch)
    warned: list[str] = []
    monkeypatch.setattr(
        QMessageBox, "warning", lambda parent, title, text: warned.append(text)
    )
    window.closeEvent(QCloseEvent())
    assert warned and warned[0].startswith("settings not saved:")


def test_closing_the_window_keeps_the_settings(window):
    window.title.setText("Spring cup")
    window.closeEvent(QCloseEvent())
    assert settings.load(window._config_path).title == "Spring cup"
