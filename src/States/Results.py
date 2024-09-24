from __future__ import annotations
from App.App import Object
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


class Results:
    """
    Results screen loop & logic
    """

    @staticmethod
    def results_loop() -> bool:
        RESULTS = True
        CLOCK = time.Clock()
        while RESULTS:
            break
        else: return False
        return True
