"""Shared test setup: Qt runs headless; a sample protocol of a stage on the site."""

from __future__ import annotations

import os
from typing import Any

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


def stage_protocol() -> dict[str, Any]:
    """A group protocol as the chip-timing generator uploads it: two categories, one of
    them nested a level deeper, and the absolute table listing everybody again."""
    columns = [
        {"id": "pl", "label": "Pl", "role": "place"},
        {"id": "no", "label": "No", "role": "bib"},
        {"id": "fio", "label": "Name", "role": "name"},
        {"id": "club", "label": "Club", "role": "team"},
        {"id": "t", "label": "Time", "role": "result"},
    ]
    boys = [
        {
            "cells": {
                "pl": "1",
                "no": "007",
                "fio": "Ivanov",
                "club": "UBT",
                "t": "8.40",
            }
        },
        {"cells": {"pl": "2", "no": "12", "fio": "Petrov", "club": "", "t": "8,90"}},
        {"cells": {"no": "13", "fio": "Sidorov", "t": "DNF"}},
    ]
    girls = [
        {"cells": {"pl": "1", "no": {"text": "21"}, "fio": "Orlova", "t": "0:09.10"}},
        {"cells": {"no": "22", "fio": "Belova", "t": "9.50"}, "status": "dns"},
        {"cells": {"fio": "nobody"}},
    ]
    return {
        "schema": 1,
        "groups": [{"id": "M10", "label": "Boys 10"}, {"id": "W10"}],
        "sections": [
            {"group": "M10", "columns": columns, "rows": boys},
            {"group": "W10", "sections": [{"columns": columns, "rows": girls}]},
            {"columns": columns, "rows": [{"cells": {"no": "7", "t": "99.0"}}]},
        ],
    }


def lap_race() -> dict[str, Any]:
    """A group protocol of a lap race as the chip-timing generator uploads it: its laps
    in columns ``lap<n>``, a split of lap 1 beside them. In M bib 2 is a lap down -- its
    third lap begun, which holds no time -- and ahead on time; in W the disqualified bib
    5 has more laps than anybody who counts."""
    columns = [
        {"id": "bib", "role": "bib"},
        {"id": "lap1", "label": "Lap 1"},
        {"id": "lap1_s1", "label": "(1 split)"},
        {"id": "lap2", "label": "Lap 2"},
        {"id": "lap3", "label": "Lap 3"},
        {"id": "result", "role": "result"},
    ]
    three = {"lap1": "14:00.0", "lap2": "14:00.0", "lap3": {"text": "14:00.0"}}
    men = [
        {"cells": {"bib": "1", **three, "result": "42:00.0"}},
        {
            "cells": {
                "bib": "2",
                "lap1": "20:00.0",
                "lap1_s1": "9:00.0",
                "lap2": "20:00.0",
                "lap3": "UNKNOWN",
                "result": "40:00.0",
            }
        },
    ]
    two = {"lap1": "16:00.0", "lap2": "16:00.0"}
    women = [
        {"cells": {"bib": "4", **two, "result": "32:00.0"}},
        {"cells": {"bib": "5", **three, "result": "42:00.0"}, "status": "dsq"},
        {"cells": {"bib": "6", **two, "result": "33:00.0"}},
    ]
    return {
        "schema": 1,
        "groups": [{"id": "M"}, {"id": "W"}],
        "sections": [
            {"group": "M", "columns": columns, "rows": men},
            {"group": "W", "columns": columns, "rows": women},
        ],
    }


@pytest.fixture
def stage_document() -> dict[str, Any]:
    return stage_protocol()
