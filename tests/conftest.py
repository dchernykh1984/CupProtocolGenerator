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


@pytest.fixture
def stage_document() -> dict[str, Any]:
    return stage_protocol()
