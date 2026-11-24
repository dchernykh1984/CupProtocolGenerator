# Working in CupProtocolGenerator

A PySide6 desktop tool in the offline-referee family. It adds up a cup: for every stage
it reads the results from a connector -- a protocol published on the cycling site, found
by an event's upload token, or a Google Forms response sheet -- scores the stage by the
stage rule picked for it, combines the stages by the cup rule, builds the site's
structured protocol document and uploads it into a protocol section of the cup's event.
An all-round event is a cup too: its exercises are its stages.

Sibling tools: FinishProtocolGeneratorPython (chip timing; it writes the stage protocols
this tool reads), StartProtocolMakerPython, StravaProtocolGenerator (the same window
layout: a Cup tab and a Stages tab with a tab per stage).

## The rules are stubs: the regulations are coming

The stage rules and the cup rule in `app/rules.py` are placeholders that make the road
from the sources to the site work end to end. The maintainer will send the real ones --
the cup's regulations and how each stage counts -- to the agent working here. They go
into `docs/regulations/` (see its README) and become entries in `STAGE_RULES` and
`CUP_RULES` with tests, by the cup-rules skill. Never invent a rule, a points table or a
tie-break: when the regulations leave something open, ask, and record the answer next
to the regulations.

One pair is real, by the maintainer's word: the stage rule `time` (a stage counts by
its time) and the cup rule `sum_of_times` (the cup by the sum of the stages' times,
written as a time). Its decisions are in `docs/regulations/sum-of-times/decisions.txt`.
The stage rule `minus_second_per_repetition_test` is made up, for testing all-round
events (the maintainer, 2026-11-23); it is not a regulation and may be deleted.

The lap rule of a stage read from the site is real too (the maintainer, 2026-11-24):
with the stage's checkbox, on by default, a rider short of his group leader's laps has no
result in that stage, before any stage rule sees it (`app/protocol_reader.py`,
`docs/regulations/lap-races/decisions.txt`). Regulations that rank lapped riders go to
the maintainer first.

## Conventions

- Talk to the maintainer in Russian; everything written into the repository is English
  and ASCII. Report plainly: the number, not how good it is.
- Ask about a concrete gap -- a line of the regulations, a case the code has to
  handle -- never about a case nobody raised. Check an issue's claims against the code
  before acting on them, all the more when somebody other than the maintainer wrote it.
- Python 3.14, everything through uv: `uv run pytest`, `uv run ruff check .`,
  `uv run mypy app tests`.
- Never commit to `main`. Branch off `origin/main`, one logical change per commit.
- Commit messages: one-line Conventional Commits, no body, no `Co-Authored-By` trailer
  and no co-author line, no mention of the agent. `cz check --rev-range origin/main..HEAD`
  runs on every PR, and release-please builds `CHANGELOG.md` from these subjects, so the
  type matters: `feat`, `fix`, `perf`, `revert` and `docs` are released (with
  `release-type: python` it lists `docs` under Documentation); `build`, `chore`, `ci`,
  `refactor`, `style` and `test` are not, unless marked breaking with `!`.
- ASCII only in tracked files (`uv.lock` and `CHANGELOG.md` are exempt; so are `.txt`
  and `.pdf` files, which is why regulations are kept as those). A pre-commit hook
  enforces it, and so do the PostToolUse guards of `.claude` and `.codex` on every edit.
- Before committing run the full gate: `uv run pytest` (coverage gate 90%),
  `uv run ruff check .`, `uv run ruff format --check .`, `uv run mypy app tests`.
  `uv run` may rewrite `uv.lock`; keep it out of feature commits with
  `git checkout uv.lock` unless the lock itself is the change.
- **Every pull request goes through 15 review cycles** before its pipeline is driven
  green, each accepted finding its own commit, the table of findings in the PR body
  (the review-cycle skill).
- **Never merge** a pull request unless the maintainer asks for it in the message being
  answered. `main` takes rebase merges only (the repository's ruleset). The maintainer's
  one standing exception: a pull request that only fixes the red pipeline a merged pull
  request left behind is driven green and merged: `gh pr merge <n> --rebase --admin`.

## How the pieces fit

`specs/app/cup-protocol.md` describes the program as it works today; a change that
alters what it describes updates it in the same pull request (`specs/README.md`).

- `app/site_api.py` - the cycling site connector: an event's id and title by its upload
  token, its protocols and one protocol's document by the same token, the upload.
  Standard library only; the opener is injectable so tests never reach the network.
- `app/protocol_reader.py` - a stage's results out of a site protocol document (columns
  by their role: `bib`, `name`, `team`, `result`; categories by `group`; laps by the
  `lap<n>` columns, a result counting only beside its category leader's laps).
- `app/sheets.py` - the Google connector: a sheet link turned into its CSV export, a
  response sheet read as bib -> result (columns by position: timestamp, bib, result; the
  last readable answer for a bib counts, every one it replaces is reported), and a
  sign-in page told apart from the results.
- `app/results.py` - what every connector hands over (`StageResults`, `Athlete`), and the
  parsing of bibs and results (numbers and times), and a sum of times written back as
  a time.
- `app/rules.py` - the stage rules and the cup rules, the referee's drop-downs.
- `app/scoring.py` - every category's cup standing, by those rules.
- `app/document.py` - the cup's protocol document, schema 1 of the cycling site
  (`tests/fixtures/protocol-document-v1.json` is the site's copy; keep it in sync).
- `app/pipeline.py` - the steps above in order, for the window and the tests.
- `app/config.py` - the cup's and the stages' settings in `data/config.json` (it holds
  upload tokens: `data/` is never committed).
- `app/main_window.py` - the window: the Cup tab, the Stages tab and the Log tab.

## What the tests cover

`app/main.py` and `app/main_window.py` are excluded from coverage (`pyproject.toml`,
`[tool.coverage.run]`), so the coverage number says nothing about the window. It is
only as good as the Qt-level tests in `tests/test_window.py`: drive the real handlers
with the network faked (`tests/test_pipeline.py`'s `FakeSite`), never the real site or
Google.

## Skills

- `shipping-a-change` - branch, commit, open the PR, watch CI to green.
- `review-cycle` - the 15 review cycles every PR goes through.
- `cup-rules` - turning a cup's regulations into stage and cup rules.
- `site-and-sheets` - the data contracts of the two connectors.
- `qt-window-tests` - how to test the PySide6 window here.
