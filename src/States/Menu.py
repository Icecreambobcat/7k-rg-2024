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


class Menu:
    """
    Menu loop & logic
    """

    @staticmethod
    def menu_loop() -> bool:
        """
        Return true to quit
        """

        def render_ui() -> None:
            pass

        MENU = True
        CLOCK = App.CLOCK
        while MENU:
            display.flip()
            CLOCK.tick_busy_loop(120)
            break
        else:
            return False
        return True
