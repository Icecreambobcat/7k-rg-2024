from ..App.App import Object
import pygame as pg
from pygame import font, mixer, surface, time, display, event, key, image, mouse
from typing import (
    List,
    Dict,
    Any,
    Union,
    Optional,
    Tuple,
    Type,
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
    def position(self) -> Tuple[int, int]:
        return (self.lane, self.time)

    @property
    def textures(self) -> dict[str, surface.Surface]:
        return {
            "tap": image.load("tap.png"),
            "ln": image.load("ln.png"),
            "lnBody": image.load("lnBody.png"),
            "lnEnd": image.load("lnEnd.png"),
        }
