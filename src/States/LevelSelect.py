from __future__ import annotations
from App.App import App, Object, AudioWrapper
import pygame as pg
from pygame import (
    Rect,
    font,
    mixer,
    surface,
    time,
    display,
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

from App.Conf import Conf
from States.Game import Level_FILE


class LevelSelect:
    """
    The level select screen is defined by this class
    Interactions of the player and level as well as player bounds should be defined here
    The structure of the screen should be imported from conf
    """

    @staticmethod
    def level_select_loop() -> bool:
        """
        return true to go back to the main menu
        """
        selected: str = ""
        BG = image.load(Conf.LEVELSELECT_BG)
        BG = transform.scale(BG, (1920, 1080))
        QUIT = False

        SELECT = True
        CLOCK = App.CLOCK

        def draw_ui() -> None:
            """
            Draws the background and individual songs according to App.LEVELS.keys()[0] and creates a dropdown/alternative menu for App.LEVELS.keys()[1]
            """
            App.SCREEN.blit(BG, (0, 0))

        while SELECT:
            if False:
                SELECT = False  # trigger this once the level is selected

            for event in pg.event.get(pg.KEYDOWN):
                if event.key == pg.K_ESCAPE:
                    QUIT = True

            if QUIT:
                break

            display.flip()
            CLOCK.tick_busy_loop(120)

        else:
            if selected is not "":
                for l in App.LEVELS.keys():
                    if selected == l[1]:
                        App.CURRENT_LEVEL = App.LEVELS[l]
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

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value


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
    def position(self) -> tuple[int, int]:
        return (self.x, self.y)

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value
