"""A stage's results out of a protocol published on the cycling site.

The protocol is the site's structured document (schema 1), as the timing generators
upload it. Its columns say what they hold by their ``role``: ``bib``, ``name``, ``team``
and ``result`` are read; a row's category is its ``group``, or its section's. Laps have
no role: they are the columns the finish protocol generator names ``lap<n>``, which in
a Number of Tries race hold the attempts.
"""

from __future__ import annotations

import re
from collections.abc import Iterator
from typing import Any

from app.results import Athlete, StageResults, normalize_bib, parse_value

# A row with one of these statuses has no result, whatever its result cell says.
_NOT_A_RESULT = {"dns", "dnf", "dsq"}
# Nor leads the laps: disqualified, or DNS -- the generator keeps the laps of a rider
# who missed the start check, and never makes him the leader.
_LEADS_NOBODY = {"dns", "dsq"}
# lap1, lap2...; lap1_s1 is a split of lap 1, not a lap.
_LAP = re.compile(r"lap\d+")


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


def read(document: dict[str, Any], leader_laps_only: bool = True) -> StageResults:
    """The athletes in the order the protocol lists them, and their valid results.

    An athlete listed twice (an absolute and a group table of one run) is read once,
    where they first appear. A row without a bib is not an athlete. With
    ``leader_laps_only`` a result counts only beside as many laps as the category's
    leader has.
    """
    results = StageResults(
        categories={
            str(group["id"]): str(group.get("label") or group["id"])
            for group in document.get("groups") or []
        }
    )
    seen: set[str] = set()
    laps: dict[str, int] = {}  # bib -> laps ridden, for every bib that may lead
    for section, group in _tables(document.get("sections") or [], ""):
        roles = _roles(section)
        if "bib" not in roles:
            continue
        lap_columns = [
            column["id"]
            for column in section.get("columns") or []
            if _LAP.fullmatch(str(column["id"]))
        ]
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
            if status not in _LEADS_NOBODY:
                laps[bib] = sum(
                    parse_value(_text(cells.get(lap))) is not None
                    for lap in lap_columns
                )
    if leader_laps_only:
        _drop_fewer_laps(results, laps)
    return results


def _drop_fewer_laps(results: StageResults, laps: dict[str, int]) -> None:
    """Keep a result only beside the laps of its category's leader: whoever has the most
    laps now, finished, on course or abandoned (both listed as DNF, laps, no result)."""
    # The maintainer, 2026-11-24: a rider has every lap or the stage does not count, so
    # a rider a lap down, ahead on time, is not ranked above the leader -- nor while the
    # leader rides on (docs/regulations/lap-races/decisions.txt).
    category = {athlete.bib: athlete.category for athlete in results.athletes}
    leader: dict[str, int] = {}
    for bib, count in laps.items():
        leader[category[bib]] = max(leader.get(category[bib], 0), count)
    for bib in list(results.values):
        if laps[bib] < leader[category[bib]]:
            del results.values[bib], results.texts[bib]
            results.fewer_laps.append(bib)
