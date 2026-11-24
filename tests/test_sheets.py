import pytest

from app.sheets import export_url, looks_like_a_page, read

SHEET = "https://docs.google.com/spreadsheets/d/1AbC_d-9"
EXPORT = f"{SHEET}/export?format=csv"
PUBLISHED = "https://docs.google.com/spreadsheets/d/e/2PACX-1vAb_c-9"


@pytest.mark.parametrize(
    ("link", "url"),
    [
        (f"{SHEET}/edit#gid=123", f"{EXPORT}&gid=123"),
        (f"{SHEET}/edit?usp=sharing&gid=45", f"{EXPORT}&gid=45"),
        (f" {SHEET}/edit ", EXPORT),
        (f"{EXPORT}&gid=7", f"{EXPORT}&gid=7"),
        ("https://example.com/results.csv", "https://example.com/results.csv"),
        # Published to the web: its own id after "/d/e/", never "e" taken for the id.
        (f"{PUBLISHED}/pubhtml", f"{PUBLISHED}/pub?output=csv"),
        (
            f"{PUBLISHED}/pub?gid=45&single=true&output=csv",
            f"{PUBLISHED}/pub?output=csv&gid=45&single=true",
        ),
    ],
)
def test_a_sheet_link_becomes_its_csv_export(link, url):
    assert export_url(link) == url


def test_the_last_answer_for_a_bib_counts_as_written_and_each_replaced_is_reported():
    csv = (
        'Timestamp,Bib,Result\n1/1 9:00,7,"2,5"\n1/1 9:01,12,8\n1/1 9:05,007,10\n'
        "1/1 9:06,7, 11 \n"
    )
    results = read(csv)
    assert results.values == {"7": 11.0, "12": 8.0}
    assert results.texts == {"7": "11", "12": "8"}
    assert results.problems == [
        "line 4: bib 7 answered again ('10'), replacing line 2 ('2,5')",
        "line 5: bib 7 answered again ('11'), replacing line 4 ('10')",
    ]
    assert results.athletes == []  # a sheet names nobody


def test_an_unreadable_first_answer_leaves_the_next_one_to_count():
    results = read("Timestamp,Bib,Result\n1/1,7,twelve\n1/1,7,12\n")
    assert results.values == {"7": 12.0}
    assert results.problems == ["line 2: 'twelve' is not a result"]


def test_an_unreadable_later_answer_replaces_nothing():
    results = read("Timestamp,Bib,Result\n1/1,7,12\n1/1,7,twelve\n")
    assert results.values == {"7": 12.0}
    assert results.problems == ["line 3: 'twelve' is not a result"]


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
