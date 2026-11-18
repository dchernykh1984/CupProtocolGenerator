---
name: review-cycle
description: The 15 review cycles every pull request goes through before its pipeline, and how their findings are landed and reported. Use before opening a PR, or when asked to review a branch or a PR.
---

# Review cycles

The maintainer's default: **every pull request gets 15 review cycles** before its
pipeline is driven green.

- A cycle reads the diff against `origin/main` as if somebody else wrote it, with a
  focus of its own. Run them in this order, then a final read of the whole diff:
  behaviour; security and privacy (tokens, what reaches the network); the connectors'
  contracts (site-and-sheets skill); tests (do they pin behaviour, not implementation,
  and would they fail without the change?); edge cases (empty input, a missing stage,
  ties, units); error handling (nothing dropped silently, every refusal says why);
  the rules against the regulations (cup-rules skill); the window (qt-window-tests
  skill); performance; naming and structure; comments and docstrings against the code;
  the agent docs (CLAUDE.md, AGENTS.md, skills) against the code; ASCII and formatting;
  the build and the workflows; the whole diff once more.
- Do not invent findings to fill a cycle: a cycle may find nothing, and says so with
  the reason.
- Every accepted finding is a commit of its own (one-line Conventional Commit), with a
  test when it is a behaviour change. Re-run the gate after each.
- A finding of medium severity or worse means at least two more cycles with fixes
  after it, even past the fifteenth.
- Put the table into the PR body and give it to the maintainer:

  | Cycle | Focus | Finding | Severity | Commit |
  | --- | --- | --- | --- | --- |

- Then drive CI to green (shipping-a-change skill) and stop: no merge without the
  maintainer's word.
