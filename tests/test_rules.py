import pytest

from app.rules import (
    CUP_RULES,
    STAGE_RULES,
    Better,
    CupScore,
    StageScore,
    cup_rule,
    rank,
    stage_rule,
)


def test_a_lower_and_a_higher_result_rank_first_equal_results_sharing_a_place():
    assert rank({"a": 8.1, "b": 7.9, "c": 8.1, "d": 9.0}, Better.LOWER) == {
        "b": 1,
        "a": 2,
        "c": 2,
        "d": 4,
    }
    assert rank({"a": 10, "b": 12, "c": 12}, Better.HIGHER) == {"b": 1, "c": 1, "a": 3}


def test_every_rule_has_its_own_key_and_says_what_it_does():
    for rules in (STAGE_RULES, CUP_RULES):
        keys = [rule.key for rule in rules]
        assert len(keys) == len(set(keys))
        assert all(rule.label and rule.description for rule in rules)


def test_the_place_rules_score_a_place_as_its_points():
    times = stage_rule("place_lower_better").score({"7": 8.4, "12": 8.9})
    counts = stage_rule("place_higher_better").score({"7": 10, "12": 12})
    assert times == {"7": StageScore(1, 1.0), "12": StageScore(2, 2.0)}
    assert counts == {"12": StageScore(1, 1.0), "7": StageScore(2, 2.0)}


def test_the_result_as_points_places_the_highest_first_and_keeps_it_as_points():
    rule = stage_rule("result_higher_better")
    assert rule.points_better is Better.HIGHER and not rule.scores_time
    assert rule.score({"7": 23, "12": 28, "3": 23}) == {
        "12": StageScore(1, 28),
        "7": StageScore(2, 23),
        "3": StageScore(2, 23),
    }


def test_the_time_rule_places_the_lowest_first_and_keeps_the_time_as_points():
    assert stage_rule("time").score({"7": 8.4, "12": 8.9, "3": 8.4}) == {
        "7": StageScore(1, 8.4),
        "3": StageScore(1, 8.4),
        "12": StageScore(3, 8.9),
    }


def test_the_test_rule_places_the_most_repetitions_first_a_second_off_each():
    rule = stage_rule("minus_second_per_repetition_test")
    assert rule.scores_time  # the cup's sum of times takes it
    assert rule.score({"7": 23, "12": 28, "3": 23}) == {
        "12": StageScore(1, -28),
        "7": StageScore(2, -23),
        "3": StageScore(2, -23),
    }


def test_the_smallest_sum_of_points_wins_and_ranks_only_complete_athletes():
    stages = [
        {"1": StageScore(1, 1), "2": StageScore(2, 2), "3": StageScore(3, 3)},
        {"1": StageScore(3, 3), "2": StageScore(1, 1)},
    ]
    assert cup_rule("sum_smallest_wins").combine(stages, ["1", "2", "3"], False) == {
        "1": CupScore(4, 2),
        "2": CupScore(3, 1),
        "3": CupScore(None, None),
    }


def test_the_largest_sum_of_points_wins_when_the_points_grow_with_the_result():
    rule = cup_rule("sum_largest_wins")
    assert rule.better is Better.HIGHER and not rule.adds_times
    stages = [
        {"1": StageScore(2, 20), "2": StageScore(1, 25), "3": StageScore(3, 10)},
        {"1": StageScore(1, 30), "2": StageScore(2, 25), "3": StageScore(3, 5)},
    ]
    assert rule.combine(stages, ["1", "2", "3"], False) == {
        "1": CupScore(50, 1),
        "2": CupScore(50, 1),
        "3": CupScore(15, 3),
    }


def test_with_everybody_placed_the_largest_sum_still_ranks_by_stages_missed_first():
    stages = [
        {"1": StageScore(1, 30), "2": StageScore(2, 10)},
        {"1": StageScore(1, 30), "3": StageScore(2, 5)},
    ]
    assert cup_rule("sum_largest_wins").combine(stages, ["1", "2", "3", "4"], True) == {
        "1": CupScore(60, 1),
        "2": CupScore(10, 2),  # one stage missed: after all who have every stage
        "3": CupScore(5, 3),
        "4": CupScore(None, 4),  # no stage at all: the last place, no total
    }


def test_the_sum_of_times_ranks_equal_sums_together_float_noise_aside():
    rule = cup_rule("sum_of_times")
    stages = [
        {"1": StageScore(1, 10.1), "2": StageScore(2, 10.2), "3": StageScore(3, 10.5)},
        {"1": StageScore(2, 20.2), "2": StageScore(1, 20.1)},
    ]
    assert rule.adds_times
    assert rule.combine(stages, ["1", "2", "3"], False) == {
        "1": CupScore(30.3, 1),  # 10.1 + 20.2 is 30.299999999999997 unrounded
        "2": CupScore(30.3, 1),
        "3": CupScore(None, None),
    }


# Six athletes over three stages: two have every stage, two missed one, one missed two,
# one missed all three.
MISSING = [
    {
        "1": StageScore(1, 10),
        "2": StageScore(2, 11),
        "3": StageScore(3, 5),
        "4": StageScore(4, 5),
        "5": StageScore(5, 1),
    },
    {"1": StageScore(1, 20), "2": StageScore(2, 21), "3": StageScore(3, 5)},
    {"1": StageScore(1, 30), "2": StageScore(2, 31), "4": StageScore(3, 5)},
]
SIX = ["6", "5", "4", "3", "2", "1"]


@pytest.mark.parametrize("key", ["sum_smallest_wins", "sum_of_times"])
def test_placing_everybody_puts_who_missed_more_stages_lower(key):
    assert cup_rule(key).combine(MISSING, SIX, True) == {
        "1": CupScore(60, 1),
        "2": CupScore(63, 2),
        "3": CupScore(10, 3),  # a smaller sum than 1's, but a stage missed
        "4": CupScore(10, 3),
        "5": CupScore(1, 5),
        "6": CupScore(None, 6),  # nothing to add up, the last place still
    }


@pytest.mark.parametrize("key", ["sum_smallest_wins", "sum_of_times"])
def test_without_placing_everybody_who_missed_a_stage_has_no_place(key):
    scores = cup_rule(key).combine(MISSING, SIX, False)
    assert {bib: score for bib, score in scores.items() if score.place} == {
        "1": CupScore(60, 1),
        "2": CupScore(63, 2),
    }
    assert {scores[bib] for bib in "3456"} == {CupScore(None, None)}


@pytest.mark.parametrize("lookup", [stage_rule, cup_rule])
def test_an_unknown_key_is_refused(lookup):
    with pytest.raises(KeyError):
        lookup("no-such-rule")
