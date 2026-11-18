from app.results import Athlete
from app.rules import StageScore, cup_rule, stage_rule
from app.scoring import standings

LOWER = stage_rule("place_lower_better")
HIGHER = stage_rule("place_higher_better")
SUM = cup_rule("sum_smallest_wins")


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
        athletes, [{"9": 7.0, "1": 8.0}, {"1": 150}], [LOWER, HIGHER], SUM
    )
    rows = table[""]
    assert [(r.athlete.bib, r.place, r.total) for r in rows] == [
        ("1", 1, 3.0),
        ("9", None, None),
    ]
    assert rows[1].stages == [StageScore(1, 1), None]
