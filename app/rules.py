"""The rules a cup is counted by: how a stage scores its results, and how the cup adds
the stages up. The referee picks them from drop-downs; they are written here, in code.

A stage's points are what the cup rule adds up: its place, its time or its result.
Points are better lower or higher, and a cup rule adds up only points that are better
the way its sum wins. A cup's own regulations add rules: one more entry in
``STAGE_RULES`` or ``CUP_RULES``, with its tests (see the cup-rules skill).
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from enum import StrEnum


class Better(StrEnum):
    """Which way a result improves."""

    LOWER = "lower"  # a time
    HIGHER = "higher"  # a count, a length, points


@dataclass(frozen=True)
class StageScore:
    place: int
    points: float  # what the cup rule adds up: the place, the time or the result


@dataclass(frozen=True)
class CupScore:
    total: float | None  # None: nothing to show, no stage counted or no place
    place: int | None  # None: this rule does not rank the athlete


# One category's results of one stage (bib -> result) -> every scored bib's score.
StageScorer = Callable[[dict[str, float]], dict[str, StageScore]]
# Every stage's scores within one category, in stage order, the category's bibs in the
# order they are listed, and whether to place everybody, those who missed stages too
# (a broadcast) -> every bib's cup score.
CupScorer = Callable[
    [list[dict[str, StageScore]], list[str], bool], dict[str, CupScore]
]


@dataclass(frozen=True)
class StageRule:
    key: str  # kept in the settings: never rename one that has been used
    label: str
    description: str
    score: StageScorer
    scores_time: bool = False  # its points are the stage's time, in seconds
    points_better: Better = Better.LOWER  # which way the points improve
    # Somebody without a result takes the first place after everybody with one.
    places_the_missing: bool = False


@dataclass(frozen=True)
class CupRule:
    key: str  # kept in the settings: never rename one that has been used
    label: str
    description: str
    combine: CupScorer
    adds_times: bool = False  # the total is a sum of times, and shown as a time
    better: Better = Better.LOWER  # which way the total wins; the stages' points too


def rank(values: dict[str, float], better: Better) -> dict[str, int]:
    """Places 1, 2, 2, 4...: equal results share a place, and the next one skips it."""
    sign = 1 if better is Better.LOWER else -1
    return _places({key: (sign * value,) for key, value in values.items()})


def _places(order: Mapping[str, tuple[float, ...]]) -> dict[str, int]:
    """Places by ``order``, the smallest first, equal ones sharing a place."""
    places: dict[str, int] = {}
    place, last = 0, None
    for index, (key, value) in enumerate(
        sorted(order.items(), key=lambda item: item[1]), start=1
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


def _result_as_points(values: dict[str, float]) -> dict[str, StageScore]:
    return {
        bib: StageScore(place, values[bib])
        for bib, place in rank(values, Better.HIGHER).items()
    }


def _minus_second_per_repetition(values: dict[str, float]) -> dict[str, StageScore]:
    return {
        bib: StageScore(place, -values[bib])
        for bib, place in rank(values, Better.HIGHER).items()
    }


def _sum(better: Better) -> CupScorer:
    """The stages' points added up, the smallest sum first or the largest."""

    def combine(
        stages: list[dict[str, StageScore]], bibs: list[str], place_everybody: bool
    ) -> dict[str, CupScore]:
        return _summed(stages, bibs, place_everybody, better)

    return combine


def _summed(
    stages: list[dict[str, StageScore]],
    bibs: list[str],
    place_everybody: bool,
    better: Better,
) -> dict[str, CupScore]:
    """The best sum first. Somebody who missed a stage is placed only when everybody
    is: after everybody who missed fewer, by the sum of the stages they have.
    """
    # The maintainer, 2026-11-19: for a broadcast "everybody is shown with a place;
    # those who missed a stage are on par, two missed behind them, three worse still"
    # (docs/regulations/sum-of-times/decisions.txt).
    missed = {bib: sum(bib not in stage for stage in stages) for bib in bibs}
    # Rounded: 10.1 + 20.2 and 10.2 + 20.1 differ by float noise, not in a place.
    totals = {
        bib: round(sum(stage[bib].points for stage in stages if bib in stage), 6)
        for bib in bibs
        if missed[bib] < len(stages)
    }
    sign = 1 if better is Better.LOWER else -1
    placed = {
        bib: (missed[bib], sign * totals.get(bib, 0.0))
        for bib in bibs
        if place_everybody or not missed[bib]
    }
    places = _places(placed)
    return {
        bib: CupScore(totals.get(bib) if bib in placed else None, places.get(bib))
        for bib in bibs
    }


STAGE_RULES: tuple[StageRule, ...] = (
    # The maintainer, 2026-11-24: a cup by the smallest sum of places, a stage's place
    # its points (docs/regulations/sum-of-places/decisions.txt).
    StageRule(
        "place_lower_better",
        "Place, the lower result the better",
        "A place by the result, a time for one: the lowest first, equal results "
        "sharing a place, somebody without a result after everybody with one. The "
        "place is the stage's points, the lower the better.",
        _place_as_points(Better.LOWER),
        places_the_missing=True,
    ),
    StageRule(
        "place_higher_better",
        "Place, the higher result the better",
        "A place by the result, a count or a length for one: the highest first, "
        "equal results sharing a place, somebody without a result after everybody "
        "with one. The place is the stage's points, the lower the better.",
        _place_as_points(Better.HIGHER),
        places_the_missing=True,
    ),
    # The maintainer, 2026-11-24: "result as points, the higher the better" (a count
    # of repetitions, say), for a cup whose largest sum wins
    # (docs/regulations/sum-of-places/decisions.txt).
    StageRule(
        "result_higher_better",
        "Result as points, the higher the better",
        "A place by the result, a count or a length for one: the highest first, "
        "equal results sharing a place. The result itself is the stage's points, the "
        "higher the better: the cup's largest sum wins.",
        _result_as_points,
        points_better=Better.HIGHER,
    ),
    # The maintainer, 2026-11-18: "the result of every stage is its time"
    # (docs/regulations/sum-of-times/decisions.txt).
    StageRule(
        "time",
        "Time, the lowest first",
        "A place by the time, the lowest first, equal times sharing a place. The "
        "time itself, in seconds, is the stage's points: the cup can add it up.",
        _time_as_points,
        scores_time=True,
    ),
    # Made up for testing (the maintainer, 2026-11-23: no all-round regulations yet, any
    # formula will do and may be deleted later).
    StageRule(
        "minus_second_per_repetition_test",
        "Minus a second per repetition (test)",
        "For testing only: a place by the count, the highest first; every repetition "
        "is a second off the cup's sum of times.",
        _minus_second_per_repetition,
        scores_time=True,
    ),
)

CUP_RULES: tuple[CupRule, ...] = (
    # The maintainer, 2026-11-24: "a cup must be countable by the smallest sum of
    # places" (docs/regulations/sum-of-places/decisions.txt).
    CupRule(
        "sum_smallest_wins",
        "Sum of the stages' points, the smallest wins",
        "The places of every stage added up, each stage scored by its place; the "
        "smallest sum wins, equal sums share a place. Somebody without a result in a "
        "stage takes the place after everybody with one, so everybody is ranked.",
        _sum(Better.LOWER),
    ),
    # The maintainer, 2026-11-24: a cup rule "the largest sum wins" beside "the
    # smallest sum wins" (docs/regulations/sum-of-places/decisions.txt).
    CupRule(
        "sum_largest_wins",
        "Sum of the stages' points, the largest wins",
        "The points of every stage added up, each stage scored by its result as "
        "points; the largest sum wins, equal sums share a place. Somebody without a "
        "result in a stage is not ranked, unless everybody is placed.",
        _sum(Better.HIGHER),
        better=Better.HIGHER,
    ),
    # The maintainer, 2026-11-18: "the cup's result is the sum of the stages' times"
    # (docs/regulations/sum-of-times/decisions.txt).
    CupRule(
        "sum_of_times",
        "Sum of the stages' times, the smallest wins",
        "Every stage's time added up; the smallest sum wins, equal sums share a "
        "place. Somebody without a time in a stage is not ranked, unless everybody "
        "is placed. Score every stage by its time.",
        _sum(Better.LOWER),
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
