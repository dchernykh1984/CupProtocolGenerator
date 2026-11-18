"""The rules a cup is counted by: how a stage scores its results, and how the cup adds
the stages up. The referee picks them from drop-downs; they are written here, in code.

The rules below are stubs, there to make the whole road from the sources to the site
work end to end. The cup's regulations replace them: a new rule is one more entry in
``STAGE_RULES`` or ``CUP_RULES``, with its tests (see the cup-rules skill).
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum


class Better(StrEnum):
    """Which way a result improves."""

    LOWER = "lower"  # a time
    HIGHER = "higher"  # a count, a length, points


@dataclass(frozen=True)
class StageScore:
    place: int
    points: (
        float  # what the cup rule adds up; the stub rules score a place as its points
    )


@dataclass(frozen=True)
class CupScore:
    total: float | None  # None: this rule does not rank the athlete
    place: int | None


# One category's results of one stage (bib -> result) -> every scored bib's score.
StageScorer = Callable[[dict[str, float]], dict[str, StageScore]]
# Every stage's scores within one category, in stage order, and the category's bibs in
# the order they are listed -> every bib's cup score.
CupScorer = Callable[[list[dict[str, StageScore]], list[str]], dict[str, CupScore]]


@dataclass(frozen=True)
class StageRule:
    key: str  # kept in the settings: never rename one that has been used
    label: str
    description: str
    score: StageScorer
    scores_time: bool = False  # its points are the stage's time, in seconds


@dataclass(frozen=True)
class CupRule:
    key: str  # kept in the settings: never rename one that has been used
    label: str
    description: str
    combine: CupScorer
    adds_times: bool = False  # the total is a sum of times, and shown as a time


def rank(values: dict[str, float], better: Better) -> dict[str, int]:
    """Places 1, 2, 2, 4...: equal results share a place, and the next one skips it."""
    sign = 1 if better is Better.LOWER else -1
    places: dict[str, int] = {}
    place, last = 0, None
    for index, (key, value) in enumerate(
        sorted(values.items(), key=lambda item: sign * item[1]), start=1
    ):
        if value != last:
            place, last = index, value
        places[key] = place
    return places


def _place_as_points(better: Better) -> StageScorer:
    def score(values: dict[str, float]) -> dict[str, StageScore]:
        return {bib: StageScore(p, float(p)) for bib, p in rank(values, better).items()}

    return score


def _time_as_points(values: dict[str, float]) -> dict[str, StageScore]:
    return {
        bib: StageScore(place, values[bib])
        for bib, place in rank(values, Better.LOWER).items()
    }


def _sum_smallest_wins(
    stages: list[dict[str, StageScore]], bibs: list[str]
) -> dict[str, CupScore]:
    # Rounded: the order times are added in must not split equal sums by a 1e-16.
    totals = {
        bib: round(sum(stage[bib].points for stage in stages), 6)
        for bib in bibs
        if all(bib in stage for stage in stages)
    }
    places = rank(totals, Better.LOWER)
    return {bib: CupScore(totals.get(bib), places.get(bib)) for bib in bibs}


STAGE_RULES: tuple[StageRule, ...] = (
    StageRule(
        "place_lower_better",
        "Place, the lower result the better (stub)",
        "A place by the result, a time for one: the lowest first, equal results "
        "sharing a place. The place is the stage's points.",
        _place_as_points(Better.LOWER),
    ),
    StageRule(
        "place_higher_better",
        "Place, the higher result the better (stub)",
        "A place by the result, a count or a length for one: the highest first, "
        "equal results sharing a place. The place is the stage's points.",
        _place_as_points(Better.HIGHER),
    ),
    StageRule(
        "time",
        "Time, the lowest first",
        "A place by the time, the lowest first, equal times sharing a place. The "
        "time itself, in seconds, is the stage's points: the cup can add it up.",
        _time_as_points,
        scores_time=True,
    ),
)

CUP_RULES: tuple[CupRule, ...] = (
    CupRule(
        "sum_smallest_wins",
        "Sum of the stages' points, the smallest wins (stub)",
        "The points of every stage added up; the smallest sum wins, equal sums share "
        "a place. Somebody without a result in a stage is not ranked.",
        _sum_smallest_wins,
    ),
    CupRule(
        "sum_of_times",
        "Sum of the stages' times, the smallest wins",
        "Every stage's time added up; the smallest sum wins, equal sums share a "
        "place. Somebody without a time in a stage is not ranked. Score every stage "
        "by its time.",
        _sum_smallest_wins,
        adds_times=True,
    ),
)


def stage_rule(key: str) -> StageRule:
    """The stage rule with this key; KeyError for one this build does not know."""
    for rule in STAGE_RULES:
        if rule.key == key:
            return rule
    raise KeyError(key)


def cup_rule(key: str) -> CupRule:
    """The cup rule with this key; KeyError for one this build does not know."""
    for rule in CUP_RULES:
        if rule.key == key:
            return rule
    raise KeyError(key)
