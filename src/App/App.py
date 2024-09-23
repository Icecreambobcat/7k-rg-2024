from __future__ import annotations  # Required for forward references
from pathlib import Path
from typing import (
    Any,
)

# from collections.abc import Iterable
# Add more as needed

from abc import ABC, abstractmethod  # Required for abstract classes

import os

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

from App.lib import Lib
from States.Menu import Menu
from States.Game import Game
from States.LevelSelect import LevelSelect
from States.Results import Results

from Conf import Conf


class App:
    """
    The app class handles the game instance itself, being instantiated once and being the top-level class for this game
    """

    def __init__(self, log) -> None:
        pg.init()
        self.screen = Screen()
        self.audio = AudioWrapper()
        self.clock = time.Clock()
        self.log = log

        display.set_mode(
            size=(Conf.SCREEN_SIZE[0], Conf.SCREEN_SIZE[1]), flags=pg.FULLSCREEN
        )
        display.set_caption("GAME TITLE")

    def run(self) -> None:
        GAME = True
        while GAME:
            self.clock.tick_busy_loop(90)
            break
        pass  # Continue implementation with game loop & consider moving specific gamestate objects to their respective gamestate files


class Screen:
    """
    Rendering implementation
    A list of objects should be passed to the render method
    yet to implement checks for whether something should be rendered
    either check somewhere else or implement here
    """

    def __init__(self) -> None:
        self.screen = Surface((Conf.SCREEN_SIZE[0], Conf.SCREEN_SIZE[1]))
        pass

    def render(self, objects: list[Object]) -> None:
        # for obj in objects:
        #     self.screen.blit(obj.tex, obj.rect, obj.rect)
        pass


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
        mixer.init()
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
        pass



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
