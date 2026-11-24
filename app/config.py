"""The cup's settings and its stages, kept between runs in ``data/config.json`` next
to the app.

The file holds upload tokens, so ``data/`` stays out of git. A setting the file lacks,
or holds in a shape this build does not read, falls back to its default.
"""

from __future__ import annotations

import contextlib
import json
import shutil
from dataclasses import asdict, dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Any

from app.paths import app_path
from app.rules import CUP_RULES, STAGE_RULES
from app.site_api import DEFAULT_SITE


class Source(StrEnum):
    """Where a stage's results come from: the connectors."""

    SITE = "site"  # a protocol published on the cycling site
    SHEET = "sheet"  # a Google Forms response sheet


def config_path() -> Path:
    return app_path("data", "config.json")


@dataclass
class StageConfig:
    name: str = ""
    source: Source = Source.SITE
    token: str = ""  # the stage event's upload token; empty: the cup's own
    section: int = 1  # the stage event's protocol section, for a site protocol
    link: str = ""  # the response sheet's link, for a sheet
    rule: str = STAGE_RULES[0].key
    # A site protocol: a result counts only beside the laps of its category's leader.
    # Off for Number of Tries, whose attempts fill the columns laps fill.
    leader_laps_only: bool = True


@dataclass
class Config:
    site_url: str = DEFAULT_SITE
    token: str = ""  # the cup's event: its protocol is published there
    title: str = ""
    rule: str = CUP_RULES[0].key
    publish_section: int = 2
    final: bool = False  # a final protocol stops the site's live polling
    # A broadcast: those who missed stages are placed too, after those who missed fewer.
    place_everybody: bool = False
    stages: list[StageConfig] = field(default_factory=lambda: [StageConfig()])


def _section(value: Any, default: int) -> int:
    whole = isinstance(value, int) and not isinstance(value, bool)
    return value if whole and value >= 1 else default


def _text(data: dict[str, Any], name: str, default: str) -> str:
    value = data.get(name)
    return value if isinstance(value, str) else default


def _stage(data: Any) -> StageConfig:
    stage = StageConfig()
    if not isinstance(data, dict):
        return stage
    stage.name = _text(data, "name", stage.name)
    stage.token = _text(data, "token", stage.token)
    stage.link = _text(data, "link", stage.link)
    stage.rule = _text(data, "rule", stage.rule)
    stage.section = _section(data.get("section"), stage.section)
    stage.leader_laps_only = data.get("leader_laps_only") is not False
    if data.get("source") in Source.__members__.values():
        stage.source = Source(data["source"])
    return stage


def from_dict(data: Any) -> Config:
    """A config out of loaded JSON, every unreadable setting at its default."""
    config = Config()
    if not isinstance(data, dict):
        return config
    for name in ("site_url", "token", "title", "rule"):
        setattr(config, name, _text(data, name, getattr(config, name)))
    config.publish_section = _section(
        data.get("publish_section"), config.publish_section
    )
    config.final = data.get("final") is True
    config.place_everybody = data.get("place_everybody") is True
    stages = data.get("stages")
    if isinstance(stages, list) and stages:
        config.stages = [_stage(stage) for stage in stages]
    return config


def load(path: Path | None = None) -> tuple[Config, str]:
    """The settings and "", or the defaults and the log's error line for a file there
    that cannot be read: it is kept aside when it can be, so that no save writes over
    it; the line says when it could not, and the window then saves nothing over it."""
    path = path or config_path()
    try:
        # A file saved by Notepad starts with a byte order mark, which json refuses.
        return from_dict(json.loads(path.read_text(encoding="utf-8-sig"))), ""
    except FileNotFoundError:
        return Config(), ""  # the first run
    except (OSError, ValueError) as exc:
        aside = path.with_name(path.name + ".unreadable")
        try:
            # shortcut: a second unreadable file replaces the first one kept aside;
            # number them if a referee ever meets two.
            path.replace(aside)
        except OSError as kept:
            return Config(), (
                f"ERROR: settings not read ({exc}) nor kept aside ({kept}): nothing "
                "is saved over it; restart once it can be read"
            )
        return Config(), f"ERROR: settings not read ({exc}): kept as {aside.name}"


def save(config: Config, path: Path | None = None) -> None:
    path = path or config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(asdict(config), ensure_ascii=False, indent=2)
    # Written beside it, then put in its place: a write a full disk cuts short leaves
    # the old file whole.
    draft = path.with_name(path.name + ".tmp")
    draft.unlink(missing_ok=True)  # one a cut-short save left would keep its own mode
    draft.touch(mode=0o600)  # the tokens: its owner's alone...
    draft.write_text(text, encoding="utf-8")
    with contextlib.suppress(FileNotFoundError):
        shutil.copymode(path, draft)  # ...or as open as the file it replaces
    draft.replace(path)
