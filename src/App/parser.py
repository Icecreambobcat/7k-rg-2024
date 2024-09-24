from __future__ import annotations
from typing import Any
from States.Game import Level
from lib import Lib
from pathlib import Path


def level_load() -> dict[str, Level]:
    out = dict()
    dir = Path(f"{Lib.PROJECT_ROOT}/Assets/Levels")
    for file in dir.iterdir():
        for diff in file.iterdir():
            if diff.name.endswith(".osu"):
                level = Level(diff)
                out[f"{level.meta["TitleUnicode"]} | {level.meta["Version"]}"] = level
    return out
