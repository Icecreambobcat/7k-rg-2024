from __future__ import annotations
import os
from pathlib import Path

from States.Game import Level_FILE


class Lib:
    @staticmethod
    def GET_ROOT() -> str:
        cwd = os.getcwd()
        root = os.path.join(cwd, "..", "..")
        return root

    @staticmethod
    def GET_SONG_IMG(level: Level_FILE) -> Path:
        return Path(
            Lib.PROJECT_ROOT,
            "Assets",
            "Levels",
            str(level.meta["TitleUnicode"]),
            level.info["Background"],
        )

    PROJECT_ROOT = GET_ROOT()
