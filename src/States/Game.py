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
    @staticmethod
    def ingame_loop() -> None:
        pass


class Note(Object):
    """
    The note parent class contains both tap notes and LNs that should be loaded to memory at runtime

    TODO: Optimise runtime overhead of loading stuff
    """

    @staticmethod
    def calc_pos() -> int:
        """
        note absolute time - current delta time * multiplier + constant

        TODO: Implement
        """
        return 0


class TapNote(Note):
    """
    tapnote logic
    """

    def __init__(self, lane, time) -> None:
        self.lane = lane
        self.time = time

    @property
    def position(self) -> tuple[int, int]:
        return (0, 0)  # PLACEHOLDER - CHANGE ASAP


class LongNote(Note):
    """
    LN logic
    """

    def __init__(self) -> None:
        pass

    @property
    def position(self) -> tuple[int, int]:
        return (0, 0)  # PLACEHOLDER - CHANGE ASAP


class Level:
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

                    case line if "[Editor]" in line:
                        section = "Editor"
                        continue

                    case line if "[Events]" in line:
                        section = "Events"
                        continue

                    case _:
                        if line:
                            pass
                        else:
                            section = ""
                            continue

                if section == "Editor" or section == "Events":
                    continue

                elif section == "General":
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
                    pass

        return out

    def __init__(self, path: Path) -> None:
        self.data = Level.parse_meta(path)
        self.notes: list[list[str]] = self.data["H"]
        self.tpoints: list[list[str]] = self.data["T"]
        self.meta: dict[str, str | list[str]] = self.data["M"]
        self.info: dict[str, str] = self.data["G"]
        self.diff: dict[str, str] = self.data["D"]
