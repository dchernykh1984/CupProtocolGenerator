"""A stage's results out of a protocol published on the cycling site.

The protocol is the site's structured document (schema 1), as the timing generators
upload it. Its columns say what they hold by their ``role``: ``bib``, ``name``, ``team``
and ``result`` are read; a row's category is its ``group``, or its section's.
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from app.results import Athlete, StageResults, normalize_bib, parse_value

# A row with one of these statuses has no result, whatever its result cell says.
_NOT_A_RESULT = {"dns", "dnf", "dsq"}


def _text(cell: Any) -> str:
    if isinstance(cell, dict):
        return str(cell.get("text") or "")
    return str(cell or "")


def _tables(sections: list[dict[str, Any]], group: str) -> Iterator[tuple[dict, str]]:
    """Every section with rows, and the category its rows fall in unless they say."""
    for section in sections:
        own = str(section.get("group") or group)
        if section.get("rows"):
            yield section, own
        yield from _tables(section.get("sections") or [], own)


def _roles(section: dict[str, Any]) -> dict[Any, str]:
    """Column id by role, the first column of each role."""
    roles: dict[Any, str] = {}
    for column in section.get("columns") or []:
        roles.setdefault(column.get("role"), column["id"])
    return roles


def read(document: dict[str, Any]) -> StageResults:
    """The athletes in the order the protocol lists them, and their valid results.

    An athlete listed twice (an absolute and a group table of one run) is read once,
    where they first appear. A row without a bib is not an athlete.
    """
    results = StageResults(
        categories={
            str(group["id"]): str(group.get("label") or group["id"])
            for group in document.get("groups") or []
        }
    )
    seen: set[str] = set()
    for section, group in _tables(document.get("sections") or [], ""):
        roles = _roles(section)
        if "bib" not in roles:
            continue
        for row in section["rows"]:
            cells = row.get("cells") or {}
            bib = normalize_bib(_text(cells.get(roles["bib"])))
            if not bib or bib in seen:
                continue
            seen.add(bib)
            results.athletes.append(
                Athlete(
                    bib=bib,
                    name=_text(cells.get(roles.get("name"))),
                    team=_text(cells.get(roles.get("team"))),
                    category=str(row.get("group") or group),
                )
            )
            written = _text(cells.get(roles.get("result"))).strip()
            value = parse_value(written)
            status = str(row.get("status") or "").strip().lower()
            if value is not None and status not in _NOT_A_RESULT:
                results.values[bib] = value
                results.texts[bib] = written
    return results
