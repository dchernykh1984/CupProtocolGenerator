"""The cup's protocol as the cycling site's structured document, schema 1.

One table per category: place, bib, name, team when anybody has one, a column per stage
(the result as its source wrote it, the stage place under it) and the cup's total, a
time when the cup adds times up, as precise as the stage results are written. The
site draws it in its own look; ``tests/fixtures/protocol-document-v1.json`` is the
site's schema.
"""

from __future__ import annotations

from typing import Any

from app.results import format_time, fraction_digits
from app.scoring import CupRow

SCHEMA_VERSION = 1
GENERATOR = "CupProtocolGenerator"


def format_number(value: float) -> str:
    """A number as a person would write it: ``12`` rather than ``12.0``."""
    return str(int(value)) if value == int(value) else f"{value:g}"


def stage_column(index: int) -> str:
    """The column id of stage ``index`` (0-based): a stage's name may be any text."""
    return f"stage_{index + 1}"


def _columns(stages: list[str], with_team: bool) -> list[dict[str, Any]]:
    columns: list[dict[str, Any]] = [
        {"id": "place", "label": "Place", "role": "place"},
        {"id": "bib", "label": "Bib", "role": "bib"},
        {"id": "name", "label": "Name", "role": "name"},
    ]
    if with_team:
        columns.append({"id": "team", "label": "Team", "role": "team"})
    columns += [
        {"id": stage_column(i), "label": name, "align": "right"}
        for i, name in enumerate(stages)
    ]
    columns.append({"id": "total", "label": "Total", "role": "result"})
    return columns


def _total(row: CupRow, texts: list[dict[str, str]], is_time: bool) -> str:
    if row.total is None:
        return ""
    if not is_time:
        return format_number(row.total)
    digits = (fraction_digits(stage.get(row.athlete.bib, "")) for stage in texts)
    return format_time(row.total, max(digits, default=0))


def _row(
    row: CupRow, texts: list[dict[str, str]], with_team: bool, total_is_time: bool
) -> dict[str, Any]:
    athlete = row.athlete
    cells: dict[str, Any] = {
        "place": "" if row.place is None else str(row.place),
        "bib": athlete.bib,
        "name": athlete.name,
    }
    if with_team:
        cells["team"] = athlete.team
    for index, score in enumerate(row.stages):
        if score is None:
            cells[stage_column(index)] = ""
            continue
        written = texts[index].get(athlete.bib) or format_number(score.points)
        cells[stage_column(index)] = {"text": written, "sub": [f"{score.place} pl."]}
    cells["total"] = _total(row, texts, total_is_time)
    return {"cells": cells}


def build(
    title: str,
    stages: list[str],
    table: dict[str, list[CupRow]],
    categories: dict[str, str],
    texts: list[dict[str, str]],
    total_is_time: bool = False,
) -> dict[str, Any]:
    """The document for ``table`` (category -> standing). ``stages`` names the stages
    in order, ``texts`` keeps each stage's results as their source wrote them,
    ``categories`` names the categories (group id -> label), and ``total_is_time``
    says the totals are seconds to write as times."""
    with_team = any(row.athlete.team for rows in table.values() for row in rows)
    columns = _columns(stages, with_team)
    sections: list[dict[str, Any]] = []
    groups: list[dict[str, str]] = []
    for category, rows in table.items():
        section: dict[str, Any] = {
            "columns": columns,
            "rows": [_row(row, texts, with_team, total_is_time) for row in rows],
        }
        if category:
            label = categories.get(category, category)
            section.update(title=label, group=category)
            groups.append({"id": category, "label": label})
        sections.append(section)
    document: dict[str, Any] = {
        "schema": SCHEMA_VERSION,
        "generator": {"name": GENERATOR},
        "sections": sections,
    }
    if title.strip():
        document["title"] = title.strip()
    if groups:
        document["groups"] = groups
    return document
