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


class Menu:
    """
    Menu loop & logic
    """

    @staticmethod
    def menu_loop() -> bool:
        MENU = True
        CLOCK = App.CLOCK
        while MENU:
            break
        else:
            return False
        return True
