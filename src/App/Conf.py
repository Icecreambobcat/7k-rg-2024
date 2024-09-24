from __future__ import annotations
from pathlib import Path
from pickle import dump, load
from lib import Lib


class Conf:
    """
    Handles fixed methods and values passed to the app at runtime
    """

    """
    Fixed configs for the app
    These may be overridden in future when saves are implemented
    """
    VERSION = "0.1.0 Dev"
    WINDOW = {"PLACEHOLDER": "PLACEHOLDER"}
    KEYS = {"PLACEHOLDER": "PLACEHOLDER"}
    DEFAULTS = {"PLACEHOLDER": "PLACEHOLDER"}
    SCREEN_SIZE: tuple = (1920, 1080)

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
