from __future__ import annotations  # Required for forward references
from collections.abc import Callable
from pathlib import Path
import sys
from typing import (
    Never,
)

from abc import ABC, abstractmethod  # Required for abstract classes

import pygame as pg
from pygame import (
    font,
    mixer,
    time,
    display,
    Surface,
    sprite,
)

from .parser import Parser, Level_FILE
from .lib import Lib


class App:
    """
    Container for game methods and variables
    """

    LEVELS: dict[list[str], Level_FILE]
    CLOCK: time.Clock
    DELTA_TIME: Callable[[], int]
    DELTA_TIME = time.get_ticks
    # it's really stupid to have one callable among other constants but oh well
    # it's the cleanest way that remains type safe
    SCREEN: Surface
    STATE: str
    """
    This can be one of:
    Menu, Results, LevelSelect, Game
    """
    CURRENT_LEVEL: Level_FILE
    AUTO: bool
    FONT72: font.Font
    FONT32: font.Font
    FONT24: font.Font
    FONT12: font.Font
    RECENTSCORE: int = 0

    @staticmethod
    def init_game() -> None:
        from .Conf import Conf

        """
        init_game should be called first before calling run to set app variables
        """

        pg.init()
        App.LEVELS = Parser.level_load()
        App.CLOCK = time.Clock()
        App.SCREEN = display.set_mode(size=(Conf.SCREEN_SIZE[0], Conf.SCREEN_SIZE[1]), vsync=1)
        display.set_caption("7k rg 1.0.0")
        App.STATE = "Menu"
        App.AUTO = False
        App.FONT72 = font.Font(Conf.FONT_TEX, 72)
        App.FONT32 = font.Font(Conf.FONT_TEX, 32)
        App.FONT24 = font.Font(Conf.FONT_TEX, 24)
        App.FONT12 = font.Font(Conf.FONT_TEX, 12)

    @staticmethod
    def run() -> Never:
        from ..States.Menu import Menu
        from ..States.Game import Game
        from ..States.LevelSelect import LevelSelect
        from ..States.Results import Results

        """
        Isolation from initialisation of values
        """

        GAME = True
        while GAME:
            match App.STATE:
                case "Menu":
                    out = Menu.menu_loop()
                    if out is False:
                        App.STATE = "LevelSelect"
                    elif out is True:
                        GAME = False
                case "LevelSelect":
                    out = LevelSelect.level_select_loop()
                    if out is False:
                        App.STATE = "Game"
                    elif out is True:
                        App.STATE = "Menu"
                case "Game":
                    out = Game.ingame_loop(App.CURRENT_LEVEL)
                    if out is False:
                        App.STATE = "Results"
                    elif out is True:
                        App.STATE = "LevelSelect"
                case "Results":
                    out = Results.results_loop()
                    if out is False:
                        App.STATE = "LevelSelect"
                    elif out is True:
                        App.STATE = "Game"

            display.flip()
            App.CLOCK.tick_busy_loop(120)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                App.quit_app()
        App.quit_app()

    @staticmethod
    def quit_app(*args) -> Never:
        """
        Calls cleanup and save functions before quitting
        if errors are passed then exit with the first error passed
        """

        if len(args) == 0:
            pg.quit()
            sys.exit(0)
        else:
            pg.quit()
            sys.exit(args[0])


class AudioWrapper:
    """
    Implementation for a 16 channel audio system

    Contains methods to control audio but should not be instantiated as an object
    """

    AUDIO_FILES: dict[str, mixer.Sound] = dict()
    bgm: mixer.Channel
    playerFX: mixer.Channel
    gameFX: mixer.Channel
    lane0: mixer.Channel
    lane1: mixer.Channel
    lane2: mixer.Channel
    lane3: mixer.Channel
    lane4: mixer.Channel
    lane5: mixer.Channel
    lane6: mixer.Channel
    song: mixer.Channel
    extra0: mixer.Channel
    extra1: mixer.Channel
    extra2: mixer.Channel
    extra3: mixer.Channel
    extra4: mixer.Channel

    @staticmethod
    def init_audio() -> None:
        mixer.set_num_channels(16)

        AudioWrapper.bgm = mixer.Channel(0)
        AudioWrapper.playerFX = mixer.Channel(1)
        AudioWrapper.gameFX = mixer.Channel(2)

        AudioWrapper.lane0 = mixer.Channel(3)
        AudioWrapper.lane1 = mixer.Channel(4)
        AudioWrapper.lane2 = mixer.Channel(5)
        AudioWrapper.lane3 = mixer.Channel(6)
        AudioWrapper.lane4 = mixer.Channel(7)
        AudioWrapper.lane5 = mixer.Channel(8)
        AudioWrapper.lane6 = mixer.Channel(9)

        AudioWrapper.song = mixer.Channel(10)

        AudioWrapper.extra0 = mixer.Channel(11)
        AudioWrapper.extra1 = mixer.Channel(12)
        AudioWrapper.extra2 = mixer.Channel(13)
        AudioWrapper.extra3 = mixer.Channel(14)
        AudioWrapper.extra4 = mixer.Channel(15)

        dir = Path(Lib.PROJECT_ROOT, "Assets", "Audio")
        for file in dir.iterdir():
            if file.name.endswith((".wav", ".mp3", ".ogg", ".flac")):
                AudioWrapper.AUDIO_FILES[file.name] = mixer.Sound(file)

    @staticmethod
    def play(sound: mixer.Sound, channel: mixer.Channel) -> None:
        channel.play(sound)

    @staticmethod
    def pause(channel: mixer.Channel) -> None:
        channel.pause()

    @staticmethod
    def unpause(channel: mixer.Channel) -> None:
        channel.unpause()

    @staticmethod
    def stop(channel: mixer.Channel) -> None:
        channel.stop()

    @staticmethod
    def fadeout(fadeout_time: int, channel: mixer.Channel) -> None:
        channel.fadeout(fadeout_time)

    @staticmethod
    def set_volume(channel: mixer.Channel, volume: int) -> None:
        channel.set_volume(volume)


class Object(ABC, sprite.Sprite):  # Base class for all onscreen objects
    """
    Pretty self explanatory, but this should be used to construct all onscreen objects
    Might import to specific gamestate files instead and instantiate the objects there before passing them back
    """
    
    @property
    @abstractmethod
    def position(self) -> tuple[int, int]:
        pass

    @property
    @abstractmethod
    def image(self) -> Surface:
        pass

    # @property
    # @abstractmethod
    # def rect(self) -> rect.Rect:
    #     pass
