---
name: shipping-a-change
description: Branch, commit, open a pull request, and drive CI to green in this repo. Use whenever you are about to commit, push, open a PR, or check CI status.
---

# Shipping a change

## Branch

- Never commit to `main`. `git fetch origin && git switch -c <type>/<slug> origin/main`.
- The working tree may hold the maintainer's local data (`data/`, holding upload
  tokens) or untracked files. Stage only files you changed (`git add <path>`), never
  `git add -A`.

## Commit

- One line, Conventional Commits: `git commit -m "type(scope): summary"`. No body, no
  `Co-Authored-By` trailer, no mention of the agent. `cz check --rev-range
  origin/main..HEAD` runs in CI, and release-please builds CHANGELOG from these
  subjects, so the type matters (`feat`/`fix` are released; `chore`/`docs`/`test`/
  `style`/`refactor` are not).
- One logical change per commit; every accepted review finding is a commit of its own.

## Before pushing

- `uv run pytest` (coverage gate 90%), `uv run ruff check .`,
  `uv run ruff format --check .`, `uv run mypy app tests`. pre-commit runs ruff, the
  ASCII check and a mypy of its own on commit, but that mypy lives in an environment
  without PySide6, where every Qt type is `Any`: only `uv run mypy app tests` checks the
  window's types, and CI's tests job runs it too.
- Every tracked file must be ASCII (the `no-non-ascii` hook covers markdown too). `uv run`
  may rewrite `uv.lock`; keep it out of feature commits with `git checkout uv.lock` unless
  the lock itself is the change.

## Pull request

- Run the 15 review cycles first (the review-cycle skill).
- `git push -u origin <branch>` then `gh pr create --base main --title "..." --body "..."`.
- The PR body says what was wrong, what changed, what is deliberately out of scope,
  what was measured, and the table of review findings. No "Generated with" line and no
  co-author footer.

## Watch CI to green

- Read the rollup, not `gh pr checks` (its per-check status lags). A check still running
  has an empty conclusion, not a null one, so look at its status too:

  ```
  gh pr view <n> --json statusCheckRollup --jq '[.statusCheckRollup[] |
    {name:(.name//.context), status:(.status//""), result:((.conclusion//"")+(.state//""))}]'
  ```

- Every check must be SUCCESS. A red check is fixed by a commit on the same branch.
- Then stop: never merge unless the maintainer asks for it in the message being
  answered. `main` takes rebase merges only.

## Releases

- A `feat` or `fix` on `main` makes release-please open its own pull request
  (`release-please--branches--main`). github-actions opens it, so its runs wait for
  approval (`action_required`). Approve them only on the maintainer's word:
  `gh api -X POST repos/<owner>/<repo>/actions/runs/<id>/approve` for each run, or the
  button on the pull request's page. That pull request builds every platform.
- Merging it tags the release, and the same run builds every platform, uploads each
  download and fails if one is missing (the `verify` job).
- A missing download is rebuilt with `gh workflow run release-please.yml --ref main -f
  tag=vX.Y.Z`. That run builds the tagged code with `main`'s workflows and uploads every
  platform again.
- A runner image GitHub switched off is cancelled with no steps and no error.
  `runner-labels.yml` asks every image in `build.yml`'s release matrix weekly; when it
  goes red, move that platform to the next image in `build.yml`.
