# CupProtocolGenerator

A desktop tool in the offline-referee family that adds up a cup: it reads the results of
every stage -- a protocol published on the cycling site, or a Google Forms response sheet
-- scores each stage by its rule, combines the stages by the cup's rule, and publishes
the cup's protocol to the site.

Sibling tools: FinishProtocolGeneratorPython (chip timing), StartProtocolMakerPython,
StravaProtocolGenerator.

## Before the cup

1. **Stages on the site.** Publish every stage protocol from the timing software with
   the protocol format "HTML + data": this tool reads the data, not the HTML. In the
   section you name it takes the group protocol (it carries the categories), else the
   absolute one. Athletes -- bibs, names, teams, categories -- come from these
   protocols, the first stage that lists somebody naming them.
2. **Stages from Google Forms** (an exercise of an all-round event, a result taken at
   the venue): one form per stage, two questions in this order -- the bib, then the
   result (a number). Link the form to a response sheet and share the sheet as "Anyone
   with the link: Viewer". Do not collect e-mail addresses: anyone with the link sees
   the sheet. A coach who made a mistake answers again: the last answer for a bib wins.
3. **A section for the cup's protocol**: add it on the cup event's "Protocol sections"
   page on the site; the tool publishes into it by its number.

## In the window

- **Cup tab** - the site, the cup event's upload token, the protocol's title (the
  event's title when left empty), the cup rule, the section to publish to, and Final
  for the last upload (the site then stops checking for updates). **Build** reads every
  stage again and lists what it could not read; **Publish** sends what was just built,
  and asks for a new build after any change.
- **Stages tab** - a tab per stage: its name, where its results come from (a protocol on
  the site, by the stage event's upload token -- the cup event's when left empty -- and
  its section; or a Google Forms sheet, by its link) and the stage rule. Add a copy of
  the current stage to its left or right, or delete it.

The rules are stubs for now (a place per stage, the smallest sum of places wins): the
cup's regulations replace them. The settings, upload tokens included, are kept in
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
still runs each runner image the release builds on. `CLAUDE.md` (and its copy `AGENTS.md`) and the skills
in `.claude/skills` (copied to `.agents/skills`) tell a coding agent how this repository
works.
