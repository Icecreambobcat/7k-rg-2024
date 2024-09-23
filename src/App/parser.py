from typing import Any, Union, Optional
from States.Game import Level
from lib import Lib
from pathlib import Path


def level_load(file: Path) -> dict[str, Level]:
    out = dict()
    dir = Path(f"{Lib.PROJECT_ROOT}/Assets/Levels")
    for file in dir.iterdir():
        out[file.name] = Level(file)
    return out
