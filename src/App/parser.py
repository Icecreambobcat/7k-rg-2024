from __future__ import annotations
from .lib import Lib
from pathlib import Path
from typing import Any


class Parser:
    @staticmethod
    def level_load() -> dict[list[str], Level_FILE]:
        out = dict()
        dir = Path(Lib.PROJECT_ROOT, "Assets", "Levels")
        for parent_path in dir.iterdir():
            for file in parent_path.rglob("*.osu"):
                level = Level_FILE(file, parent_path)
                out[(level.meta["TitleUnicode"], level.meta["Version"])] = level
        return out


class Level_FILE:
    """
    Stores level meta
    """

    __slots__ = ("data", "notes", "tpoints", "meta", "info", "diff", "parent_path")

    @staticmethod
    def parse_meta(path: Path) -> dict[str, Any]:
        """
        Horrific type safety but gets the job done

        Reads the .osu file and returns a dictionary containing the level data in several nested dictionaries and lists
        """

        General: dict[str, str] = dict()
        Metadata: dict[str, str | list[str]] = dict()
        Difficulty: dict[str, str] = dict()
        TimingPoints: list[list[str]] = list()
        HitObjects: list[list[str]] = list()

        out = {
            "G": General,
            "M": Metadata,
            "D": Difficulty,
            "T": TimingPoints,
            "H": HitObjects,
        }

        with path.open() as level:
            meta = level.readlines()
            section = ""
            for line in meta:
                if line.strip() == "":
                    section = ""
                    continue
                if line.startswith("["):
                    section = line.strip()[1:-1]
                    continue
                if section == "General":
                    pair = line.split(":", 1)
                    out["G"][pair[0].strip()] = pair[1].strip()
                elif section == "Metadata":
                    pair = line.split(":", 1)
                    out["M"][pair[0].strip()] = pair[1].strip()
                elif section == "Difficulty":
                    pair = line.split(":", 1)
                    out["D"][pair[0].strip()] = pair[1].strip()
                elif section == "TimingPoints":
                    out["T"].append(line.split(","))
                elif section == "HitObjects":
                    out["H"].append(line.split(","))
                elif section == "Events":
                    if not line.startswith("//"):
                        out["G"]["Background"] = line.split(",")[2]

        return out

    def __init__(self, path: Path, parent: Path) -> None:
        self.data = Level_FILE.parse_meta(path)
        self.notes: list[list[str]] = self.data["H"]
        self.tpoints: list[list[str]] = self.data["T"]
        self.meta: dict[str, str | list[str]] = self.data["M"]
        self.info: dict[str, str] = self.data["G"]
        self.diff: dict[str, str] = self.data["D"]
        self.parent_path = parent
