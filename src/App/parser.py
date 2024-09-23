from __future__ import annotations
from typing import Any
from States.Game import Level
from lib import Lib
from pathlib import Path


def level_load(file: Path) -> dict[str, Level]:
    out = dict()
    dir = Path(f"{Lib.PROJECT_ROOT}/Assets/Levels")
    for file in dir.iterdir():
        out[file.name] = Level(file)
    return out
