"""What every source hands over for one stage: its athletes and their results.

A source is a connector: a protocol on the cycling site, a Google Forms response
sheet. Whatever it reads, it fills a ``StageResults``: the athletes it names (a sheet
names nobody, only bibs), every bib's result as a number to score and as it was
written to show, the categories it knows, and what it could not read. A result is
read here from its text, and a sum of times written back as a time.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

# h:mm:ss.f or m:ss.f, with a dot or a comma before the fraction.
_TIME = re.compile(r"^(?:(\d+):)?(\d{1,2}):(\d{1,2}(?:\.\d+)?)$")
_NUMBER = re.compile(r"^\d+(?:\.\d+)?$")


@dataclass(frozen=True)
class Athlete:
    bib: str
    name: str = ""
    team: str = ""
    category: str = ""  # a group id of the protocol that named them; "" for none


@dataclass
class StageResults:
    athletes: list[Athlete] = field(default_factory=list)
    values: dict[str, float] = field(default_factory=dict)  # bib -> result to score
    texts: dict[str, str] = field(default_factory=dict)  # bib -> result as written
    categories: dict[str, str] = field(default_factory=dict)  # group id -> label
    problems: list[str] = field(default_factory=list)


def normalize_bib(text: str) -> str:
    """A bib as every source agrees on it: no spaces, no leading zeros in a number, its
    letters in capitals -- a phone may well type "a7" for "A7"."""
    bib = "".join(text.split())
    # isdecimal, not isdigit: a superscript two is a digit that int() refuses.
    return str(int(bib)) if bib.isdecimal() else bib.upper()


def parse_value(text: str) -> float | None:
    """A result as a number: ``12``, ``2,35``, or a time such as ``0:08.43`` or
    ``1:02:33.4`` in seconds; None for anything else (``DNF``, a word, a minus)."""
    plain = text.strip().replace(",", ".")
    if _NUMBER.match(plain):
        return float(plain)
    time = _TIME.match(plain)
    if time is None:
        return None
    hours, minutes, seconds = time.groups()
    # A unit under a larger one stays under 60: "1:75" is no time.
    if float(seconds) >= 60 or (hours is not None and int(minutes) >= 60):
        return None
    return int(hours or 0) * 3600 + int(minutes) * 60 + float(seconds)


def fraction_digits(text: str) -> int:
    """How many digits a result is written with after its dot or comma."""
    _, dot, fraction = text.strip().replace(",", ".").rpartition(".")
    return len(fraction) if dot else 0


def format_time(seconds: float, decimals: int = 0) -> str:
    """Seconds as the timing tools write a time: ``h:mm:ss`` from an hour on, ``m:ss``
    below it, ``decimals`` digits after the dot, a minus before a negative one."""
    if seconds < 0:
        return "-" + format_time(-seconds, decimals)
    factor = 10**decimals
    whole, fraction = divmod(round(seconds * factor), factor)
    hours, rest = divmod(whole, 3600)
    minutes, secs = divmod(rest, 60)
    text = f"{hours}:{minutes:02d}:{secs:02d}" if hours else f"{minutes}:{secs:02d}"
    return f"{text}.{fraction:0{decimals}d}" if decimals else text
