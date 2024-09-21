from __future__ import annotations  # Required for forward references
from typing import (
    Any,
    Union,
    Optional,
)

# from collections.abc import Iterable
# Add more as needed

from abc import ABC, abstractmethod  # Required for abstract classes

import os

import pygame as pg
from pygame import Rect, font, mixer, time, display, event, key, image, mouse, Surface, sprite

from ..States.Menu import Menu
from ..States.Game import Game
from ..States.LevelSelect import LevelSelect
from ..States.Results import Results

from Conf import Conf


class App:
    """
    The app class handles the game instance itself, being instantiated once and being the top-level class for this game
    """

    def __init__(self) -> None:
        pg.init()
        self.screen = Screen()
        self.menu = Menu()
        self.game = Game()
        self.levelSelect = LevelSelect()
        self.results = Results()
        self.audio = AudioWrapper()
        self.clock = time.Clock()

        display.set_mode(
            size=(Conf.SCREEN_SIZE[0], Conf.SCREEN_SIZE[1]), flags=pg.FULLSCREEN
        )
        display.set_caption("GAME TITLE")

    def run(self) -> None:
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
    Implementation for audio & room for expansion
    All pygame audio functions should be called from here
    """

    def __init__(self) -> None:
        mixer.init()
        mixer.set_num_channels(16)

        self.bgm = mixer.Channel(0)
        self.playerFX = mixer.Channel(1)
        self.gameFX = mixer.Channel(2)

        self.lane0 = mixer.Channel(3)
        self.lane1 = mixer.Channel(4)
        self.lane2 = mixer.Channel(5)
        self.lane3 = mixer.Channel(6)
        self.lane4 = mixer.Channel(7)
        self.lane5 = mixer.Channel(8)
        self.lane6 = mixer.Channel(9)

        self.song = mixer.Channel(10)

        self.extra0 = mixer.Channel(11)
        self.extra1 = mixer.Channel(12)
        self.extra2 = mixer.Channel(13)
        self.extra3 = mixer.Channel(14)
        self.extra4 = mixer.Channel(15)

        for file in os.listdir("../../Assets/Audio/"):
            if file.endswith(".wav"):
                pass  # to be implemented...

    def play(self, channel: int, sound: mixer.Sound) -> None:
        pass


class Object(ABC, sprite.Sprite):  # Base class for all onscreen objects
    """
    Pretty self explanatory, but this should be used to construct all onscreen objects
    Might import to specific gamestate files instead and instantiate the objects there before passing them back
    """

    @property
    @abstractmethod
    def gamestatas(self) -> list[str]:
        pass

    # Defines the gamestates in which the object is visible
    @property
    @abstractmethod
    def position(self) -> tuple[int, int]:
        pass

    # Defines the position of the object WITH RESPECT TO GAMESTATE

    @property
    @abstractmethod
    def tex(self) -> dict[str, Surface]:
        pass

    # Defines a dict of textures for each object type

    @property
    @abstractmethod
    def rect(self) -> Rect:
        pass
