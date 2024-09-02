from __future__ import annotations # Required for forward references
from typing import List, Dict, Any, Union, Optional, Tuple, Type # Required for forward references

from abc import ABC, abstractmethod # Required for abstract classes

from threading import Thread # Required for threading
import math 
import os
import sys 

import pygame as pg
from pygame import font, mixer, surface, time, display, event, key, image, mouse

from States.Menu import Menu
from States.Game import Game
from States.LevelSelect import LevelSelect
from States.Results import Results


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
        
    def run(self) -> None:
        pg.display.set_mode(size=(1920, 1080), flags = pg.FULLSCREEN)
        pg.display.set_caption('RG 0.1 Alpha')
        pass


class Screen:
    def __init__(self) -> None:
        pass
        
    def render(self, objects: List[Object]) -> None:
        for obj in objects:
            pass


class AudioWrapper:
    def __init__(self) -> None:
        mixer.init()
        mixer.set_num_channels(16)
        perfect = mixer.Sound('perfect.wav')
        hold = mixer.Sound('hold.wav')
        miss = mixer.Sound('miss.wav')

        bgm = mixer.Channel(0)
        playerFX = mixer.Channel(1)
        gameFX = mixer.Channel(2)

        lane1 = mixer.Channel(3)
        lane2 = mixer.Channel(4)
        lane3 = mixer.Channel(5)
        lane4 = mixer.Channel(6)
        lane5 = mixer.Channel(7)
        lane6 = mixer.Channel(8)
        lane7 = mixer.Channel(9)

        song = mixer.Channel(10)

        def play(self, channel: int, sound: mixer.Sound) -> None:
            pass


class Object(ABC): # Base class for all onscreen objects
    @property
    @abstractmethod
    def gamestates(self) -> list[str]:
        pass
    # Defines the gamestates in which the object is visible
    @property
    @abstractmethod
    def position(self) -> Tuple[int, int]:
        pass
    # Defines the position of the object WITH RESPECT TO GAMESTATE

    @property
    @abstractmethod
    def textures(self) -> dict[str, surface.Surface]:
        pass
    # Defines a dict of textures for each object type


class Note(Object):
    """
    The note class is used for the rhythm game part of the game
    All note objects are first loaded into memory
    LNs are then reparsed live in the level
    """
    def __init__(self, lane, time, noteType) -> None:
        self.lane = lane
        self.time = time
        self.noteType = noteType

    @property
    def gamestates(self) -> list[str]:
        return ['game']

    @property
    def position(self) -> Tuple[int, int]:
        return (self.lane, self.time)

    @property
    def textures(self) -> dict[str, surface.Surface]:
        return {
            'tap': image.load('tap.png'),
            'ln': image.load('ln.png'),
            'lnBody': image.load('lnBody.png'),
            'lnEnd': image.load('lnEnd.png'),
        }


class Player(Object):
    """
    The player class is used for the song select screen to fulfill the requirement of a movable player
    """
    def __init__(self) -> None:
        self.x = 0
        self.y = 0

    @property
    def gamestates(self) -> list[str]:
        return ['levelSelect']

    @property
    def position(self) -> Tuple[int, int]:
        return (self.x, self.y)

    @property
    def textures(self) -> dict[str, surface.Surface]:
        return {
            'player': image.load('player.png')
        }
