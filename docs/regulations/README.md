# Regulations

The regulations of each cup and of its stages, as the maintainer sends them, one folder
per cup: `docs/regulations/<cup-slug>/`.

- Keep them as `.txt` or `.pdf`: they are usually in Russian, and the ASCII hook checks
  markdown.
- Keep a `decisions.txt` beside them: every question the regulations left open, the
  maintainer's answer, and its date.
- They become stage rules and cup rules in `app/rules.py` (the cup-rules skill).
