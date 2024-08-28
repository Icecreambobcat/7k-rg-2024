from __future__ import annotations # Required for forward references
from typing import List, Dict, Any, Union, Optional, Tuple, Type # Required for forward references

from abc import ABC, abstractmethod # Required for abstract classes

from threading import Thread # Required for threading
import math 
import os
import sys 

import pygame as pg
from pygame import font, mixer, surface, time, display, event, key, image, mouse

pg.init()

class App:
    def __init__(self, launchState) -> None:
        pass


class Screen:
    def __init__(self) -> None:
        pass


class Object(ABC):
    @property
    @abstractmethod
    def type(self) -> str:
        pass


class AudioWrapper:
    def __init__(self) -> None:
        pass
