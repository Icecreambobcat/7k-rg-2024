from __future__ import annotations
from abc import abstractmethod
from pathlib import Path
from App.App import Object, App
from App.Conf import Conf
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

from App.lib import Lib


class Game:
    """
    Container for ingame behaviour
    """
    STARTTIME: int = 0

    @staticmethod
    def ingame_loop(level: Level, auto: bool) -> bool:
        """
        Instantiantes own clock
        Provides multiple return states:
        False - pass
        True - fail OR quit: skip results screen and play fail graphic if fail
        """
        CLOCK = App.CLOCK
        AUDIO = Game.get_audio(level)

        STARTTIME = App.DELTA_TIME # call this as late as possible to minimise delay

        INGAME = True
        while INGAME:
            break
        else:
            return False
        return True

    @staticmethod
    def get_audio(level: Level) -> mixer.Sound:
        """
        For fetching the level audio for a level
        """

        info = level.info
        if "AudioFilename" in info:
            AUDIO = mixer.Sound(
                Path(
                    Lib.PROJECT_ROOT,
                    "Assets",
                    "Levels",
                    str(level.meta["TitleUnicode"]),
                    level.info["AudioFilename"],
                )
            )
            return AUDIO
        else:
            raise FileNotFoundError(
                "Audio file not found in level metadata:", level.meta["TitleUnicode"]
            )


class Note(Object):
    """
    Strictly only a parent class to contain TapNote and LongNote as well as common logic

    TODO: Optimise runtime overhead of loading stuff
    """

    LOADED = sprite.Group()
    ACTIVE = sprite.Group()
    PASSED = sprite.Group()

    @property
    @abstractmethod
    def time(self) -> int:
        pass

    def calc_pos(self) -> int:
        """
        note absolute time - current delta time * multiplier + constant

        TODO: Implement
        """
        out = (self.time - Game.STARTTIME) * Conf.MULTIPLIER + Conf.CONSTANT
        return out


class TapNote(Note):
    """
    tapnote logic
    """

    def __init__(self, lane: int, note_time: int) -> None:
        sprite.Sprite.__init__(self)

        self.lane = lane
        self._time = note_time

    @property
    def position(self) -> tuple[int, int]:
        return (Note.calc_pos(self), 0)  # PLACEHOLDER - CHANGE ASAP

    @property
    def image(self) -> Surface:
        return self.image

    @property
    def time(self) -> int:
        return self._time

    @time.setter
    def time(self, val: int) -> None:
        self._time = val


class LongNote(Note):
    """
    LN logic
    """

    def __init__(self, lane: int, note_time: int, note_endtime: int) -> None:
        sprite.Sprite.__init__(self)

        self.lane = lane
        self._time = note_time
        self._endtime = note_endtime

    @property
    def position(self) -> tuple[int, int]:
        return (0, 0)  # PLACEHOLDER - CHANGE ASAP

    @property
    def image(self) -> Surface:
        return self.image

    @property
    def time(self) -> int:
        return self.time

    @time.setter
    def time(self, value: int) -> None:
        self._time = value

    @property
    def endtime(self) -> int:
        return self._endtime

    @endtime.setter
    def _endtime(self, value: int) -> None:
        self._endtime = value


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
