from __future__ import annotations
from States.Game import Level_FILE
from lib import Lib
from pathlib import Path


def level_load() -> dict[str, Level_FILE]:
    out = dict()
    dir = Path(Lib.PROJECT_ROOT, "Assets", "Levels")
    for file in dir.iterdir():
        for diff in file.iterdir():
            if diff.name.endswith(".osu"):
                level = Level_FILE(diff)
                out[f"{level.meta["TitleUnicode"]} | {level.meta["Version"]}"] = level
    return out
