"""A stage's results out of a Google Forms response sheet.

The form asks two questions, in this order: the bib, then the result. Its response sheet
then has three columns -- the timestamp Google adds, the bib, the result -- and that is
how they are read: by position, so the questions may be worded in any language.
Rows are read in the sheet's order -- the order Google wrote the answers in, which may
part from their timestamps by a second -- and the last readable answer for a bib
counts, so a judge corrects a mark by answering again; every answer it replaces is
reported, so a second mark for an athlete is seen by the referee. A sheet names no
athletes: their names and categories come from the stages read from the site.
"""

from __future__ import annotations

import csv
import io
import re

from app.results import StageResults, normalize_bib, parse_value

_SHEETS_URL = "https://docs.google.com/spreadsheets/d/"
_SHEET = re.compile(r"^https://docs\.google\.com/spreadsheets/d/([A-Za-z0-9_-]+)")
# "File > Share > Publish to the web" gives a link of its own, its id after "/d/e/".
_PUBLISHED = re.compile(r"^https://docs\.google\.com/spreadsheets/d/e/([A-Za-z0-9_-]+)")
_GID = re.compile(r"[#?&]gid=(\d+)")


def export_url(link: str) -> str:
    """The CSV export of a Google Sheets link, its tab kept; any other address as it is.

    The sheet must be shared as "anyone with the link can view" for the export to open
    without signing in, or published to the web, whose link reads as its CSV too.
    """
    link = link.strip()
    tab = _GID.search(link)
    published = _PUBLISHED.match(link)
    if published is not None:
        url = f"{_SHEETS_URL}e/{published.group(1)}/pub?output=csv"
        return url + (f"&gid={tab.group(1)}&single=true" if tab else "")
    sheet = _SHEET.match(link)
    if sheet is None:
        return link
    url = f"{_SHEETS_URL}{sheet.group(1)}/export?format=csv"
    return url + (f"&gid={tab.group(1)}" if tab else "")


def looks_like_a_page(text: str) -> bool:
    """Whether Google answered with a web page instead of the CSV export.

    A sheet that is not shared for reading redirects its export to a sign-in page,
    which comes back as an ordinary answer: read as CSV, every line of it would look
    like a broken result and no result at all would be found.
    """
    head = text.lstrip("\ufeff \t\r\n")[:200].lower()
    return head.startswith(("<!doctype", "<html"))


def read(text: str) -> StageResults:
    """The last readable result for every bib, and what could not be read or was
    replaced by a later answer, line by line."""
    results = StageResults()
    counted: dict[str, int] = {}  # bib -> the line its result is read from
    rows = list(csv.reader(io.StringIO(text.lstrip("\ufeff"))))
    for line, row in enumerate(rows[1:], start=2):
        if not any(cell.strip() for cell in row):
            continue
        if len(row) < 3:
            results.problems.append(
                f"line {line}: expected a timestamp, a bib, a result"
            )
            continue
        bib, value = normalize_bib(row[1]), parse_value(row[2])
        if not bib:
            results.problems.append(f"line {line}: no bib")
        elif value is None:
            results.problems.append(f"line {line}: {row[2]!r} is not a result")
        else:
            # The maintainer, 2026-11-24: the last answer counts, so a judge can correct
            # a mark by answering again; the answer it replaces is still an error.
            if bib in counted:
                results.problems.append(
                    f"line {line}: bib {bib} answered again ({row[2].strip()!r}), "
                    f"replacing line {counted[bib]} ({results.texts[bib]!r})"
                )
            counted[bib] = line
            results.values[bib] = value
            results.texts[bib] = row[2].strip()
    return results
