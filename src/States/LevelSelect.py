from __future__ import annotations
from ..App.App import App, Object
import pygame as pg
from pygame import (
    Rect,
    display,
    image,
    sprite,
    transform,
)

from ..App.Conf import Conf
from ..App.lib import Lib
from .Game import Level_FILE


class LevelSelect:
    """
    The level select screen is defined by this class
    Interactions of the player and level as well as player bounds should be defined here
    The structure of the screen should be imported from conf
    """

    @staticmethod
    def level_select_loop() -> bool:
        from ..App.App import AudioWrapper
        from .Game import Game
        """
        return true to go back to the main menu
        """
        BG = image.load(Conf.LEVELSELECT_BG)
        BG = transform.scale(BG, (1920, 1080))
        QUIT = False
        PREVIEW = False

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
                        f"> {song.level.meta["Title"]} | {song.level.meta["Version"]}",
                        True,
                        (255, 255, 115),
                    )
                else:
                    text = App.FONT24.render(
                        f"  {song.level.meta["Title"]} | {song.level.meta["Version"]}",
                        True,
                        (115, 215, 215),
                    )
                prompt = App.FONT32.render(
                    "Select with the arrow keys, press enter to start. Toggle autoplay with tab",
                    True,
                    (255, 255, 255),
                )
                auto = App.FONT24.render(
                    "AUTOPLAY: " + ("ON" if App.AUTO else "OFF"),
                    True,
                    (255, 155, 155),
                )
                quitprompt = App.FONT24.render(
                    "Press esc to quit, press space to toggle song.",
                    True,
                    (255, 255, 255),
                )
                App.SCREEN.blits(
                    [
                        (quitprompt, (700, 150)),
                        (text, (400, row * 40 + 200)),
                        (prompt, (300, 100)),
                        (auto, (350, 150)),
                    ]
                )
                row += 1

        AudioWrapper.gameFX.set_volume(0.1)
        while SELECT:
            draw_ui()
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        index -= 1
                        if index < 0:
                            index = len(SONG_LIST) - 1
                        SONG_LIST[index].selected = True
                        for i, song in enumerate(SONG_LIST):
                            if i != index:
                                song.selected = False
                    elif event.key == pg.K_DOWN:
                        index += 1
                        if index >= len(SONG_LIST):
                            index = 0
                        SONG_LIST[index].selected = True
                        for i, song in enumerate(SONG_LIST):
                            if i != index:
                                song.selected = False
                    elif event.key == pg.K_ESCAPE:
                        QUIT = True
                    elif event.key == pg.K_TAB:
                        App.AUTO = not App.AUTO
                    elif event.key == pg.K_RETURN:
                        SELECT = False
                    elif event.key == pg.K_SPACE:
                        PREVIEW = not PREVIEW
                        if PREVIEW:
                            if AudioWrapper.gameFX.get_busy():
                                pass
                            else:
                                AudioWrapper.gameFX.play(Game.get_audio(SONG_LIST[index].level))
                        else:
                            AudioWrapper.gameFX.fadeout(500)

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
