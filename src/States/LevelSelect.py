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


class LevelSelect:
    def __init__(self) -> None:
        pass


class Player(Object):
    """
    The player class is used for the song select screen to fulfill the requirement of a movable player
    Probably gonna implement specific movement reading here but could also do it somewhere else

    Might move into levelselect class
    """

    def __init__(self) -> None:
        self.x = 0
        self.y = 0

    @property
    def gamestates(self) -> list[str]:
        return ["levelSelect"]

    @property
    def position(self) -> Tuple[int, int]:
        return (self.x, self.y)

    @property
    def textures(self) -> dict[str, surface.Surface]:
        return {"player": image.load("player.png")}
