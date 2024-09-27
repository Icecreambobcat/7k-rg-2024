from __future__ import annotations
from ..App.App import App
import pygame as pg
from pygame import (
    display,
    image,
    transform,
)

from ..App.Conf import Conf


class Results:
    """
    Results screen loop & logic
    """

    @staticmethod
    def results_loop() -> bool:
        """
        False for normal true for retry
        """

        bg = image.load(Conf.RESULTS_BG)
        bg = transform.scale(bg, (1920, 1080))
        score = App.FONT32.render(f"Score: {App.RECENTSCORE}", True, (255, 255, 255))
        score_rect = score.get_rect(center=(960, 300))
        prompt = App.FONT24.render(
            "Press enter to continue, press space to retry", True, (255, 255, 255)
        )
        prompt_rect = prompt.get_rect(center=(960, 600))

        def update_ui() -> None:
            App.SCREEN.blit(bg, (0, 0))
            App.SCREEN.blits([(score, score_rect), (prompt, prompt_rect)])

        RETRY = False
        RESULTS = True
        CLOCK = App.CLOCK

        while RESULTS:
            update_ui()

            for event in pg.event.get([pg.KEYDOWN]):
                if event.key == pg.K_RETURN:
                    RESULTS = False
                elif event.key == pg.K_SPACE:
                    RETRY = True

            if RETRY:
                break

            display.flip()
            CLOCK.tick_busy_loop(120)
        else:
            return False
        return True
