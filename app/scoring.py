"""The cup's standing in every category, the stages scored by their rules and added up
by the cup's rule (``app.rules``)."""

from __future__ import annotations

from dataclasses import dataclass

from app.results import Athlete
from app.rules import CupRule, StageRule, StageScore


@dataclass
class CupRow:
    athlete: Athlete
    stages: list[StageScore | None]  # in stage order; None without a result there
    total: float | None
    place: int | None


def standings(
    athletes: list[Athlete],
    stage_values: list[dict[str, float]],
    stage_rules: list[StageRule],
    rule: CupRule,
) -> dict[str, list[CupRow]]:
    """Every category's standing, the categories in the order the athletes come in.

    ``stage_values`` holds, for each stage in order, the result of every bib that has
    one; ``stage_rules`` the rule each stage is scored by. Places are given within a
    category. The ranked come first, by place -- a shared place keeping the order the
    athletes are listed in -- then everybody the cup rule did not rank, who missed
    fewer stages first.
    """
    categories: dict[str, list[Athlete]] = {}
    for athlete in athletes:
        categories.setdefault(athlete.category, []).append(athlete)
    table: dict[str, list[CupRow]] = {}
    for category, members in categories.items():
        bibs = [member.bib for member in members]
        scores = [
            stage.score({bib: values[bib] for bib in bibs if bib in values})
            for values, stage in zip(stage_values, stage_rules, strict=True)
        ]
        cup = rule.combine(scores, bibs)
        rows = [
            CupRow(
                member,
                [score.get(member.bib) for score in scores],
                cup[member.bib].total,
                cup[member.bib].place,
            )
            for member in members
        ]
        ranked = sorted((row for row in rows if row.place is not None), key=_place)
        unranked = sorted((row for row in rows if row.place is None), key=_missed)
        table[category] = ranked + unranked
    return table


def _place(row: CupRow) -> int:
    return row.place or 0


def _missed(row: CupRow) -> int:
    return row.stages.count(None)
