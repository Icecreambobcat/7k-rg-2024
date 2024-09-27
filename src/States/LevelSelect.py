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

from App.Conf import Conf
from App.lib import Lib
from States.Game import Level_FILE


class LevelSelect:
    """
    The level select screen is defined by this class
    Interactions of the player and level as well as player bounds should be defined here
    The structure of the screen should be imported from conf
    """

    @staticmethod
    def level_select_loop() -> bool:
        """
        return true to go back to the main menu
        """
        selected: str = ""
        BG = image.load(Conf.LEVELSELECT_BG)
        BG = transform.scale(BG, (1920, 1080))
        QUIT = False

        SELECT = True
        CLOCK = App.CLOCK

        SONG_LIST: list[LevelObj] = list()
        for level in App.LEVELS.values():
            SONG_LIST.append(LevelObj(level))

        SONG_LIST[0].selected = True
        index = 0

        def draw_ui() -> None:
            """
            Draws the background and individual songs according to App.LEVELS.keys()[0] and creates a dropdown/alternative menu for App.LEVELS.keys()[1]
            """
            App.SCREEN.blit(BG, (0, 0))
            row = 0
            for song in SONG_LIST:
                if song.selected:
                    text = App.FONT24.render(
                        f"> {song.level.info["TitleUnicode"]} | {song.level.meta["Version"]}",
                        True,
                        (255, 255, 51),
                    )
                text = App.FONT24.render(
                    f"  {song.level.info["TitleUnicode"]} | {song.level.meta["Version"]}",
                    True,
                    (255, 255, 255),
                )
                prompt = App.FONT32.render(
                    "Select with the arrow keys, press enter to start. Toggle autoplay with space.",
                    True,
                    (255, 255, 255),
                )
                auto = App.FONT24.render(
                    "AUTOPLAY: " + ("ON" if App.AUTO else "OFF"),
                    True,
                    (255, 155, 155),
                )
                App.SCREEN.blit(prompt, (400, 100))
                App.SCREEN.blit(text, (400, row * 40 + 200))
                App.SCREEN.blit(auto, (400, 150))
                row += 1

        while SELECT:
            draw_ui()
            for event in pg.event.get(pg.KEYDOWN):
                if event.key == pg.K_RETURN:
                    SELECT = False
                elif event.key == pg.K_UP and index > 0:
                    SONG_LIST[index].selected = False
                    SONG_LIST[index - 1].selected = True
                    index -= 1
                elif event.key == pg.K_DOWN and index < len(SONG_LIST) - 1:
                    SONG_LIST[index].selected = False
                    SONG_LIST[index + 1].selected = True
                    index += 1
                elif event.key == pg.K_SPACE:
                    App.AUTO = not App.AUTO
                elif event.key == pg.K_ESCAPE:
                    QUIT = True

            if QUIT:
                break

            display.flip()
            CLOCK.tick_busy_loop(120)

        else:
            App.CURRENT_LEVEL = SONG_LIST[index].level
            return False
        return True


class LevelObj(Object):
    """
    The levelobj class is used for the song select screen to fulfill the requirement of a selectable level
    Levels are read from the parser and then loaded as levels to be rendered in a predefined order
    Functionally speaking this is also the enemy object

    This class is the graphical representation of selectable songs
    """

    def __init__(self, level: Level_FILE) -> None:
        sprite.Sprite.__init__(self)

        self.level = level
        self.selected = False

    @property
    def position(self) -> tuple[int, int]:
        return (0, 0)

    @property
    def image(self):
        img = transform.scale(image.load(Lib.GET_SONG_IMG(self.level)), (300, 300))
        return img

    @property
    def rect(self) -> Rect:
        return self.image.get_rect()
