import pytest

from app.protocol_reader import read
from app.results import Athlete


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
