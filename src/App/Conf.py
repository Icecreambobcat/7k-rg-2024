from __future__ import annotations
from pathlib import Path
# from pickle import dump, load
from .lib import Lib


class Conf:
    """
    Handles fixed methods and values passed to the app at runtime
    """

    # Fixed configs for the app
    # These may be overridden in future when saves are implemented
    SCREEN_SIZE: tuple = (1920, 1080)

    # FWIW it's just better to hard path every image and asset rather than try to use an auto parser
    MENU_BG = Path(Lib.PROJECT_ROOT, "Assets", "Images", "MENU_BG.jpg")
    LEVELSELECT_BG = Path(Lib.PROJECT_ROOT, "Assets", "Images", "LEVELSELECT_BG.jpg")
    RESULTS_BG = Path(Lib.PROJECT_ROOT, "Assets", "Images", "RESULTS_BG.jpg")
    FONT_TEX = Path(
        Lib.PROJECT_ROOT, "Assets", "Fonts", "JetBrainsMonoNerdFont-Regular.ttf"
    )
    INGAME_BG = Path(Lib.PROJECT_ROOT, "Assets", "Images", "RG_BG.jpg")
    JUDGEMENT_LINE = Path(Lib.PROJECT_ROOT, "Assets", "Images", "judgement_line.png")
    NOTE_TEX_BLUE = Path(Lib.PROJECT_ROOT, "Assets", "Images", "blue_note_tex.png")
    NOTE_TEX_WHITE = Path(Lib.PROJECT_ROOT, "Assets", "Images", "white_note_tex.png")
    NOTE_TEX_GOLD = Path(Lib.PROJECT_ROOT, "Assets", "Images", "gold_note_tex.png")
    NOTE_TEX_BODY = Path(Lib.PROJECT_ROOT, "Assets", "Images", "note_body_tex.png")
    # NOTE_TEX_TAIL = Path(Lib.PROJECT_ROOT, "Assets", "Images", "note_tail_tex.png")
    # change file formats as necessary
    # however default textures are shipped with the game

    # These two handle scroll velocity
    CONSTANT = 950
    MULTIPLIER = 2.5

    HIT_WINDOWS = {
        "plusperfect": 30,
        "perfect": 50,
        "great": 100,
        "good": 150,
        "miss": 200,
    }

    SCORING = {
        "plusperfect": 301,
        "perfect": 300,
        "great": 100,
        "good": 50,
        "miss": 0,
    }
    #
    # """
    # Yet to be implemented
    # """
    # RUNTIME_CONF = None
    #
    # @staticmethod
    # def loadConf():
    #     """Placeholder for future implementation"""
    #     confs = Path(Lib.PROJECT_ROOT, "STO", "conf.bin")
    #     with confs.open("rb") as f:
    #         Conf.RUNTIME_CONF = load(f)
    #
    # @staticmethod
    # def saveConf():
    #     """Placeholder for future implementation"""
    #     confs = Path(Lib.PROJECT_ROOT, "STO", "conf.bin")
    #     with confs.open("wb") as f:
    #         dump(Conf.RUNTIME_CONF, f)
