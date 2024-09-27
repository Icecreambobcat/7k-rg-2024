from __future__ import annotations
from abc import abstractmethod
from collections.abc import Callable
from pathlib import Path

from ..App.App import Object, App
from ..App.lib import Lib
from ..App.Conf import Conf
from ..App.parser import Level_FILE
import pygame as pg
from pygame import (
    Rect,
    draw,
    font,
    mixer,
    rect,
    time,
    display,
    image,
    Surface,
    sprite,
    transform,
)


class Game:
    """
    Container for ingame behaviour
    """

    """
    for some reason my type checker really doesn't like pulling fonts from app so here they are
    """
    START_TIME: int = 0
    PASSED_TIME: Callable[[], int]
    PAUSE_TIME: int = 0

    LOADED = sprite.Group()
    # All note sprites are first loaded into this group
    ACTIVE = sprite.Group()
    # Notes that should be visible are then moved into this group
    PASSED = sprite.Group()
    # Notes should be moved here once hit and should then stop being updated and rendered
    HEAD_HIT = sprite.Group()

    MULTIPLIER = Conf.MULTIPLIER
    CONSTANT = Conf.CONSTANT

    @staticmethod
    def PASSED_TIME() -> int:
        return time.get_ticks() - Game.START_TIME - Game.PAUSE_TIME

    @staticmethod
    def ingame_loop(level: Level_FILE) -> bool:
        from ..App.App import AudioWrapper, App

        """
        Provides multiple return states:
        False - pass.
        True - fail OR quit: skip results screen and play fail graphic if fail.
        """

        bg = image.load(Conf.INGAME_BG)
        bg = transform.scale(bg, (1920, 1080))
        line = image.load(Conf.JUDGEMENT_LINE)
        line = transform.scale(line, (700, 20))
        line_rect = line.get_rect(center=(960, 1000))
        cover_rect = Rect(600, 0, 700, 1080)

        App.RECENTSCORE = 0
        QUIT_LEVEL = False
        AudioWrapper.song.set_volume(0.3)

        def failscreen() -> None:
            """Display the fail graphic upon failure."""

            fail = True
            AudioWrapper.fadeout(1000, AudioWrapper.song)

            for n in Game.LOADED:
                n.kill()
            for n in Game.PASSED:
                n.kill()
            for n in Game.ACTIVE:
                n.kill()

            while fail:
                App.SCREEN.fill((0, 0, 0))
                App.SCREEN.blit(bg, (0, 0))
                App.SCREEN.blit(line, line_rect)
                failtext = App.FONT32.render("FAILED!", True, (255, 0, 0))
                failprompt = App.FONT24.render(
                    "Press enter to return to song select", True, (255, 255, 255)
                )
                failrect = failtext.get_rect(center=(960, 540))
                promptrect = failprompt.get_rect(center=(960, 580))
                App.SCREEN.blits([(failtext, failrect), (failprompt, promptrect)])
                display.flip()
                App.CLOCK.tick_busy_loop(120)
                for k in pg.event.get([pg.KEYDOWN, pg.QUIT]):
                    if k.key == pg.K_RETURN:
                        fail = False
                    elif k == pg.QUIT:
                        App.quit_app()

        def load_tex_UI() -> None:
            """loads UI elememnts"""
            App.SCREEN.blit(bg, (0, 0))
            draw.rect(App.SCREEN, (0, 0, 0), cover_rect)
            App.SCREEN.blit(line, line_rect)

        def render_ELEMENTS() -> None:
            score_text = App.FONT32.render(f"{SCORE}", True, (255, 255, 255))
            score_rect = score_text.get_rect(topright=(1920 - 10, 10))
            hp_rect = rect.Rect(10, 10, HEALTH // 2, 40)
            draw.rect(App.SCREEN, (255, 255, 255), hp_rect)
            App.SCREEN.blit(score_text, score_rect)

        def mod_hp(hp: int, amount: int) -> int:
            hp += amount
            if hp > 1000:
                return 1000
            else:
                return hp

        # implement a pause loop
        def pause_loop() -> bool:
            """
            The entire feature is really half-assed so it's best to quit after pausing
            Fixing offset is largely impossible with this setup
            """
            AudioWrapper.pause(AudioWrapper.song)
            pause = True
            quit = False
            while pause:
                App.SCREEN.fill((0, 0, 0))
                pause_text = App.FONT32.render(
                    "PAUSED - ESC TO QUIT, ANY KEY TO CONTINUE", True, (255, 255, 255)
                )
                pause_rect = pause_text.get_rect(center=(960, 540))
                App.SCREEN.blit(pause_text, pause_rect)
                for event in pg.event.get([pg.KEYDOWN, pg.QUIT]):
                    if event.type == pg.KEYDOWN:
                        # if key pressed is esc: then break
                        if event.key == pg.K_ESCAPE:
                            AudioWrapper.stop(AudioWrapper.song)
                            quit = True
                            break
                        else:
                            pause = False
                            App.SCREEN.fill((0, 0, 0))
                            pause_text = App.FONT32.render("3", True, (255, 255, 255))
                            App.SCREEN.blit(pause_text, pause_rect)
                            display.flip()
                            time.delay(1000)
                            App.SCREEN.fill((0, 0, 0))
                            pause_text = App.FONT32.render("2", True, (255, 255, 255))
                            App.SCREEN.blit(pause_text, pause_rect)
                            display.flip()
                            time.delay(1000)
                            App.SCREEN.fill((0, 0, 0))
                            pause_text = App.FONT32.render("1", True, (255, 255, 255))
                            App.SCREEN.blit(pause_text, pause_rect)
                            render_ELEMENTS()
                            display.flip()
                            time.delay(1000)
                    elif event.type == pg.QUIT:
                        App.quit_app()

                display.flip()
                App.CLOCK.tick_busy_loop(120)
                if quit:
                    break
            else:
                AudioWrapper.unpause(AudioWrapper.song)
                return False
            return True

        HEALTH = 1000
        SCORE = 0
        CLOCK = App.CLOCK
        SONG = Game.get_audio(level)
        LEVEL_LOADED = Game.load_level(level)

        for note in LEVEL_LOADED.notes:
            Game.LOADED.add(note)

        load_tex_UI()
        render_ELEMENTS()
        display.flip()
        time.delay(2000)

        Game.START_TIME = App.DELTA_TIME()  # Call right before loop for accuracy

        AudioWrapper.play(SONG, AudioWrapper.song)
        INGAME = True

        # Dictionary to store key event lists for each key
        key_events_this_frame: dict[str, list[dict]] = {
            "s": [],
            "d": [],
            "f": [],
            "space": [],
            "j": [],
            "k": [],
            "l": [],
        }

        # Dictionary to track currently held keys for long notes
        already_paused = False
        Game.PAUSE_TIME = 0

        while INGAME:
            key_events_this_frame: dict[str, list[dict]] = {
                "s": [],
                "d": [],
                "f": [],
                "space": [],
                "j": [],
                "k": [],
                "l": [],
            }
            load_tex_UI()
            render_ELEMENTS()

            # Move notes from LOADED to ACTIVE based on time
            for sp in Game.LOADED:
                if sp.hit_time >= Game.PASSED_TIME() - 500:
                    sp.remove(Game.LOADED)
                    sp.add(Game.ACTIVE)

            Game.ACTIVE.update()

            for event in pg.event.get([pg.KEYDOWN, pg.KEYUP, pg.QUIT]):
                if event.type == pg.QUIT:
                    App.quit_app()
                elif (
                    event.key == pg.K_ESCAPE and already_paused == False
                ):  # Pause handling
                    already_paused = True
                    pre_pause_time = Game.PASSED_TIME()
                    QUIT_LEVEL = pause_loop()
                    Game.PAUSE_TIME = (
                        Game.PASSED_TIME() - pre_pause_time + Game.PAUSE_TIME
                    )
                    continue
                elif App.AUTO:
                    continue
                elif event.type == pg.KEYDOWN:
                    already_paused = False
                    key_name = pg.key.name(event.key)
                    if key_name in key_events_this_frame:
                        key_events_this_frame[key_name].append(
                            {"event": "down", "time": Game.PASSED_TIME()}
                        )
                elif event.type == pg.KEYUP:
                    already_paused = False
                    key_name = pg.key.name(event.key)
                    if key_name in key_events_this_frame:
                        key_events_this_frame[key_name].append(
                            {
                                "event": "up",
                                "time": Game.PASSED_TIME(),
                            }
                        )
                time.delay(1)

            if App.AUTO == False:
                for key, events in key_events_this_frame.items():
                    for event in events:
                        if event["event"] == "down":
                            for note in Game.ACTIVE:
                                if (
                                    note not in Game.HEAD_HIT
                                    and note.type == "LongNote"
                                ):
                                    if note.required_key == key:
                                        diff_time = abs(note.hit_time - event["time"])
                                        if diff_time <= Conf.HIT_WINDOWS["miss"]:
                                            if (
                                                diff_time
                                                <= Conf.HIT_WINDOWS["plusperfect"]
                                            ):
                                                SCORE += Conf.SCORING["plusperfect"]
                                                HEALTH = mod_hp(HEALTH, 5)
                                            elif (
                                                diff_time <= Conf.HIT_WINDOWS["perfect"]
                                            ):
                                                SCORE += Conf.SCORING["perfect"]
                                                HEALTH = mod_hp(HEALTH, 3)
                                            elif diff_time <= Conf.HIT_WINDOWS["great"]:
                                                SCORE += Conf.SCORING["great"]
                                                HEALTH = mod_hp(HEALTH, 1)
                                            elif diff_time <= Conf.HIT_WINDOWS["good"]:
                                                SCORE += Conf.SCORING["good"]
                                                HEALTH = mod_hp(HEALTH, 0)
                                            else:
                                                SCORE += Conf.SCORING["miss"]
                                                HEALTH = mod_hp(HEALTH, -80)
                                            note.add(
                                                Game.HEAD_HIT
                                            )  # Mark the long note's head as hit

                                elif note.required_key == key:
                                    diff_time = abs(note.hit_time - event["time"])
                                    if diff_time <= Conf.HIT_WINDOWS["miss"]:
                                        if diff_time <= Conf.HIT_WINDOWS["plusperfect"]:
                                            SCORE += Conf.SCORING["plusperfect"]
                                            HEALTH = mod_hp(HEALTH, 5)
                                        elif diff_time <= Conf.HIT_WINDOWS["perfect"]:
                                            SCORE += Conf.SCORING["perfect"]
                                            HEALTH = mod_hp(HEALTH, 3)
                                        elif diff_time <= Conf.HIT_WINDOWS["great"]:
                                            SCORE += Conf.SCORING["great"]
                                            HEALTH = mod_hp(HEALTH, 1)
                                        elif diff_time <= Conf.HIT_WINDOWS["good"]:
                                            SCORE += Conf.SCORING["good"]
                                            HEALTH = mod_hp(HEALTH, 0)
                                        else:
                                            SCORE += Conf.SCORING["miss"]
                                            HEALTH = mod_hp(HEALTH, -80)

                                        note.remove(Game.ACTIVE)
                                        note.add(Game.PASSED)

                        # On KEYUP: process the end of the long note
                        elif event["event"] == "up":
                            for note in Game.HEAD_HIT:
                                if key == note.required_key and note.type == "LongNote":
                                    diff_time = abs(note.endtime - event["time"])
                                    if diff_time <= Conf.HIT_WINDOWS["miss"]:
                                        if diff_time <= Conf.HIT_WINDOWS["plusperfect"]:
                                            SCORE += Conf.SCORING["plusperfect"]
                                            HEALTH = mod_hp(HEALTH, 5)
                                        elif diff_time <= Conf.HIT_WINDOWS["perfect"]:
                                            SCORE += Conf.SCORING["perfect"]
                                            HEALTH = mod_hp(HEALTH, 3)
                                        elif diff_time <= Conf.HIT_WINDOWS["great"]:
                                            SCORE += Conf.SCORING["great"]
                                            HEALTH = mod_hp(HEALTH, 1)
                                        elif diff_time <= Conf.HIT_WINDOWS["good"]:
                                            SCORE += Conf.SCORING["good"]
                                            HEALTH = mod_hp(HEALTH, 0)
                                    else:
                                        SCORE += Conf.SCORING["miss"]
                                        HEALTH = mod_hp(HEALTH, -80)

                                    # Remove the note from active play
                                    note.remove(Game.ACTIVE)
                                    note.remove(Game.HEAD_HIT)
                                    note.add(Game.PASSED)

                for sp in Game.ACTIVE:
                    if sp.type == "TapNote" and sp.hit_time <= (
                        Game.PASSED_TIME() - Conf.HIT_WINDOWS["miss"]
                    ):
                        SCORE += Conf.SCORING["miss"]
                        HEALTH = mod_hp(HEALTH, -80)
                        sp.remove(Game.ACTIVE)
                        sp.add(Game.PASSED)

            else:  # Auto-play logic
                for note in Game.ACTIVE:
                    if note.type == "TapNote":
                        if note.hit_time <= Game.PASSED_TIME() - 10:
                            SCORE += Conf.SCORING["plusperfect"]
                            note.remove(Game.ACTIVE)
                            note.add(Game.PASSED)
                    elif (
                        note.hit_time <= Game.PASSED_TIME() - 10
                        and note not in Game.HEAD_HIT
                    ):
                        SCORE += Conf.SCORING["plusperfect"]
                        note.add(Game.HEAD_HIT)
                    elif note.endtime <= Game.PASSED_TIME() - 10:
                        SCORE += Conf.SCORING["plusperfect"]
                        note.remove(Game.HEAD_HIT)
                        note.remove(Game.ACTIVE)
                        note.add(Game.PASSED)

            Game.ACTIVE.update()

            if HEALTH <= 0:
                failscreen()
                break
            elif QUIT_LEVEL:
                break
            elif AudioWrapper.song.get_busy() == False:
                INGAME = False
                Game.PASSED.empty()
                App.RECENTSCORE = SCORE

            if pg.event.get(pg.QUIT):
                App.quit_app()

            display.flip()
            CLOCK.tick_busy_loop(120)

        else:
            return False
        return True

    @staticmethod
    def load_level(level: Level_FILE) -> Level_MEMORY:
        return Level_MEMORY(level)

    @staticmethod
    def get_audio(level: Level_FILE) -> mixer.Sound:
        """
        For fetching the level audio for a level
        """

        info = level.info
        if "AudioFilename" in info.keys():
            SONG = mixer.Sound(
                Path(
                    Lib.PROJECT_ROOT,
                    "Assets",
                    "Levels",
                    str(level.meta["TitleUnicode"]),
                    level.info["AudioFilename"],
                )
            )
            return SONG
        else:
            App.quit_app(
                FileNotFoundError(
                    "Audio file not found in level metadata:",
                    level.meta["TitleUnicode"],
                )
            )


class Note(Object):
    """
    Strictly only a parent class to contain TapNote and LongNote as well as common logic

    TODO: Optimise runtime overhead of loading stuff
    """

    @property
    @abstractmethod
    def type(self) -> str:
        pass

    @property
    @abstractmethod
    def hit_time(self) -> int:
        pass

    @property
    @abstractmethod
    def lane(self) -> int:
        pass

    @property
    def required_key(self):
        table = {
            0: "s",
            1: "d",
            2: "f",
            3: "space",
            4: "j",
            5: "k",
            6: "l",
        }
        return table[self.lane]

    lane_map = {
        36: 0,
        109: 1,
        182: 2,
        256: 3,
        329: 4,
        402: 5,
        475: 6,
    }

    _white_tex = transform.scale(image.load(Conf.NOTE_TEX_WHITE), (100, 50))
    _blue_tex = transform.scale(image.load(Conf.NOTE_TEX_BLUE), (100, 50))
    _gold_tex = transform.scale(image.load(Conf.NOTE_TEX_GOLD), (100, 50))
    _ln_body = image.load(Conf.NOTE_TEX_BODY)

    @property
    def image(self) -> Surface:
        if self.lane == 3:
            return Note._gold_tex
        return Note._white_tex if self.lane in [0, 2, 4, 6] else Note._blue_tex

    def calc_pos(self) -> int:
        out = (Game.PASSED_TIME() - self.hit_time) * Game.MULTIPLIER + Game.CONSTANT
        return int(out)


class TapNote(Note):
    """
    tapnote logic
    """

    def __init__(self, lane: int, note_time: int) -> None:
        sprite.Sprite.__init__(self)
        self._lane = Note.lane_map[lane]
        self._time = note_time

    def update(self) -> None:
        App.SCREEN.blit(self.image, self.position)

    @property
    def type(self):
        return "TapNote"

    @property
    def position(self) -> tuple[int, int]:
        return (self.lane * 100 + 600, self.calc_pos())

    @property
    def hit_time(self) -> int:
        return self._time

    @property
    def lane(self) -> int:
        return self._lane


class LongNote(Note):
    """
    LN logic
    """

    def __init__(self, lane: int, note_time: int, note_endtime: int) -> None:
        sprite.Sprite.__init__(self)
        self._lane = Note.lane_map[lane]
        self._time = note_time
        self._endtime = note_endtime
        self._body = transform.scale(
            Note._ln_body, (100, self.calc_end_len() * Game.MULTIPLIER - 50)
        )

    def update(self) -> None:
        if self not in Game.HEAD_HIT:
            App.SCREEN.blit(
                self._body,
                (
                    self.lane * 100 + 600,
                    self.calc_pos() - self.calc_end_len() * Game.MULTIPLIER + 50,
                ),
            )
            App.SCREEN.blit(self.image, self.position)
        else:
            App.SCREEN.blit(
                self._body,
                (
                    self.lane * 100 + 600,
                    self.calc_pos() - self.calc_end_len() * Game.MULTIPLIER,
                ),
            )

    def calc_end_len(self) -> int:
        return int(self._endtime - self._time)

    @property
    def type(self):
        return "LongNote"

    @property
    def position(self) -> tuple[int, int]:
        return (self.lane * 100 + 600, self.calc_pos())

    @property
    def hit_time(self) -> int:
        return self._time

    @property
    def endtime(self) -> int:
        return self._endtime

    @property
    def lane(self) -> int:
        return self._lane

    """
    Hold tail textures MAY be implemented for certain skins and textures
    But will not be implemented with this version as most players prefer to have them invisible

    These are commented out but are perfectly valid implementations otherwise
    """
    # @property
    # def image_tail(self) -> Surface:
    #     tex = image.load(Conf.NOTE_TEX_TAIL)
    #     tex = transform.scale(tex, (200, 100))
    #     return tex

    # @property
    # def rect_tail(self) -> Rect:
    #     return self.image_tail.get_rect()


class Level_MEMORY:
    """
    The actual object passed to the level engine at runtime
    Ensures reasonable overheads and isolates level data from loaded sprites which are more expensive
    """

    @staticmethod
    def load_notes(line: list[str]) -> Note:
        obj_type = int(line[3])
        time = int(line[2])
        endtime = time
        lane = int(line[0])

        is_tap = obj_type & (1 << 0) != 0
        is_long = obj_type & (1 << 7) != 0

        if is_tap:
            return TapNote(lane, time)
        elif is_long:
            endtime = int(line[5].split(":")[0])
            return LongNote(lane, time, endtime)

        else:
            App.quit_app(FileNotFoundError("Loaded level file is of incorrect format."))

    def __init__(self, level: Level_FILE) -> None:
        """
        reads level data and removes invalid notes
        """

        self.notes: list[Note] = [Level_MEMORY.load_notes(line) for line in level.notes]
        self.meta = level.meta
        self.info = level.info
