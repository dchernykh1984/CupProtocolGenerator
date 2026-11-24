from __future__ import annotations

from typing import Any

import pytest

from app.config import Config, Source, StageConfig
from app.pipeline import PipelineError, build, publish
from app.site_api import SiteApiError
from tests.conftest import lap_race, stage_protocol

JUMPS = "https://docs.google.com/spreadsheets/d/JUMP/edit#gid=1"
JUMPS_CSV = "https://docs.google.com/spreadsheets/d/JUMP/export?format=csv&gid=1"
RUNS = "https://docs.google.com/spreadsheets/d/RUN/edit"
RUNS_CSV = "https://docs.google.com/spreadsheets/d/RUN/export?format=csv"
SHEETS = {
    JUMPS_CSV: "Timestamp,Bib,Result\n1,7,180\n1,12,190\n1,21,150\n1,99,3\n1,13,x\n",
    RUNS_CSV: "Timestamp,Bib,Result\n1,7,1:02.5\n1,12,1:01.0\n1,21,59.9\n",
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

    def protocols(self, competition_id: int, token: str):
        assert self.events[token][0] == competition_id  # read by the event's own token
        return self.listed.get(competition_id, [])

    def protocol(self, protocol_id: int, token: str):
        listed = self.listed.get(self.events[token][0], [])
        assert protocol_id in [p["id"] for p in listed]  # its event's token reads it
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
    assert [c["label"] for c in boys["columns"]][-5:] == [
        "Sprint",
        "Sprint place",
        "Jump",
        "Jump place",
        "Total",
    ]
    assert [row["cells"]["bib"] for row in boys["rows"]] == ["7", "12", "13"]
    assert built.report == [
        "Sprint: 3 results",
        "ERROR: Jump: line 6: 'x' is not a result",
        "Jump: 4 results",
        "ERROR: Jump: bibs no protocol names: 99",
    ]


def test_a_stage_of_another_event_is_read_by_its_token_and_each_event_asked_once():
    stage = StageConfig("Away", Source.SITE, token="other", section=2)
    site = FakeSite()
    build(_config(stages=[StageConfig("Home"), stage, StageConfig("Again")]), site)
    assert site.read == [4, 8, 4]
    assert site.asked == ["cup", "other"]


def test_a_lap_race_counts_only_the_leaders_laps_and_says_whom_it_left_out():
    site = FakeSite(document=lap_race())
    stages = [StageConfig("XCO", Source.SITE, rule="time")]
    built = build(_config(stages=stages, rule="sum_of_times"), site)
    assert built.report == [
        "XCO: 3 results",
        "XCO: not counted, fewer laps than their leader: 2",
    ]
    men = built.document["sections"][0]["rows"]
    assert [(row["cells"]["bib"], row["cells"]["place"]) for row in men] == [
        ("1", "1"),
        ("2", ""),
    ]
    stages[0].leader_laps_only = False  # a Number of Tries race: attempts, no laps
    built = build(_config(stages=stages, rule="sum_of_times"), site)
    assert built.report == ["XCO: 4 results"]


def test_a_cup_by_the_sum_of_places_adds_each_stages_place_up():
    stages = [
        StageConfig("Sprint", Source.SITE, rule="place_lower_better"),
        StageConfig("Jump", Source.SHEET, link=JUMPS, rule="place_higher_better"),
    ]
    built = build(_config(stages=stages, rule="sum_smallest_wins"), FakeSite())
    boys = {
        row["cells"]["bib"]: row["cells"]
        for row in built.document["sections"][0]["rows"]
    }
    # Sprint: 7 first, 12 second; Jump: 12 (190) first, 7 (180) second.
    assert (boys["7"]["stage_1_place"], boys["7"]["stage_2_place"]) == ("1", "2")
    assert (boys["7"]["total"], boys["12"]["total"]) == ("3", "3")
    assert (boys["7"]["place"], boys["12"]["place"]) == ("1", "1")


def test_a_cup_by_the_largest_sum_of_results_ranks_the_most_first():
    # Sprint and Jump scored by their results as points: 12 has 8.90 + 190, 7 has
    # 8.40 + 180; 13 has no result at all and stays unscored, unless all are placed.
    stages = [
        StageConfig("Sprint", Source.SITE, rule="result_higher_better"),
        StageConfig("Jump", Source.SHEET, link=JUMPS, rule="result_higher_better"),
    ]

    def boys(**kwargs):
        config = _config(stages=stages, rule="sum_largest_wins", **kwargs)
        rows = build(config, FakeSite()).document["sections"][0]["rows"]
        return [row["cells"] for row in rows]

    cells = boys()
    assert [(c["bib"], c["place"], c["total"]) for c in cells] == [
        ("12", "1", "198.9"),
        ("7", "2", "188.4"),
        ("13", "", ""),
    ]
    assert (cells[0]["stage_1_place"], cells[0]["stage_2_place"]) == ("1", "1")
    assert (cells[2]["stage_1"], cells[2]["stage_1_place"]) == ("", "")
    placed = boys(place_everybody=True)
    assert [(c["bib"], c["place"]) for c in placed] == [
        ("12", "1"),
        ("7", "2"),
        ("13", "3"),
    ]


@pytest.mark.parametrize(
    ("cup", "stage", "message"),
    [
        (
            "sum_largest_wins",
            "place_lower_better",
            "Sprint: the cup's largest sum wins: score this stage by \"Result as",
        ),
        (
            "sum_smallest_wins",
            "result_higher_better",
            "Sprint: the cup's smallest sum wins: score this stage by \"Place,",
        ),
    ],
)
def test_points_that_improve_the_other_way_than_the_sum_wins_are_refused(
    cup, stage, message
):
    stages = [StageConfig("Sprint", Source.SITE, rule=stage)]
    with pytest.raises(PipelineError, match=message):
        build(_config(stages=stages, rule=cup), FakeSite())


def test_the_event_title_and_a_stage_number_stand_in_for_missing_names():
    built = build(_config(stages=[StageConfig()]), FakeSite())
    assert built.document["title"] == "Cup"
    assert built.document["sections"][0]["columns"][-3]["label"] == "Stage 1"


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
        (
            FakeSite(),
            _config(rule="sum_of_times"),
            'Sprint: the cup rule adds times up: score this stage by "Time, the lowest',
        ),
        (
            FakeSite(),
            _config(stages=[StageConfig("Sprint", rule="time")]),
            "Sprint: the stage counts by its time, but the cup rule does not add "
            "times up: pick the cup rule \"Sum of the stages' times, the smallest",
        ),
        (FakeSite(protocols={249: []}), _config(), "Sprint: no protocol in section 1"),
        (FakeSite(document={}), _config(), "Sprint: protocol 4 has no data the site"),
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


def test_a_stage_the_site_or_google_fails_to_give_is_named_in_the_error(monkeypatch):
    site = FakeSite()

    def refuse(url: str) -> str:
        raise SiteApiError("HTTP 404: Not Found")

    monkeypatch.setattr(site, "fetch_text", refuse)
    with pytest.raises(PipelineError, match="Jump: HTTP 404: Not Found"):
        build(_config(), site)


def test_a_cup_of_summed_times_shows_every_stage_and_the_total_as_a_time():
    stages = [
        StageConfig("Sprint", Source.SITE, rule="time"),
        StageConfig("Run", Source.SHEET, link=RUNS, rule="time"),
    ]
    built = build(_config(rule="sum_of_times", stages=stages), FakeSite())
    boys, girls = (
        [(r["cells"]["bib"], r["cells"]["place"], r["cells"]["total"]) for r in rows]
        for rows in (section["rows"] for section in built.document["sections"])
    )
    assert boys == [("12", "1", "1:09.90"), ("7", "2", "1:10.90"), ("13", "", "")]
    assert girls == [("21", "1", "1:09.00"), ("22", "", "")]
    first = built.document["sections"][0]["rows"][0]["cells"]
    assert (first["stage_1"], first["stage_2"]) == ("8,90", "1:01.0")


def test_a_broadcast_places_everybody_who_missed_stages_after_the_rest():
    def boys(config):
        rows = build(config, FakeSite()).document["sections"][0]["rows"]
        cells = [row["cells"] for row in rows]
        return [(cell["bib"], cell["place"], cell["total"]) for cell in cells]

    # Stages scored by time: 13 has no sprint time and no run, so no stage and no total.
    # (A place stage would place him after everybody with a result instead.)
    stages = [
        StageConfig("Sprint", Source.SITE, rule="time"),
        StageConfig("Run", Source.SHEET, link=RUNS, rule="time"),
    ]
    times = {"stages": stages, "rule": "sum_of_times"}
    ranked = [("12", "1", "1:09.90"), ("7", "2", "1:10.90")]
    assert boys(_config(**times)) == [*ranked, ("13", "", "")]
    assert boys(_config(**times, place_everybody=True)) == [*ranked, ("13", "3", "")]


def test_publishing_sends_the_protocol_to_its_section_live_until_final():
    site = FakeSite()
    built = build(_config(), site)
    publish(_config(title="Final", publish_section=5, final=True), site, built)
    publish(_config(), site, built)
    assert site.uploads == [
        {"token": "cup", "section": 5, "label": "Final", "live": False},
        {"token": "cup", "section": 2, "label": "", "live": True},
    ]
