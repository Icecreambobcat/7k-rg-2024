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
    transform,
)
from typing import (
    Any,
)


class Results:
    """
    Results screen loop & logic
    """

    @staticmethod
    def results_loop() -> bool:
        """
        False for normal true for retry
        """
        RESULTS = True
        CLOCK = App.CLOCK
        while RESULTS:
            display.flip()
            CLOCK.tick_busy_loop(120)
            break
        else:
            return False
        return True
