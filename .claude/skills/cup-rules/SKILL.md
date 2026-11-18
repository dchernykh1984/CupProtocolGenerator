---
name: cup-rules
description: Turn a cup's regulations into stage rules and a cup rule in app/rules.py. Use when the maintainer sends regulations, a points table, a tie-break, or asks how a stage or the cup is counted.
---

# Cup rules

## Where the regulations live

The maintainer sends the regulations of a cup and of each stage to the agent working in
this repository. Keep them in `docs/regulations/<cup-slug>/` as `.txt` or `.pdf` -- the
ASCII hook checks markdown, and regulations are usually in Russian. Next to them keep a
`decisions.txt`: every question you asked about them, with the maintainer's answer and
its date.

## How a rule plugs in

Both kinds live in `app/rules.py` and are picked from drop-downs:

- A **stage rule** (`StageRule`) turns one category's results of one stage into scores:
  `score(values: dict[bib, result]) -> dict[bib, StageScore(place, points)]`. A bib
  with no result is absent from `values` and must be absent from the answer.
- A **cup rule** (`CupRule`) adds the stages up within one category:
  `combine(stages: list[dict[bib, StageScore]], bibs: list[str]) -> dict[bib,
  CupScore(total, place)]`, an entry for every bib in `bibs`; `place=None` for somebody
  the rule does not rank (they are listed after the ranked).
- A stage rule whose points are the stage's time in seconds says so with
  `scores_time=True`; a cup rule that adds times up says so with `adds_times=True`. The
  pipeline then refuses a stage scored any other way, and the document writes the total
  as a time, with as many decimals as the stage results are written with.
- A rule's `key` is stored in the settings: never rename or reuse one once released.
- The stubs (`place_lower_better`, `place_higher_better`, `sum_smallest_wins`) stay
  until the maintainer says to drop them. `time` and `sum_of_times` are the
  maintainer's (`docs/regulations/sum-of-times/decisions.txt`).

## Writing one

1. Quote the paragraph of the regulations each piece comes from in the rule's
   description or a comment (translated to English, ASCII).
2. Never invent: a points table, a minimum of stages, which stages count, a tie-break,
   what happens to a DNS or a disqualification, how categories are matched across
   stages -- if the regulations do not say, ask the maintainer and record the answer
   in `decisions.txt`.
3. Tests with the rule: the regulations' own examples when they give any, ties, a
   missing stage, and one run through `pipeline.build` with a `FakeSite`.
4. The document's columns and labels follow the regulations' wording where it names
   them; the protocol document is English for now (ASCII), say so if it matters.
