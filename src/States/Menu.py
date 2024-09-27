from __future__ import annotations
from App.App import App, AudioWrapper
import pygame as pg
from pygame import (
    display,
    image,
    transform,
)
from App.Conf import Conf


class Menu:
    """
    Menu loop & logic
    """

    @staticmethod
    def menu_loop() -> bool:
        """
        Return true to quit
        """

        bg = image.load(Conf.MENU_BG)
        bg = transform.scale(bg, (1920, 1080))
        welcome_text = App.FONT32.render("Welcome to my game!", True, (255, 255, 255))
        rect_line1 = welcome_text.get_rect(center=(960, 500))
        welcome_line2 = App.FONT24.render(
            "Press enter to start, press esc to quit.", True, (255, 255, 255)
        )
        rect_line2 = welcome_line2.get_rect(center=(960, 570))

        def render_ui() -> None:
            App.SCREEN.blit(bg, (0, 0))
            App.SCREEN.blit(welcome_text, rect_line1)
            App.SCREEN.blit(welcome_line2, rect_line2)

        MENU = True
        CLOCK = App.CLOCK
        QUIT = False

        while MENU:
            render_ui()
            for event in pg.event.get([pg.KEYDOWN]):
                if event.key == pg.K_RETURN:
                    MENU = False
                if event.key == pg.K_ESCAPE:
                    QUIT = True

            if QUIT:
                break

            display.flip()
            CLOCK.tick_busy_loop(120)
        else:
            return False
        return True
