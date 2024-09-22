from typing import Any, Union, Optional
from States.Game import Level
from lib import Lib
from pathlib import Path
import os


def level_load(file) -> dict[str, Level]:
    out = dict()
    dir = Path(f"{Lib.GET_ROOT()}/Assets/Levels")
    for file in dir.iterdir():
        out[file.name] = Level(file)
    return out
