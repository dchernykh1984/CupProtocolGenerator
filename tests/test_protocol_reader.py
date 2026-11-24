import pytest

from app.protocol_reader import read
from app.results import Athlete
from tests.conftest import lap_race


def test_athletes_come_in_the_protocols_order_each_in_their_category(stage_document):
    assert read(stage_document).athletes == [
        Athlete("7", "Ivanov", "UBT", "M10"),
        Athlete("12", "Petrov", "", "M10"),
        Athlete("13", "Sidorov", "", "M10"),
        Athlete("21", "Orlova", "", "W10"),
        Athlete("22", "Belova", "", "W10"),
    ]


def test_only_a_valid_result_of_an_athlete_who_started_counts(stage_document):
    results = read(stage_document)
    assert results.values == pytest.approx({"7": 8.40, "12": 8.90, "21": 9.10})
    assert results.texts == {"7": "8.40", "12": "8,90", "21": "0:09.10"}


def test_categories_are_named_by_the_protocols_groups(stage_document):
    assert read(stage_document).categories == {"M10": "Boys 10", "W10": "W10"}


def test_a_table_without_a_bib_column_is_no_table_of_athletes():
    document = {
        "schema": 1,
        "sections": [{"columns": [{"id": "a"}], "rows": [{"cells": {"a": "1"}}]}],
    }
    assert read(document).athletes == []


def test_in_a_lap_race_only_the_leaders_laps_count_each_category_its_own():
    results = read(lap_race())
    # Bib 2 is a lap down; W's leader has two laps, bib 5's three are disqualified.
    assert results.values == pytest.approx({"1": 2520.0, "4": 1920.0, "6": 1980.0})
    assert results.fewer_laps == ["2"]
    assert "2" not in results.texts
    assert [athlete.bib for athlete in results.athletes] == ["1", "2", "4", "5", "6"]


def test_in_a_live_race_the_leader_still_on_course_sets_the_laps():
    # The timing generator lists a rider still on course as DNF: laps, no result.
    document = lap_race()
    on_course = {"bib": "7", "lap1": "15:00.0", "lap2": "15:00.0", "lap3": "15:00.0"}
    document["sections"][1]["rows"].append({"cells": on_course, "status": "dnf"})
    results = read(document)
    assert sorted(results.values) == ["1"]  # W's two-lap finishers trail bib 7
    assert results.fewer_laps == ["2", "4", "6"]


def test_without_the_laps_rule_every_result_counts():
    results = read(lap_race(), leader_laps_only=False)
    assert sorted(results.values) == ["1", "2", "4", "6"]
    assert results.fewer_laps == []
