"""From the settings to the cup's protocol, and from the protocol to the site.

``build`` reads every stage fresh, so running it again after a correction anywhere is
all a correction takes. The athletes -- bibs, names, teams, categories -- come from the
stages read from site protocols, the first stage that lists somebody naming them; a
sheet only gives results by bib. What could not be read is reported line by line, each
such line marked ``ERROR:`` as the finish protocol generator marks its own.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app import document, protocol_reader, scoring, sheets
from app.config import Config, Source, StageConfig
from app.results import Athlete, StageResults
from app.rules import CUP_RULES, STAGE_RULES, CupRule, StageRule, cup_rule, stage_rule
from app.site_api import SiteApi, SiteApiError


class PipelineError(Exception):
    """Something the protocol cannot be built without; the message says what."""


@dataclass
class Built:
    document: dict[str, Any]
    report: list[str] = field(default_factory=list)


class _Site:
    """The site within one build: each event is looked up by its token once."""

    def __init__(self, api: SiteApi) -> None:
        self.api = api
        self._events: dict[str, tuple[int, str]] = {}

    def event(self, token: str) -> tuple[int, str]:
        if token not in self._events:
            self._events[token] = self.api.competition(token)
        competition_id, title = self._events[token]
        if not competition_id:
            raise PipelineError("The site does not know this upload token")
        return competition_id, title

    def protocol(self, token: str, section: int) -> dict[str, Any]:
        """The group protocol of the event's ``section`` (it carries the categories),
        else its absolute one, as its structured document."""
        competition_id, _ = self.event(token)
        found = {
            p["protocol_type"]: p
            for p in self.api.protocols(competition_id)
            if p["section"] == section
        }
        chosen = found.get("group") or found.get("absolute")
        if chosen is None:
            raise PipelineError(f"no protocol in section {section} of its event")
        detail = self.api.protocol(chosen["id"])
        if not detail.get("document"):
            raise PipelineError(
                f"protocol {chosen['id']} has no data, only HTML: publish it with data"
            )
        return dict(detail["document"])


def _read_stage(site: _Site, config: Config, stage: StageConfig) -> StageResults:
    if stage.source is Source.SITE:
        token = stage.token.strip() or config.token.strip()
        document = site.protocol(token, stage.section)
        return protocol_reader.read(document, stage.leader_laps_only)
    if not stage.link.strip():
        raise PipelineError("no sheet link")
    text = site.api.fetch_text(sheets.export_url(stage.link))
    if sheets.looks_like_a_page(text):
        raise PipelineError(
            "Google answered with a page, not the results -- share the sheet as "
            "'Anyone with the link: Viewer'"
        )
    return sheets.read(text)


def _stages(
    site: _Site, config: Config, cup: CupRule, report: list[str]
) -> tuple[list[str], list[StageRule], list[StageResults]]:
    names: list[str] = []
    rules: list[StageRule] = []
    read: list[StageResults] = []
    for number, stage in enumerate(config.stages, start=1):
        name = stage.name.strip() or f"Stage {number}"
        try:
            rules.append(stage_rule(stage.rule))
        except KeyError:
            raise PipelineError(f"{name}: unknown rule {stage.rule!r}") from None
        # Seconds and places added up together make a total of neither.
        if cup.adds_times and not rules[-1].scores_time:
            timed = " or ".join(f'"{r.label}"' for r in STAGE_RULES if r.scores_time)
            raise PipelineError(
                f"{name}: the cup rule adds times up: score this stage by {timed}"
            )
        if rules[-1].scores_time and not cup.adds_times:
            adders = " or ".join(f'"{r.label}"' for r in CUP_RULES if r.adds_times)
            raise PipelineError(
                f"{name}: the stage counts by its time, but the cup rule does not add "
                f"times up: pick the cup rule {adders}"
            )
        try:
            results = _read_stage(site, config, stage)
        except (PipelineError, SiteApiError) as exc:
            # Several stages read the same way: the message names the one that failed.
            raise PipelineError(f"{name}: {exc}") from None
        report += [f"ERROR: {name}: {problem}" for problem in results.problems]
        report.append(f"{name}: {len(results.values)} results")
        if results.fewer_laps:
            report.append(
                f"{name}: not counted, fewer laps than their leader: "
                f"{', '.join(results.fewer_laps)}"
            )
        names.append(name)
        read.append(results)
    return names, rules, read


def _athletes(read: list[StageResults]) -> tuple[list[Athlete], dict[str, str]]:
    """Everybody the stages name, in the order they are first named."""
    athletes: dict[str, Athlete] = {}
    categories: dict[str, str] = {}
    for results in read:
        for athlete in results.athletes:
            athletes.setdefault(athlete.bib, athlete)
        for group, label in results.categories.items():
            categories.setdefault(group, label)
    return list(athletes.values()), categories


def build(config: Config, api: SiteApi) -> Built:
    if not config.token.strip():
        raise PipelineError("Enter the cup event's upload token")
    if not config.stages:
        raise PipelineError("Add a stage")
    try:
        rule = cup_rule(config.rule)
    except KeyError:
        raise PipelineError(f"Unknown cup rule {config.rule!r}") from None
    site = _Site(api)
    _, event_title = site.event(config.token.strip())
    report: list[str] = []
    names, rules, read = _stages(site, config, rule, report)
    athletes, categories = _athletes(read)
    if not athletes:
        raise PipelineError(
            "No stage names an athlete: read at least one stage from a site protocol"
        )
    known = {athlete.bib for athlete in athletes}
    for name, results in zip(names, read, strict=True):
        strangers = sorted(set(results.values) - known)
        if strangers:
            report.append(
                f"ERROR: {name}: bibs no protocol names: {', '.join(strangers)}"
            )
    values = [r.values for r in read]
    table = scoring.standings(athletes, values, rules, rule, config.place_everybody)
    title = config.title.strip() or event_title
    texts = [r.texts for r in read]
    built = document.build(
        title, names, table, categories, texts, total_is_time=rule.adds_times
    )
    return Built(built, report)


def publish(config: Config, api: SiteApi, built: Built) -> str:
    """Upload the built protocol; the site's reason to refuse its data, or ``""``."""
    return api.upload(
        config.token.strip(),
        built.document,
        section=config.publish_section,
        stage_label=config.title.strip(),
        is_live=not config.final,
    )
