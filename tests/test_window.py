"""The window, driven through its real handlers with the site and Google faked."""

from __future__ import annotations

import pytest
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QApplication

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
    ]
    assert _titles(window) == ["Sprint", "Jump"]
    assert window.token.echoMode() == window.token.EchoMode.Password


def test_a_stage_shows_the_fields_of_its_source(window):
    sprint, jump = window.stage_tabs()
    assert sprint.form.isRowVisible(sprint.section)
    assert not sprint.form.isRowVisible(sprint.link)
    assert jump.form.isRowVisible(jump.link)
    assert not jump.form.isRowVisible(jump.token)
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
    window.delete_stage.click()
    assert _titles(window) == ["Jump"]
    window.delete_stage.click()
    assert _titles(window) == ["Jump"]
    assert window.log.toPlainText() == "A cup needs at least one stage."


def test_renaming_a_stage_renames_its_tab(window):
    jump = window.stage_tabs()[1]
    jump.name.setText("Standing jump")
    jump.name.setText("")
    assert _titles(window)[1] == "Stage 2"


def test_a_rule_this_build_does_not_know_falls_back_to_the_first(window):
    window.apply(Config(rule="best_three", stages=[StageConfig(rule="laps")]))
    assert window.config().rule == "sum_smallest_wins"
    assert window.config().stages[0].rule == "place_lower_better"


def test_a_build_shows_its_report_and_lets_the_protocol_be_published(window):
    window.on_build()
    text = window.log.toPlainText()
    assert "Jump: bibs no protocol names: 99" in text
    assert "Built: 2 table(s)" in text
    assert window.publish_button.isEnabled()
    assert QApplication.overrideCursor() is None  # the wait cursor is gone again
    assert settings.load(window._config_path) == SAVED  # saved on build


def test_a_changed_setting_asks_for_a_new_build_before_publishing(window):
    window.on_build()
    window.stage_tabs()[0].section.setValue(3)
    assert not window.publish_button.isEnabled()
    window.on_publish()  # nothing built: nothing sent
    assert window.site.uploads == []


def test_a_build_that_fails_says_why_and_publishes_nothing(window):
    window.token.setText("")
    window.on_build()
    assert window.log.toPlainText() == "Not built: Enter the cup event's upload token"
    assert QApplication.overrideCursor() is None
    assert not window.publish_button.isEnabled()


def test_publishing_sends_the_built_protocol_and_says_where(window):
    window.publish_section.setValue(3)
    window.on_build()
    window.publish_button.click()
    assert window.site.uploads[-1]["section"] == 3
    assert window.log.toPlainText().endswith("Published to section 3")


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


def test_closing_the_window_keeps_the_settings(window):
    window.title.setText("Spring cup")
    window.closeEvent(QCloseEvent())
    assert settings.load(window._config_path).title == "Spring cup"
