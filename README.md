# CupProtocolGenerator

A desktop tool in the offline-referee family that adds up a cup: it reads the results of
every stage -- a protocol published on the cycling site, or a Google Forms response sheet
-- scores each stage by its rule, combines the stages by the cup's rule, and publishes
the cup's protocol to the site.

Sibling tools: FinishProtocolGeneratorPython (chip timing), StartProtocolMakerPython,
StravaProtocolGenerator.

## Before the cup

1. **Stages on the site.** Publish every stage protocol from the timing software with the
   protocol format "HTML + data": this tool reads the data, not the HTML. In the section
   you name it takes the group protocol (it carries the categories), else the absolute
   one. Athletes -- bibs, names, teams, categories -- come from these protocols, the
   first stage that lists somebody naming them. In a lap race only riders with as many
   laps as their category's leader count, so show the lap times in the protocol and, for
   a live race, keep "Print DNF" on (its default): a rider still on course is listed as
   DNF, and the cup compares laps with him; untick "Only riders with their leader's laps"
   for a Number of Tries stage, whose attempts fill the lap columns.
2. **Stages from Google Forms** (an exercise of an all-round event, a result taken at the
   venue): one form per stage, two questions in this order -- the bib, then the result (a
   number). Link the form to a response sheet and share the sheet as "Anyone with the
   link: Viewer", or publish it to the web and give its published link. Do not collect
   e-mail addresses: anyone with the link sees the sheet. The last answer for a bib that
   is a number or a time counts, so a judge corrects a mark by sending the form again; an
   answer that is neither replaces nothing. Each such answer, and every answer replaced,
   is named in the log as an error, so a mark given twice is seen.
3. **A section for the cup's protocol**: add it on the cup event's "Protocol sections"
   page on the site; the tool publishes into it by its number.

## In the window

- **Cup tab** - the site, the cup event's upload token, the protocol's title (the
  event's title when left empty), the cup rule, the section to publish to, Final for
  the last upload (the site then stops checking for updates), and Place everybody for
  a broadcast (who missed a stage is placed too: after everybody with every stage, and
  the more stages missed, the lower). **Build** reads every stage again and lists what
  it could not read, each such line marked `ERROR:`, in the **Log** tab, the Cup tab's
  status line saying how many there were; **Publish** sends what was just built, and
  asks for a new build after any change.
- **Stages tab** - a tab per stage: its name, where its results come from (a protocol on
  the site, by the stage event's upload token -- the cup event's when left empty -- and
  its section, with the laps checkbox; or a Google Forms sheet, by its link) and the
  stage rule. Add a copy of the current stage to its left or right, or delete it.

A cup of summed times: score every stage by "Time, the lowest first" and pick the cup
rule "Sum of the stages' times, the smallest wins". A cup of summed places: score every
stage by "Place, the lower result the better" (a time) or "Place, the higher result the
better" (a count) and pick "Sum of the stages' points, the smallest wins". A cup of
summed results: score every stage by "Result as points, the higher the better" and pick
"Sum of the stages' points, the largest wins". A stage and a cup rule that do not go
together are refused with the rule to pick. The protocol shows every stage's result and
its place, each in a column of its own, and the total; somebody without a result in a
stage is listed after the ranked without a place, who missed fewer stages first --
unless Place everybody is ticked. The settings, upload tokens included, are kept in
`data/config.json` next to the app: keep it to yourself.

## Development

```
uv sync
uv run pre-commit install --hook-type pre-commit --hook-type commit-msg
uv run pytest
```

Pull requests run the hooks, the tests, a dependency audit and a smoke build for Linux;
release-please's own pull request builds every platform. A release builds the portable
app for Linux, Windows and macOS and attaches it to the GitHub release, and the run fails
if a platform's download is missing. Every week `runner-labels.yml` checks that GitHub
still runs each runner image the release builds on. `CLAUDE.md` (and its copy
`AGENTS.md`) and the skills in `.claude/skills` (copied to `.agents/skills`) tell a
coding agent how this repository works.
