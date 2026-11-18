import pytest

from app.results import normalize_bib, parse_value


@pytest.mark.parametrize(
    ("text", "value"),
    [
        ("12", 12.0),
        ("2,35", 2.35),
        (" 150 ", 150.0),
        ("8.43", 8.43),
        ("0:08.43", 8.43),
        ("0:08,43", 8.43),
        ("12:05", 725.0),
        ("1:02:33.4", 3753.4),
    ],
)
def test_a_result_is_a_number_or_a_time_in_seconds(text, value):
    assert parse_value(text) == pytest.approx(value)


@pytest.mark.parametrize(
    "text", ["", "DNF", "dns", "-8.4", "8.4.3", "1:75", "1:60:00", "1 2", "abc"]
)
def test_anything_else_is_no_result(text):
    assert parse_value(text) is None


@pytest.mark.parametrize(
    ("text", "bib"), [("007", "7"), (" 1 2 ", "12"), ("A7", "A7"), ("a7", "A7")]
)
def test_a_bib_is_compared_without_spaces_and_leading_zeros(text, bib):
    assert normalize_bib(text) == bib
