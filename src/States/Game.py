from ..App.App import Object
import pygame as pg
from pygame import Rect, font, mixer, time, display, event, key, image, mouse, Surface
from typing import (
    Any,
    Union,
    Optional,
)


class Game:
    def __init__(self) -> None:
        pass


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
        return ["game"]

    @property
    def position(self) -> tuple[int, int]:
        return (self.lane, self.time)

    @property
    def tex(self) -> dict[str, Surface]:
        return {
            "tap": image.load("tap.png"),
            "ln": image.load("ln.png"),
            "lnBody": image.load("lnBody.png"),
            "lnEnd": image.load("lnEnd.png"),
        }
