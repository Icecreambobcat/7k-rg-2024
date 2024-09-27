from __future__ import annotations
import os
from pathlib import Path


class Lib:
    @staticmethod
    def GET_ROOT() -> str:
        cwd = os.getcwd()
        root = os.path.join(cwd, "..", "..")
        return root

    @staticmethod
    def GET_SONG_IMG(level) -> Path:
        return Path(
            Lib.PROJECT_ROOT,
            "Assets",
            "Levels",
            str(level.meta["TitleUnicode"]),
            level.info["Background"],
        )

    PROJECT_ROOT = GET_ROOT()
