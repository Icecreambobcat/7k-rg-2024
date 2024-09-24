from __future__ import annotations
from App.App import App, Object
import pygame as pg
from pygame import (
    Rect,
    font,
    mixer,
    surface,
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


class LevelSelect:
    """
    The level select screen is defined by this class
    Interactions of the player and level as well as player bounds should be defined here
    The structure of the screen should be imported from conf
    """

    @staticmethod
    def level_select_loop() -> bool:
        SELECT = True
        CLOCK = App.CLOCK

        while SELECT:
            break
        else:
            return False
        return True


class Player(Object):
    """
    The player class is used for the song select screen to fulfill the requirement of a movable player
    Probably gonna implement specific movement reading here but could also do it somewhere else
    """

    def __init__(self) -> None:
        sprite.Sprite.__init__(self)

        self.x = 0
        self.y = 0

    @property
    def position(self) -> tuple[int, int]:
        return (self.x, self.y)


class LevelObj(Object):
    """
    The levelobj class is used for the song select screen to fulfill the requirement of a selectable level
    Levels are read from the parser and then loaded as levels to be rendered in a predefined order
    Functionally speaking this is also the enemy object

    This class is the graphical representation of selectable songs
    """

    def __init__(self, x, y, level) -> None:
        sprite.Sprite.__init__(self)

        self.x = x
        self.y = y
        self.level = level

    @property
    def gamestates(self) -> list[str]:
        return ["levelSelect"]

    @property
    def position(self) -> tuple[int, int]:
        return (self.x, self.y)
