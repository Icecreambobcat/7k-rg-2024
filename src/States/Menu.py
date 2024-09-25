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


class Menu:
    """
    Menu loop & logic
    """

    @staticmethod
    def menu_loop() -> bool:
        """
        Return true to quit
        """
        MENU = True
        CLOCK = App.CLOCK
        while MENU:
            CLOCK.tick_busy_loop(120)
            break
        else:
            return False
        return True
