from app.results import Athlete
from app.rules import StageScore, cup_rule, stage_rule
from app.scoring import standings

LOWER = stage_rule("place_lower_better")
HIGHER = stage_rule("place_higher_better")
SUM = cup_rule("sum_smallest_wins")
# A stage scored by its time leaves somebody without one unscored: he missed it.
TIME = stage_rule("time")
TIMES = cup_rule("sum_of_times")


def test_each_category_is_counted_on_its_own():
    athletes = [
        Athlete("1", "A", category="M"),
        Athlete("2", "B", category="M"),
        Athlete("3", "C", category="M"),
        Athlete("4", "D", category="W"),
    ]
    runs = {"1": 8.0, "2": 8.5, "3": 9.0, "4": 9.5}
    jumps = {"1": 150, "2": 190, "3": 160, "4": 140}
    table = standings(athletes, [runs, jumps], [LOWER, HIGHER], SUM)
    assert list(table) == ["M", "W"]
    assert [(r.athlete.bib, r.total, r.place) for r in table["M"]] == [
        ("2", 3, 1),
        ("1", 4, 2),
        ("3", 5, 3),
    ]
    assert table["M"][0].stages == [StageScore(2, 2), StageScore(1, 1)]
    assert [(r.athlete.bib, r.total, r.place) for r in table["W"]] == [("4", 2, 1)]


def test_a_shared_place_keeps_the_listing_order():
    athletes = [Athlete("9", "Late"), Athlete("1", "Early")]
    table = standings(
        athletes, [{"9": 8.0, "1": 8.5}, {"9": 150, "1": 190}], [LOWER, HIGHER], SUM
    )
    assert [(r.athlete.bib, r.place) for r in table[""]] == [("9", 1), ("1", 1)]


def test_somebody_the_cup_rule_does_not_rank_comes_last_without_a_place():
    athletes = [Athlete("9", "Missed one"), Athlete("1", "Both")]
    table = standings(
        athletes, [{"9": 7.0, "1": 8.0}, {"1": 150.0}], [TIME, TIME], TIMES
    )
    rows = table[""]
    assert [(r.athlete.bib, r.place, r.total) for r in rows] == [
        ("1", 1, 158.0),
        ("9", None, None),
    ]
    assert rows[1].stages == [StageScore(1, 7.0), None]


def test_the_unranked_are_listed_by_how_many_stages_they_missed():
    athletes = [Athlete("5", "None"), Athlete("9", "One missed"), Athlete("1", "Both")]
    table = standings(
        athletes, [{"9": 7.0, "1": 8.0}, {"1": 150.0}], [TIME, TIME], TIMES
    )
    assert [(r.athlete.bib, r.place) for r in table[""]] == [
        ("1", 1),
        ("9", None),
        ("5", None),
    ]


def test_placing_everybody_lists_who_missed_more_stages_lower():
    athletes = [Athlete("5", "None"), Athlete("9", "One missed"), Athlete("1", "Both")]
    table = standings(
        athletes, [{"9": 7.0, "1": 8.0}, {"1": 150.0}], [TIME, TIME], TIMES, True
    )
    assert [(r.athlete.bib, r.place, r.total) for r in table[""]] == [
        ("1", 1, 158.0),
        ("9", 2, 7.0),
        ("5", 3, None),
    ]


def test_a_place_stage_puts_everybody_without_a_result_first_after_the_rest():
    # 9 and 1 ran, only 1 jumped: 5 is third in the run and, with 9, second in the jump.
    athletes = [Athlete("5", "None"), Athlete("9", "Ran"), Athlete("1", "Both")]
    table = standings(
        athletes, [{"9": 7.0, "1": 8.0}, {"1": 150}], [LOWER, HIGHER], SUM
    )
    rows = table[""]
    assert [(r.athlete.bib, r.place, r.total) for r in rows] == [
        ("9", 1, 3.0),
        ("1", 1, 3.0),
        ("5", 3, 5.0),
    ]
    assert rows[2].stages == [StageScore(3, 3.0), StageScore(2, 2.0)]


def test_after_a_tie_somebody_without_a_result_takes_the_place_after_everybody():
    # 8.4, 8.9, 8.9 are 1, 2, 2: the next possible place is 4, not 3.
    athletes = [Athlete(bib, bib) for bib in ("1", "2", "3", "4")]
    table = standings(athletes, [{"1": 8.4, "2": 8.9, "3": 8.9}], [LOWER], SUM)
    places = {r.athlete.bib: r.stages[0].place for r in table[""] if r.stages[0]}
    assert places == {"1": 1, "2": 2, "3": 2, "4": 4}


def test_before_anybody_has_gone_everybody_is_first_in_every_place_stage():
    athletes = [Athlete("5", "A"), Athlete("9", "B")]
    table = standings(athletes, [{}, {"9": 12}], [LOWER, HIGHER], SUM)
    assert [(r.athlete.bib, r.stages) for r in table[""]] == [
        ("9", [StageScore(1, 1.0), StageScore(1, 1.0)]),
        ("5", [StageScore(1, 1.0), StageScore(2, 2.0)]),
    ]
