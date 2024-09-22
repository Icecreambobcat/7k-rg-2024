from pathlib import Path
from App.App import Object
import pygame as pg
from pygame import (
    Rect,
    font,
    mixer,
    time,
    display,
    event,
    key,
    image,
    mouse,
    Surface,
    sprite,
)
from typing import (
    Any,
)


class Game:
    def __init__(self) -> None:
        pass


class Note(Object):
    """
    The note class is used for the rhythm game part of the game
    All note objects are first loaded into memory
    Then a second pass should be completed for LNs
    """

    def __init__(self, lane, time, noteType) -> None:
        sprite.Sprite.__init__(self)

        self.lane = lane
        self.time = time
        self.noteType = noteType

    @property
    def gamestates(self) -> list[str]:
        return ["game"]

    @property
    def position(self) -> tuple[int, int]:
        return (self.lane, self.time)


class Level:
    @staticmethod
    def parse_meta(path: Path) -> dict[str, Any]:
        """
        This is genuinely horrible in terms of type safety and is held together by hopes and dreams

        This function reads the .osu file and returns a dictionary containing the level data in several nested dictionaries and lists
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
                match line:
                    case line if "[General]" in line:
                        section = "General"
                        continue

                    case line if "[Metadata]" in line:
                        section = "Metadata"
                        continue

                    case line if "[Difficulty]" in line:
                        section = "Difficulty"
                        continue

                    case line if "[TimingPoints]" in line:
                        section = "TimingPoints"
                        continue

                    case line if "[HitObjects]" in line:
                        section = "HitObjects"
                        continue

                    case _:
                        if line:
                            pass
                        else:
                            section = ""
                            continue

                if section == "General":
                    pair = line.replace(" ", "").split(":")
                    General[pair[0]] = pair[1]

                elif section == "Metadata":
                    pair = line.split(":")
                    if pair[0] == "Tags":
                        Metadata[pair[0]] = pair[1].split(" ")
                        continue
                    Metadata[pair[0]] = pair[1]

                elif section == "Difficulty":
                    pair = line.split(":")
                    Difficulty[pair[0]] = pair[1]

                elif section == "TimingPoints":
                    point = line.split(",")
                    TimingPoints.append(point)

                elif section == "HitObjects":
                    obj = line.split(",")
                    HitObjects.append(obj)

                else:
                    pass  # ignore file header

        return out

    def __init__(self, path: Path) -> None:
        self.data = Level.parse_meta(path)
        self.notes: list[list[str]] = self.data["H"]
        self.tpoints: list[list[str]] = self.data["T"]
        self.meta: dict[str, str | list[str]] = self.data["M"]
        self.info: dict[str, str] = self.data["G"]
        self.diff: dict[str, str] = self.data["D"]
