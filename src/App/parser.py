from typing import Any, Union, Optional
from lib import Lib
from pathlib import Path
import os


def level_load(file) -> dict[str, object]:
    dir = Path(f"{Lib.GET_ROOT()}/Assets/Levels")
    for file in dir.iterdir():
        pass
    pass
