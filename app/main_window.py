"""The window, laid out as StravaProtocolGenerator's: a Cup tab with the cup's settings,
the build and publish buttons and the log, and a Stages tab with a tab per stage.

A build reads everything fresh; any change to a setting asks for a new build before the
protocol may be published, so what goes to the site is what the log just showed.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QPlainTextEdit,
    QPushButton,
    QSpinBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from app import config as settings
from app import pipeline
from app.config import Config, Source, StageConfig
from app.rules import CUP_RULES, STAGE_RULES, CupRule, StageRule
from app.site_api import DEFAULT_SITE, SiteApi, SiteApiError

ICON_PATH = str(Path(__file__).parent / "app.ico")
APP_DISPLAY_NAME = "Cup Protocol Generator"
APP_DESKTOP_NAME = "cup-protocol-generator"
MAX_SECTION = 2_147_483_647
SOURCES = {Source.SITE: "Protocol on the site", Source.SHEET: "Google Forms sheet"}


def _rule_box(
    rules: tuple[StageRule, ...] | tuple[CupRule, ...], key: str
) -> QComboBox:
    """A drop-down of rules, each explained in its tooltip, ``key`` picked."""
    box = QComboBox()
    for rule in rules:
        box.addItem(rule.label, rule.key)
        box.setItemData(box.count() - 1, rule.description, Qt.ItemDataRole.ToolTipRole)
    box.setCurrentIndex(max(box.findData(key), 0))
    return box


def _section_box(value: int) -> QSpinBox:
    box = QSpinBox()
    box.setRange(1, MAX_SECTION)
    box.setValue(value)
    return box


class StageTab(QWidget):
    """One stage: its name, where its results come from, the rule it is scored by."""

    def __init__(self, stage: StageConfig, on_change: Callable[[], None]) -> None:
        super().__init__()
        self.name = QLineEdit(stage.name)
        self.source = QComboBox()
        for source, label in SOURCES.items():
            self.source.addItem(label, source.value)
        self.source.setCurrentIndex(self.source.findData(stage.source.value))
        self.token = QLineEdit(stage.token)
        self.token.setEchoMode(QLineEdit.EchoMode.Password)
        self.token.setPlaceholderText("The cup event's token when left empty")
        self.section = _section_box(stage.section)
        self.link = QLineEdit(stage.link)
        self.link.setPlaceholderText("Google Sheets link to the form's responses")
        self.rule = _rule_box(STAGE_RULES, stage.rule)
        self.form = QFormLayout(self)
        self.form.addRow("Stage name", self.name)
        self.form.addRow("Results from", self.source)
        self.form.addRow("Stage event's upload token", self.token)
        self.form.addRow("Protocol section", self.section)
        self.form.addRow("Sheet link", self.link)
        self.form.addRow("Stage rule", self.rule)
        self.source.currentIndexChanged.connect(self._show_source)
        self._show_source()
        for line in (self.name, self.token, self.link):
            line.textChanged.connect(on_change)
        for box in (self.source, self.rule):
            box.currentIndexChanged.connect(on_change)
        self.section.valueChanged.connect(on_change)

    def _show_source(self) -> None:
        on_site = self.source.currentData() == Source.SITE.value
        self.form.setRowVisible(self.token, on_site)
        self.form.setRowVisible(self.section, on_site)
        self.form.setRowVisible(self.link, not on_site)

    def stage(self) -> StageConfig:
        return StageConfig(
            name=self.name.text().strip(),
            source=Source(self.source.currentData()),
            token=self.token.text().strip(),
            section=self.section.value(),
            link=self.link.text().strip(),
            rule=str(self.rule.currentData()),
        )


class MainWindow(QMainWindow):
    def __init__(
        self,
        api_factory: Callable[[str], SiteApi] = SiteApi,
        config_path: Path | None = None,
    ) -> None:
        super().__init__()
        self.setWindowTitle(APP_DISPLAY_NAME)
        self.setWindowIcon(QIcon(ICON_PATH))
        self._api_factory = api_factory
        self._config_path = config_path or settings.config_path()
        self._built: pipeline.Built | None = None
        self.tabs = QTabWidget()
        self.tabs.addTab(self._cup_tab(), "Cup")
        self.tabs.addTab(self._stages_tab(), "Stages")
        self.setCentralWidget(self.tabs)
        self.apply(settings.load(self._config_path))

    def _cup_tab(self) -> QWidget:
        self.site_url = QLineEdit()
        self.token = QLineEdit()
        self.token.setEchoMode(QLineEdit.EchoMode.Password)
        self.title = QLineEdit()
        self.title.setPlaceholderText("The cup event's title when left empty")
        self.rule = _rule_box(CUP_RULES, CUP_RULES[0].key)
        self.publish_section = _section_box(2)
        self.final = QCheckBox("Final (the site stops checking for updates)")
        self.place_everybody = QCheckBox(
            "Place everybody, for a broadcast: who missed stages comes after the rest"
        )
        form = QFormLayout()
        form.addRow("Site", self.site_url)
        form.addRow("Cup event's upload token", self.token)
        form.addRow("Protocol title", self.title)
        form.addRow("Cup rule", self.rule)
        form.addRow("Publish to section", self.publish_section)
        form.addRow("", self.final)
        form.addRow("", self.place_everybody)
        self.build_button = QPushButton("Build")
        self.publish_button = QPushButton("Publish")
        self.publish_button.setEnabled(False)
        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)
        buttons = QHBoxLayout()
        buttons.addWidget(self.build_button)
        buttons.addWidget(self.publish_button)
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.addLayout(form)
        layout.addLayout(buttons)
        layout.addWidget(self.log, stretch=1)
        self.build_button.clicked.connect(self.on_build)
        self.publish_button.clicked.connect(self.on_publish)
        for line in (self.site_url, self.token, self.title):
            line.textChanged.connect(self._invalidate)
        self.rule.currentIndexChanged.connect(self._invalidate)
        self.publish_section.valueChanged.connect(self._invalidate)
        self.final.toggled.connect(self._invalidate)
        self.place_everybody.toggled.connect(self._invalidate)
        return tab

    def _stages_tab(self) -> QWidget:
        self.stages = QTabWidget()
        self.add_left = QPushButton("Add stage left")
        self.add_right = QPushButton("Add stage right")
        self.delete_stage = QPushButton("Delete stage")
        buttons = QHBoxLayout()
        for button in (self.add_left, self.add_right, self.delete_stage):
            buttons.addWidget(button)
        buttons.addStretch(1)
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.addWidget(self.stages, stretch=1)
        layout.addLayout(buttons)
        self.add_left.clicked.connect(lambda: self.add_stage_copy(0))
        self.add_right.clicked.connect(lambda: self.add_stage_copy(1))
        self.delete_stage.clicked.connect(self.on_delete_stage)
        return tab

    def stage_tabs(self) -> list[StageTab]:
        widgets = (self.stages.widget(i) for i in range(self.stages.count()))
        return [tab for tab in widgets if isinstance(tab, StageTab)]

    def apply(self, config: Config) -> None:
        self.site_url.setText(config.site_url)
        self.token.setText(config.token)
        self.title.setText(config.title)
        self.rule.setCurrentIndex(max(self.rule.findData(config.rule), 0))
        self.publish_section.setValue(config.publish_section)
        self.final.setChecked(config.final)
        self.place_everybody.setChecked(config.place_everybody)
        while self.stages.count():
            self._drop_stage(0)
        for stage in config.stages or [StageConfig()]:
            self.add_stage(stage)
        self._invalidate()

    def config(self) -> Config:
        return Config(
            site_url=self.site_url.text().strip(),
            token=self.token.text().strip(),
            title=self.title.text().strip(),
            rule=str(self.rule.currentData()),
            publish_section=self.publish_section.value(),
            final=self.final.isChecked(),
            place_everybody=self.place_everybody.isChecked(),
            stages=[tab.stage() for tab in self.stage_tabs()],
        )

    def add_stage(self, stage: StageConfig, index: int | None = None) -> StageTab:
        tab = StageTab(stage, self._invalidate)
        at = self.stages.count() if index is None else index
        self.stages.insertTab(at, tab, "")
        tab.name.textChanged.connect(self._retitle)
        self.stages.setCurrentIndex(at)
        self._retitle()
        self._invalidate()
        return tab

    def _retitle(self) -> None:
        """Every tab titled by its stage's name, an unnamed one by its place, as the
        protocol's column will call it: a stage moved along keeps the two agreeing."""
        for index, tab in enumerate(self.stage_tabs()):
            name = tab.name.text().strip()
            self.stages.setTabText(index, name or f"Stage {index + 1}")

    def add_stage_copy(self, offset: int) -> StageTab:
        """A copy of the current stage beside it: offset 0 to its left, 1 right."""
        current = self.stages.currentWidget()
        template = current.stage() if isinstance(current, StageTab) else StageConfig()
        return self.add_stage(template, self.stages.currentIndex() + offset)

    def on_delete_stage(self) -> None:
        if self.stages.count() <= 1:
            self.log.appendPlainText("A cup needs at least one stage.")
            return
        self._drop_stage(self.stages.currentIndex())
        self._retitle()
        self._invalidate()

    def _drop_stage(self, index: int) -> None:
        """Take a stage's tab out and free it: removeTab alone keeps it alive."""
        tab = self.stages.widget(index)
        self.stages.removeTab(index)
        if tab is not None:
            tab.deleteLater()

    def _invalidate(self) -> None:
        """A changed setting makes the last build stale: build again to publish."""
        self._built = None
        self.publish_button.setEnabled(False)

    def _api(self, config: Config) -> SiteApi:
        return self._api_factory(config.site_url or DEFAULT_SITE)

    def on_build(self) -> None:
        config = self.config()
        settings.save(config, self._config_path)
        # The site and every sheet are read here, in the window's own thread: say so
        # before it goes quiet for the seconds that takes.
        self.log.setPlainText("Building...")
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        QApplication.processEvents()
        try:
            built = pipeline.build(config, self._api(config))
        except (pipeline.PipelineError, SiteApiError) as exc:
            self.log.setPlainText(f"Not built: {exc}")
            return
        except Exception as exc:  # a rule's own failure must not leave "Building..."
            self.log.setPlainText(f"Not built, unexpected {type(exc).__name__}: {exc}")
            return
        finally:
            QApplication.restoreOverrideCursor()
        self.log.setPlainText("\n".join(built.report))
        self.log.appendPlainText(f"Built: {len(built.document['sections'])} table(s)")
        self._built = built
        self.publish_button.setEnabled(True)

    def on_publish(self) -> None:
        if self._built is None:
            return
        config = self.config()
        try:
            refused = pipeline.publish(config, self._api(config), self._built)
        except SiteApiError as exc:
            self.log.appendPlainText(f"Not published: {exc}")
            return
        except Exception as exc:  # said in the log rather than lost on stderr
            name = type(exc).__name__
            self.log.appendPlainText(f"Not published, unexpected {name}: {exc}")
            return
        if refused:
            self.log.appendPlainText(f"The site did not take the protocol: {refused}")
            return
        self.log.appendPlainText(f"Published to section {config.publish_section}")

    def closeEvent(self, event: QCloseEvent) -> None:  # noqa: N802 - Qt's name
        settings.save(self.config(), self._config_path)
        super().closeEvent(event)
