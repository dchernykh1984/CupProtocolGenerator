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


def test_the_stub_stage_rules_score_a_place_as_its_points():
    times = stage_rule("place_lower_better").score({"7": 8.4, "12": 8.9})
    counts = stage_rule("place_higher_better").score({"7": 10, "12": 12})
    assert times == {"7": StageScore(1, 1.0), "12": StageScore(2, 2.0)}
    assert counts == {"12": StageScore(1, 1.0), "7": StageScore(2, 2.0)}


def test_the_stub_cup_rule_adds_up_points_and_ranks_only_complete_athletes():
    stages = [
        {"1": StageScore(1, 1), "2": StageScore(2, 2), "3": StageScore(3, 3)},
        {"1": StageScore(3, 3), "2": StageScore(1, 1)},
    ]
    assert cup_rule("sum_smallest_wins").combine(stages, ["1", "2", "3"]) == {
        "1": CupScore(4, 2),
        "2": CupScore(3, 1),
        "3": CupScore(None, None),
    }


@pytest.mark.parametrize("lookup", [stage_rule, cup_rule])
def test_an_unknown_key_is_refused(lookup):
    with pytest.raises(KeyError):
        lookup("no-such-rule")
