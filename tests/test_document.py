import json
from pathlib import Path

import jsonschema
import pytest

from app.document import build, format_number, stage_column
from app.results import Athlete
from app.rules import cup_rule, stage_rule
from app.scoring import standings

SCHEMA = json.loads(
    (Path(__file__).parent / "fixtures" / "protocol-document-v1.json").read_text()
)
STAGES = ["Stage 1: sprint", "Stage 2: jump"]


def _table(team: str = "UBT"):
    athletes = [
        Athlete("7", "Ivanov", team, "M10"),
        Athlete("12", "Petrov", "", "M10"),
        Athlete("21", "Orlova", "", "W10"),
    ]
    values = [{"7": 8.4, "12": 8.9, "21": 9.1}, {"7": 180, "21": 150.5}]
    rules = [stage_rule("place_lower_better"), stage_rule("place_higher_better")]
    return standings(athletes, values, rules, cup_rule("sum_smallest_wins"))


def _document(**kwargs):
    defaults = {
        "title": "Cup, after two stages",
        "stages": STAGES,
        "table": _table(),
        "categories": {"M10": "Boys 10", "W10": "Girls 10"},
        "texts": [
            {"7": "8.40", "12": "8.90", "21": "9.10"},
            {"7": "180", "21": "150.5"},
        ],
    }
    return build(**{**defaults, **kwargs})


def test_the_document_is_what_the_site_takes():
    jsonschema.validate(_document(), SCHEMA)
    jsonschema.validate(_document(title="", table=_table(team="")), SCHEMA)


def test_a_category_is_a_table_of_its_own_named_and_declared():
    document = _document()
    assert [(s["title"], s["group"]) for s in document["sections"]] == [
        ("Boys 10", "M10"),
        ("Girls 10", "W10"),
    ]
    assert document["groups"] == [
        {"id": "M10", "label": "Boys 10"},
        {"id": "W10", "label": "Girls 10"},
    ]
    assert document["title"] == "Cup, after two stages"


def test_a_row_carries_each_stage_with_its_place_and_the_total():
    boys = _document()["sections"][0]
    assert [c["id"] for c in boys["columns"]] == [
        "place",
        "bib",
        "name",
        "team",
        "stage_1",
        "stage_1_place",
        "stage_2",
        "stage_2_place",
        "total",
    ]
    labels = [c["label"] for c in boys["columns"]][4:8]
    assert labels == [STAGES[0], f"{STAGES[0]} place", STAGES[1], f"{STAGES[1]} place"]
    # A phone leaves out the stage places first: the highest priority goes first.
    assert {c.get("priority") for c in boys["columns"][5:8:2]} == {3}
    first, second = (row["cells"] for row in boys["rows"])
    assert (first["stage_1"], first["stage_1_place"]) == ("8.40", "1")  # as written
    assert (first["stage_2"], first["stage_2_place"]) == ("180", "1")
    assert (first["place"], first["total"]) == ("1", "2")
    # 12 has no jump: the place stage puts him after everybody with one; no result
    # is shown.
    assert (second["stage_2"], second["stage_2_place"]) == ("", "2")
    assert (second["place"], second["total"]) == ("2", "4")


def test_no_team_column_when_nobody_has_one_nor_title_when_none_is_given():
    document = _document(title="  ", table=_table(team=""))
    assert "team" not in [c["id"] for c in document["sections"][0]["columns"]]
    assert "title" not in document


def test_athletes_without_a_category_make_one_untitled_table():
    table = standings(
        [Athlete("1", "A")],
        [{"1": 8.0}],
        [stage_rule("place_lower_better")],
        cup_rule("sum_smallest_wins"),
    )
    document = build("", ["Sprint"], table, {}, [{}])
    assert "group" not in document["sections"][0] and "groups" not in document
    jsonschema.validate(document, SCHEMA)


def test_a_sum_of_times_is_written_as_a_time_as_precise_as_its_stages():
    times = [stage_rule("time")] * 2
    athletes = [Athlete("7", "Ivanov"), Athlete("12", "Petrov"), Athlete("3", "Orlov")]
    values = [{"7": 8.4, "12": 3600.0, "3": 9.0}, {"7": 62.5, "12": 0.5}]
    table = standings(athletes, values, times, cup_rule("sum_of_times"))
    texts = [{"7": "8.40", "12": "1:00:00", "3": "9.00"}, {"7": "1:02.5", "12": "0.5"}]
    document = build("", ["Sprint", "Run"], table, {}, texts, total_is_time=True)
    jsonschema.validate(document, SCHEMA)
    rows = [row["cells"] for row in document["sections"][0]["rows"]]
    assert [(r["bib"], r["place"], r["total"]) for r in rows] == [
        ("7", "1", "1:10.90"),
        ("12", "2", "1:00:00.5"),
        ("3", "", ""),
    ]
    assert (rows[0]["stage_2"], rows[0]["stage_2_place"]) == ("1:02.5", "2")


def test_a_time_less_the_repetitions_is_the_total_of_an_all_round_test():
    rules = [stage_rule("time"), stage_rule("minus_second_per_repetition_test")]
    athletes = [Athlete("7", "Ivanov"), Athlete("12", "Petrov")]
    values = [{"7": 62.5, "12": 61.0}, {"7": 23, "12": 5}]
    table = standings(athletes, values, rules, cup_rule("sum_of_times"))
    texts = [{"7": "1:02.5", "12": "1:01.0"}, {"7": "23", "12": "5"}]
    document = build("", ["Run", "Pull-ups"], table, {}, texts, total_is_time=True)
    rows = [row["cells"] for row in document["sections"][0]["rows"]]
    assert [(r["bib"], r["place"], r["total"]) for r in rows] == [
        ("7", "1", "0:39.5"),  # 62.5 s less 23 pull-ups
        ("12", "2", "0:56.0"),
    ]
    assert (rows[0]["stage_2"], rows[0]["stage_2_place"]) == ("23", "1")


@pytest.mark.parametrize(
    ("value", "text"),
    [
        (12.0, "12"),
        (150.5, "150.5"),
        (2.35, "2.35"),
        (1351.123, "1351.123"),  # every digit of a sum of results, not six of them
        (45123.45, "45123.45"),
        (1234567.5, "1234567.5"),
    ],
)
def test_a_number_is_written_as_a_person_would(value, text):
    assert format_number(value) == text


def test_a_stage_column_is_numbered_from_one():
    assert [stage_column(i) for i in range(3)] == ["stage_1", "stage_2", "stage_3"]
