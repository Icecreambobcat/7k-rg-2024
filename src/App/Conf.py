from __future__ import annotations
from pathlib import Path
from pickle import dump, load
from lib import Lib
import pygame as pg


class Conf:
    """
    Handles fixed methods and values passed to the app at runtime
    """

    """
    Fixed configs for the app
    These may be overridden in future when saves are implemented
    """
    VERSION = "0.1.0 Dev"
    KEYS = {
        "lane0": "s",
        "lane1": "d",
        "lane2": "f",
        "lane3": " ",
        "lane4": "j",
        "lane5": "k",
        "lane6": "l",
    }
    SCREEN_SIZE: tuple = (1920, 1080)

    NOTE_TEX_BLUE = Path(Lib.PROJECT_ROOT, "Assets", "Images", "blue_note_tex.jpg")
    NOTE_TEX_WHITE = Path(Lib.PROJECT_ROOT, "Assets", "Images", "white_note_tex.jpg")
    # change file formats as necessary

    """
    These two handle scroll velocity
    """
    CONSTANT = 0
    MULTIPLIER = 1

    """
    Yet to be implemented
    """
    RUNTIME_CONF = None

    @staticmethod
    def loadConf():
        """Placeholder for future implementation"""
        confs = Path(Lib.PROJECT_ROOT, "STO", "conf.bin")
        with confs.open("rb") as f:
            Conf.RUNTIME_CONF = load(f)

    @staticmethod
    def saveConf():
        """Placeholder for future implementation"""
        confs = Path(Lib.PROJECT_ROOT, "STO", "conf.bin")
        with confs.open("wb") as f:
            dump(Conf.RUNTIME_CONF, f)
