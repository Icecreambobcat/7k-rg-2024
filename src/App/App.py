from __future__ import annotations  # Required for forward references
from pathlib import Path
import sys
from typing import (
    Any,
)

from abc import ABC, abstractmethod  # Required for abstract classes

import os

import pygame as pg
from pygame import (
    Rect,
    font,
    mixer,
    rect,
    time,
    display,
    event,
    key,
    image,
    mouse,
    Surface,
    sprite,
)

from App import parser
from App.lib import Lib
from States.Menu import Menu
from States.Game import Game
from States.LevelSelect import LevelSelect
from States.Results import Results

from Conf import Conf


class App:
    """
    Isolates the game instance
    Should only be instantiated once
    """

    @staticmethod
    def quit_app() -> None:
        """
        Calls cleanup and save functions before quitting
        """
        sys.exit(0)

    LEVELS = parser.level_load()
    LOGFILE = Path(Lib.PROJECT_ROOT, "STO", "LOG", "log")

    def __init__(self, log) -> None:
        pg.init()
        self.Screen = display.set_mode(
            size=(Conf.SCREEN_SIZE[0], Conf.SCREEN_SIZE[1]), flags=pg.FULLSCREEN
        )
        self.Audio = AudioWrapper
        self.Clock = time.Clock()
        self.LOG = log

        display.set_caption("7/4k rg 0.1.0")

    def run(self) -> None:
        """
        Isolated instance initiation
        """
        GAME = True
        while GAME:
            self.Clock.tick_busy_loop(60)
            break
        
        sys.exit(0)

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
        mixer.Channel.play(channel, sound)

    @staticmethod
    def pause(channel: mixer.Channel) -> None:
        mixer.Channel.pause(channel)

    @staticmethod
    def unpause(channel: mixer.Channel) -> None:
        mixer.Channel.unpause(channel)

    @staticmethod
    def stop(channel: mixer.Channel) -> None:
        mixer.Channel.stop(channel)

    @staticmethod
    def fadeout(fadeout_time: int, channel: mixer.Channel) -> None:
        mixer.Channel.fadeout(channel, fadeout_time)

    @staticmethod
    def set_volume(channel: mixer.Channel, volume: int) -> None:
        mixer.Channel.set_volume(channel, volume)


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

    @property
    @abstractmethod
    def rect(self) -> rect.Rect:
        pass
