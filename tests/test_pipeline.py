from __future__ import annotations

from typing import Any

import pytest

from app.config import Config, Source, StageConfig
from app.pipeline import PipelineError, build, publish
from tests.conftest import stage_protocol

JUMPS = "https://docs.google.com/spreadsheets/d/JUMP/edit#gid=1"
JUMPS_CSV = "https://docs.google.com/spreadsheets/d/JUMP/export?format=csv&gid=1"
SHEETS = {
    JUMPS_CSV: "Timestamp,Bib,Result\n1,7,180\n1,12,190\n1,21,150\n1,99,3\n1,13,x\n"
}


class FakeSite:
    """The site and Google as the pipeline sees them, with nothing on the network.

    Two events: the cup's ("cup", id 249) and another stage's ("other", id 300).
    """

    def __init__(self, protocols=None, document=None, sheets=None, events=None):
        self.events = events or {"cup": (249, "Cup"), "other": (300, "Stage 2 event")}
        self.listed = protocols or {
            249: [
                {"id": 3, "section": 1, "protocol_type": "absolute"},
                {"id": 4, "section": 1, "protocol_type": "group"},
            ],
            300: [{"id": 8, "section": 2, "protocol_type": "absolute"}],
        }
        self.document = stage_protocol() if document is None else document
        self.sheets = SHEETS if sheets is None else sheets
        self.asked: list[str] = []
        self.read: list[int] = []
        self.uploads: list[dict[str, Any]] = []

    def competition(self, token: str):
        self.asked.append(token)
        return self.events.get(token, (0, ""))

    def protocols(self, competition_id: int):
        return self.listed.get(competition_id, [])

    def protocol(self, protocol_id: int):
        self.read.append(protocol_id)
        return {"id": protocol_id, "document": self.document}

    def fetch_text(self, url: str) -> str:
        return self.sheets[url]

    def upload(self, token, document, section, stage_label="", is_live=True):
        self.uploads.append(
            {"token": token, "section": section, "label": stage_label, "live": is_live}
        )
        return ""


def _config(**kwargs) -> Config:
    stages = [
        StageConfig("Sprint", Source.SITE),
        StageConfig("Jump", Source.SHEET, link=JUMPS, rule="place_higher_better"),
    ]
    return Config(**{"token": "cup", "stages": stages, **kwargs})


def test_the_stages_make_one_protocol_and_say_what_they_could_not_read():
    site = FakeSite()
    built = build(_config(title=" Final "), site)
    assert site.read == [4]  # the group protocol of section 1: it carries categories
    assert built.document["title"] == "Final"
    boys = built.document["sections"][0]
    assert [c["label"] for c in boys["columns"]][-3:] == ["Sprint", "Jump", "Total"]
    assert [row["cells"]["bib"] for row in boys["rows"]] == ["7", "12", "13"]
    assert built.report == [
        "Sprint: 3 results",
        "Jump: line 6: 'x' is not a result",
        "Jump: 4 results",
        "Jump: bibs no protocol names: 99",
    ]


def test_a_stage_of_another_event_is_read_by_its_token_and_each_event_asked_once():
    stage = StageConfig("Away", Source.SITE, token="other", section=2)
    site = FakeSite()
    build(_config(stages=[StageConfig("Home"), stage, StageConfig("Again")]), site)
    assert site.read == [4, 8, 4]
    assert site.asked == ["cup", "other"]


def test_the_event_title_and_a_stage_number_stand_in_for_missing_names():
    built = build(_config(stages=[StageConfig()]), FakeSite())
    assert built.document["title"] == "Cup"
    assert built.document["sections"][0]["columns"][-2]["label"] == "Stage 1"


def test_the_absolute_protocol_serves_when_a_section_has_no_group_one():
    site = FakeSite(
        protocols={249: [{"id": 3, "section": 1, "protocol_type": "absolute"}]}
    )
    build(_config(), site)
    assert site.read == [3]


@pytest.mark.parametrize(
    ("site", "config", "message"),
    [
        (FakeSite(), Config(), "Enter the cup event's upload token"),
        (FakeSite(), _config(token="nobody"), "does not know this upload token"),
        (FakeSite(), _config(stages=[]), "Add a stage"),
        (FakeSite(), _config(rule="best_three"), "Unknown cup rule 'best_three'"),
        (
            FakeSite(),
            _config(stages=[StageConfig("Run", rule="laps")]),
            "Run: unknown rule 'laps'",
        ),
        (FakeSite(protocols={249: []}), _config(), "Sprint: no protocol in section 1"),
        (FakeSite(document={}), _config(), "Sprint: protocol 4 has no data, only HTML"),
        (
            FakeSite(),
            _config(stages=[StageConfig("Pull", Source.SHEET)]),
            "Pull: no sheet link",
        ),
        (
            FakeSite(sheets={JUMPS_CSV: "<!doctype html><title>Sign in"}),
            _config(),
            "Jump: Google answered with a page",
        ),
        (
            FakeSite(),
            _config(stages=[StageConfig("Jump", Source.SHEET, link=JUMPS)]),
            "No stage names an athlete",
        ),
        (
            FakeSite(document={"schema": 1, "sections": []}),
            _config(),
            "No stage names an athlete",
        ),
    ],
)
def test_what_the_protocol_cannot_be_built_without_is_said(site, config, message):
    with pytest.raises(PipelineError, match=message):
        build(config, site)


def test_publishing_sends_the_protocol_to_its_section_live_until_final():
    site = FakeSite()
    built = build(_config(), site)
    publish(_config(title="Final", publish_section=5, final=True), site, built)
    publish(_config(), site, built)
    assert site.uploads == [
        {"token": "cup", "section": 5, "label": "Final", "live": False},
        {"token": "cup", "section": 2, "label": "", "live": True},
    ]
