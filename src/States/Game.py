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
    Union,
    Optional,
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
    def parse_meta(path: Path) -> dict[str, str | list]:
        out = dict()
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
                        out["TimingPoints"] = []
                        continue

                    case line if "[HitObjects]" in line:
                        section = "Hitobjects"
                        out["HitObjects"] = []
                        continue

                    case _:
                        if line:
                            pass
                        else:
                            section = ""
                            continue

                if section == "General":
                    pair = line.replace(" ", "").split(":")
                    out[pair[0]] = pair[1]

                elif section == "Metadata":
                    pair = line.split(":")
                    if pair[0] == "Tags":
                        out[pair[0]] = pair[1].split(" ")
                        continue
                    out[pair[0]] = pair[1]

                elif section == "Difficulty":
                    pair = line.split(":")
                    out[pair[0]] = pair[1]

                elif section == "TimingPoints":
                    point = line.split(",")
                    out["TimingPoints"].append(point)

                elif section == "Hitobjects":
                    obj = line.split(",")
                    out["HitObjects"].append(obj)

                else:
                    pass  # ignore file header

        return out

    def __init__(self, path: Path) -> None:
        pass
