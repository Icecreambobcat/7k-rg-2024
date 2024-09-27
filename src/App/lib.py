from __future__ import annotations
from pathlib import Path


class Lib:
    @staticmethod
    def GET_ROOT() -> Path:
        cwd = Path.cwd()
        return cwd

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
