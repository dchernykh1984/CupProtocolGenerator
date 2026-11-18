import pytest

from app.sheets import export_url, looks_like_a_page, read

SHEET = "https://docs.google.com/spreadsheets/d/1AbC_d-9"
EXPORT = f"{SHEET}/export?format=csv"


@pytest.mark.parametrize(
    ("link", "url"),
    [
        (f"{SHEET}/edit#gid=123", f"{EXPORT}&gid=123"),
        (f"{SHEET}/edit?usp=sharing&gid=45", f"{EXPORT}&gid=45"),
        (f" {SHEET}/edit ", EXPORT),
        (f"{EXPORT}&gid=7", f"{EXPORT}&gid=7"),
        ("https://example.com/results.csv", "https://example.com/results.csv"),
    ],
)
def test_a_sheet_link_becomes_its_csv_export(link, url):
    assert export_url(link) == url


def test_the_last_answer_for_a_bib_wins_and_is_kept_as_written():
    csv = 'Timestamp,Bib,Result\n1/1 9:00,7,10\n1/1 9:01,12,8\n1/1 9:05,007,"2,5"\n'
    results = read(csv)
    assert results.values == {"7": 2.5, "12": 8.0}
    assert results.texts == {"7": "2,5", "12": "8"}
    assert results.athletes == []  # a sheet names nobody


def test_what_cannot_be_read_is_reported_by_line():
    csv = "\ufeffTimestamp,Bib,Result\n1/1,7,ten\n1/1,,5\n1/1,8\n,,\n1/1,9,4\n"
    results = read(csv)
    assert results.values == {"9": 4.0}
    assert results.problems == [
        "line 2: 'ten' is not a result",
        "line 3: no bib",
        "line 4: expected a timestamp, a bib, a result",
    ]


@pytest.mark.parametrize(
    ("text", "page"),
    [
        ("<!DOCTYPE html><html><body>Sign in</body></html>", True),
        ("\ufeff\n <html lang='en'>", True),
        ("Timestamp,Bib,Result\n1,7,10\n", False),
        ("", False),
    ],
)
def test_a_sign_in_page_is_told_apart_from_the_results(text, page):
    assert looks_like_a_page(text) is page
