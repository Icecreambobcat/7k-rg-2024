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
    transform,
)
from typing import (
    Any,
)

from App.lib import Lib


class Game:
    """
    Container for ingame behaviour
    """

    START_TIME: int
    PASSED_TIME: int

    STATIC = sprite.Group()
    # Everything non rhythm game related that's still loaded
    LOADED = sprite.Group()
    # All note sprites are first loaded into this group
    ACTIVE = sprite.Group()
    # Notes that should be visible are then moved into this group
    PASSED = sprite.Group()
    # Notes should be moved here once hit and should then stop being updated and rendered

    @staticmethod
    def ingame_loop(level: Level_FILE, auto: bool) -> bool:
        """
        Instantiantes own clock
        Provides multiple return states:
        False - pass
        True - fail OR quit: skip results screen and play fail graphic if fail
        """

        def failscreen() -> None:
            """
            Should be called upon fail to display the fail graphic
            """
            pass

        CLOCK = App.CLOCK
        AUDIO = Game.get_audio(level)

        Game.START_TIME = App.DELTA_TIME()  # call right before loop for accuracy
        Game.PASSED_TIME = Game.START_TIME

        INGAME = True
        while INGAME:
            Game.PASSED_TIME = App.DELTA_TIME() - Game.START_TIME
            break
        else:
            return False
        return True

    @staticmethod
    def load_level(level: Level_FILE) -> Level_MEMORY:
        return Level_MEMORY(level)

    @staticmethod
    def get_audio(level: Level_FILE) -> mixer.Sound:
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
            App.quit_app(
                FileNotFoundError(
                    "Audio file not found in level metadata:",
                    level.meta["TitleUnicode"],
                )
            )


class Note(Object):
    """
    Strictly only a parent class to contain TapNote and LongNote as well as common logic

    TODO: Optimise runtime overhead of loading stuff
    """

    @property
    @abstractmethod
    def time(self) -> int:
        pass

    @property
    @abstractmethod
    def lane(self) -> int:
        pass

    @property
    @abstractmethod
    def state(self) -> sprite.Group:
        """
        Handles whether objects are still updated
        hits and misses are handled immediately before notes are passed here
        """
        pass

    _white_tex = None
    _blue_tex = None

    @property
    def image(self) -> Surface:
        if Note._white_tex is None:
            Note._white_tex = image.load(Conf.NOTE_TEX_WHITE)
            Note._white_tex = transform.scale(Note._white_tex, (200, 100))

        if Note._blue_tex is None:
            Note._blue_tex = image.load(Conf.NOTE_TEX_BLUE)
            Note._blue_tex = transform.scale(Note._blue_tex, (200, 100))

        return Note._white_tex if self.lane in [0, 2, 4, 6] else Note._blue_tex

    def calc_pos(self) -> int:
        out = (self.time - Game.PASSED_TIME) * Conf.MULTIPLIER + Conf.CONSTANT
        return out


class TapNote(Note):
    """
    tapnote logic
    """

    def __init__(self, lane: int, note_time: int) -> None:
        super().__init__()

        self._lane = lane
        self._time = note_time

    @property
    def position(self) -> tuple[int, int]:
        return (self.lane, self.calc_pos())

    @property
    def time(self) -> int:
        return self._time

    @property
    def lane(self) -> int:
        return self._lane

    @property
    def rect(self) -> Rect:
        return self.image.get_rect()

    @property
    def state(self) -> sprite.Group:
        return self._state

    @state.setter
    def state(self, value: sprite.Group) -> None:
        self._state = value
        self.add(value)


class LongNote(Note):
    """
    LN logic
    """

    def __init__(self, lane: int, note_time: int, note_endtime: int) -> None:
        super().__init__()

        self._lane = lane
        self._time = note_time
        self._endtime = note_endtime

    @property
    def position(self) -> tuple[int, int]:
        return (Note.calc_pos(self), self.lane)

    @property
    def time(self) -> int:
        return self._time

    @property
    def endtime(self) -> int:
        return self._endtime

    @property
    def lane(self) -> int:
        return self._lane

    @property
    def rect(self) -> Rect:
        return self.image.get_rect()

    @property
    def state(self) -> sprite.Group:
        return self._state

    @state.setter
    def state(self, value: sprite.Group) -> None:
        self._state = value
        self.add(value)

    @property
    def image_body(self) -> Surface:
        tex = image.load(Conf.NOTE_TEX_BODY)
        tex = transform.scale(tex, ((self.endtime - self.time) / 50, 100))
        return tex

    @property
    def rect_body(self) -> Rect:
        return self.image_body.get_rect()

    """
    Hold tail textures MAY be implemented for certain skins and textures
    But will not be implemented with this version as most players prefer to have them invisible

    These are commented out but are perfectly valid implementations otherwise
    """
    # @property
    # def image_tail(self) -> Surface:
    #     tex = image.load(Conf.NOTE_TEX_TAIL)
    #     tex = transform.scale(tex, (200, 100))
    #     return tex

    # @property
    # def rect_tail(self) -> Rect:
    #     return self.image_tail.get_rect()


class Level_MEMORY:
    """
    The actual object passed to the level engine at runtime
    Ensures reasonable overheads and isolates level data from loaded sprites which are more expensive
    """

    @staticmethod
    def load_notes(line: list[str]) -> Note:
        obj_type = None
        time = int(line[2])
        endtime = time
        lane = int(line[0])

        if int(line[3]) == 0:
            obj_type = TapNote
        elif int(line[3]) == 7:
            obj_type = LongNote
            endtime = int(line[5])

        if obj_type == TapNote:
            return TapNote(lane, time)
        elif obj_type == LongNote:
            return LongNote(lane, time, endtime)
        else:
            App.quit_app(FileNotFoundError("Loaded level file is of incorrect format."))

    def __init__(self, level: Level_FILE) -> None:
        """
        reads level data and removes invalid notes
        """

        note_list = [Level_MEMORY.load_notes(line) for line in level.notes]
        self.notes: list[Note] = [note for note in note_list if note is not None]
        self.meta = level.meta
        self.info = level.info


class Level_FILE:
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
        self.data = Level_FILE.parse_meta(path)
        self.notes: list[list[str]] = self.data["H"]
        self.tpoints: list[list[str]] = self.data["T"]
        self.meta: dict[str, str | list[str]] = self.data["M"]
        self.info: dict[str, str] = self.data["G"]
        self.diff: dict[str, str] = self.data["D"]
