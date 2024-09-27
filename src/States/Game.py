from __future__ import annotations
from abc import abstractmethod
from pathlib import Path

from ..shared import App, AudioWrapper, Object, Level_FILE, Lib, Game, Conf
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
from threading import Lock, Thread
from queue import Queue


class Game:
    """
    Container for ingame behaviour
    """

    """
    for some reason my type checker really doesn't like pulling fonts from app so here they are
    """
    FONT32 = font.Font(Conf.FONT_TEX, 32)
    FONT24 = font.Font(Conf.FONT_TEX, 24)
    FONT12 = font.Font(Conf.FONT_TEX, 12)

    START_TIME: int
    PASSED_TIME: int

    LOADED = sprite.Group()
    # All note sprites are first loaded into this group
    ACTIVE = sprite.Group()
    # Notes that should be visible are then moved into this group
    PASSED = sprite.Group()
    # Notes should be moved here once hit and should then stop being updated and rendered

    @staticmethod
    def ingame_loop(level: Level_FILE, auto: bool) -> bool:
        """
        Provides multiple return states:
        False - pass.
        True - fail OR quit: skip results screen and play fail graphic if fail.
        """

        bg = image.load(Conf.INGAME_BG)
        bg = transform.scale(bg, (1920, 1080))
        line = image.load(Conf.JUDGEMENT_LINE)
        line = transform.scale(line, (1400, 20))
        line_rect = line.get_rect(center=(960, 1000))
        cover_rect = Rect(260, 0, 1400, 1080)

        App.RECENTSCORE = 0
        QUIT_LEVEL = False
        KEY_QUEUE = Queue()
        QUEUE_LOCK = Lock()

        def get_key_events():
            while True:
                events = pg.event.get([pg.KEYDOWN, pg.KEYUP])
                timestamp = Game.PASSED_TIME
                with QUEUE_LOCK:
                    for event in events:
                        key_time = {"key": event, "time": timestamp}
                        KEY_QUEUE.put(key_time)
                time.delay(1)

        key_thread = Thread(target=get_key_events)
        key_thread.daemon = True
        key_thread.start()

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
                failtext = Game.FONT32.render("FAILED!", True, (255, 0, 0))
                failprompt = Game.FONT12.render(
                    "Press any key to return to song select", True, (255, 255, 255)
                )
                failrect = failtext.get_rect(center=(960, 540))
                promptrect = failprompt.get_rect(center=(960, 580))
                App.SCREEN.blits([(failtext, failrect), (failprompt, promptrect)])
                display.flip()
                App.CLOCK.tick_busy_loop(120)
                if pg.event.get(pg.KEYDOWN):
                    break
                elif pg.event.get(pg.QUIT):
                    App.quit_app()

        def load_tex_UI() -> None:
            """loads UI elememnts"""
            App.SCREEN.blit(bg, (0, 0))
            draw.rect(App.SCREEN, (0, 0, 0), cover_rect)
            App.SCREEN.blit(line, line_rect)

        def render_ELEMENTS() -> None:
            score_text = Game.FONT32.render(f"{SCORE}", True, (255, 255, 255))
            score_rect = score_text.get_rect(topright=(1920 - 10, 10))
            hp_rect = rect.Rect(10, 10, HEALTH // 2, 40)
            draw.rect(App.SCREEN, (255, 255, 255), hp_rect)
            App.SCREEN.blit(score_text, score_rect)

        def mod_hp(hp: int, amount: int) -> int:
            hp += amount
            if hp > 1000:
                return 1000
            return hp

        # implement a pause loop
        def pause_loop() -> bool:
            AudioWrapper.pause(AudioWrapper.song)
            pause = True
            quit = False
            while pause:
                App.SCREEN.fill((0, 0, 0))
                pause_text = Game.FONT32.render(
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
                            render_ELEMENTS()
                            pause_text = Game.FONT32.render("3", True, (255, 255, 255))
                            App.SCREEN.blit(pause_text, pause_rect)
                            display.flip()
                            time.delay(1000)
                            pause_text = Game.FONT32.render("2", True, (255, 255, 255))
                            App.SCREEN.blit(pause_text, pause_rect)
                            display.flip()
                            time.delay(1000)
                            pause_text = Game.FONT32.render("1", True, (255, 255, 255))
                            App.SCREEN.blit(pause_text, pause_rect)
                            time.delay(1000)
                            display.flip()
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

        Game.START_TIME = App.DELTA_TIME()  # Call right before loop for accuracy
        Game.PASSED_TIME = Game.START_TIME

        AudioWrapper.play(SONG, AudioWrapper.song)
        INGAME = True

        # Dictionary to store key event lists for each key
        key_events_this_frame: dict[str, list[dict]] = {
            "s": [],
            "d": [],
            "f": [],
            " ": [],
            "j": [],
            "k": [],
            "l": [],
        }

        # Dictionary to track currently held keys for long notes
        held_keys = {}

        while INGAME:
            load_tex_UI()
            Game.PASSED_TIME = App.DELTA_TIME() - Game.START_TIME

            # Move notes from LOADED to ACTIVE based on time
            for sp in Game.LOADED:
                if sp.time <= Game.PASSED_TIME - 2000:
                    sp.remove(Game.LOADED)
                    sp.add(Game.ACTIVE)

            # Reset key events per frame
            for key in key_events_this_frame:
                key_events_this_frame[key].clear()

            # Process input events
            while not KEY_QUEUE.empty():
                event_data = KEY_QUEUE.get()
                pressed = event_data["key"]
                timestamp = event_data["time"]

                # Store multiple keydown and keyup events for each key
                key_name = pg.key.name(pressed.key)
                if key_name in key_events_this_frame:
                    key_events_this_frame[key_name].append(
                        {"event": pressed.type, "time": timestamp}
                    )

            # Process active notes based on key events
            if not auto:
                notes_hit_this_frame = set()

                # Iterate over each key event that occurred this frame
                for key, events in key_events_this_frame.items():
                    for event in events:
                        if event["event"] == pg.KEYDOWN:
                            # if key is esc then pause
                            if key == "escape":
                                QUIT_LEVEL = pause_loop()
                            # Process each note in the active notes list
                            for note in Game.ACTIVE:
                                if note in notes_hit_this_frame:
                                    continue  # Skip notes that were already hit in this frame

                                hit_time = Game.PASSED_TIME - note.hit_time
                                if hit_time > Conf.HIT_WINDOWS["miss"]:
                                    continue

                                # Check if the note matches the key and is within the hit window
                                hit_window = abs(hit_time)
                                if (
                                    note.required_key == key
                                    and hit_window <= Conf.HIT_WINDOWS["miss"]
                                ):
                                    if note.is_long_note:
                                        # Long note: store it as held
                                        held_keys[key] = {
                                            "note": note,
                                            "start_time": Game.PASSED_TIME,
                                        }
                                    else:
                                        if (
                                            hit_window
                                            <= Conf.HIT_WINDOWS["plusperfect"]
                                        ):
                                            SCORE += Conf.SCORING["plusperfect"]
                                            HEALTH = mod_hp(HEALTH, 5)
                                        elif hit_window <= Conf.HIT_WINDOWS["perfect"]:
                                            SCORE += Conf.SCORING["perfect"]
                                            HEALTH = mod_hp(HEALTH, 3)
                                        elif hit_window <= Conf.HIT_WINDOWS["great"]:
                                            SCORE += Conf.SCORING["great"]
                                            HEALTH = mod_hp(HEALTH, 1)
                                        elif hit_window <= Conf.HIT_WINDOWS["good"]:
                                            SCORE += Conf.SCORING["good"]
                                            HEALTH = mod_hp(HEALTH, 0)
                                        else:
                                            SCORE += Conf.SCORING["miss"]
                                            HEALTH = mod_hp(HEALTH, -10)

                                        note.remove(Game.ACTIVE)
                                        note.add(Game.PASSED)
                                        notes_hit_this_frame.add(note)
                                        break

                        elif event["event"] == pg.KEYUP:
                            # Handle key release for long notes
                            if key in held_keys:
                                held_note_info = held_keys[key]
                                note = held_note_info["note"]

                                # Check if key is released within the long note's release window
                                hit_window = abs(Game.PASSED_TIME - note.endtime)
                                if hit_window <= Conf.HIT_WINDOWS["miss"]:
                                    if hit_window <= Conf.HIT_WINDOWS["plusperfect"]:
                                        SCORE += Conf.SCORING["plusperfect"]
                                        HEALTH = mod_hp(HEALTH, 5)
                                    elif hit_window <= Conf.HIT_WINDOWS["perfect"]:
                                        SCORE += Conf.SCORING["perfect"]
                                        HEALTH = mod_hp(HEALTH, 3)
                                    elif hit_window <= Conf.HIT_WINDOWS["great"]:
                                        SCORE += Conf.SCORING["great"]
                                        HEALTH = mod_hp(HEALTH, 1)
                                    elif hit_window <= Conf.HIT_WINDOWS["good"]:
                                        SCORE += Conf.SCORING["good"]
                                        HEALTH = mod_hp(HEALTH, 0)
                                    else:
                                        SCORE += Conf.SCORING["miss"]
                                        HEALTH = mod_hp(HEALTH, -10)

                                    note.remove(Game.ACTIVE)
                                    note.add(Game.PASSED)
                                else:
                                    # Penalize for releasing too early or too late
                                    SCORE += Conf.SCORING["miss"]
                                    HEALTH = mod_hp(HEALTH, -10)
                                    note.remove(Game.ACTIVE)
                                    note.add(Game.PASSED)

                                # Remove the key from held_keys once it's released
                                del held_keys[key]

                # Handle notes that weren't hit and are now too late
                for note in Game.ACTIVE:
                    if note.hit_time <= Game.PASSED_TIME - Conf.HIT_WINDOWS["miss"]:
                        SCORE += Conf.SCORING["miss"]
                        HEALTH = mod_hp(HEALTH, -10)
                        note.remove(Game.ACTIVE)
                        note.add(Game.PASSED)

            else:  # Auto-play logic
                for note in Game.ACTIVE:
                    if note.type is TapNote and note.hit_time <= Game.PASSED_TIME - 10:
                        SCORE += Conf.SCORING["plusperfect"]
                        note.remove(Game.ACTIVE)
                        note.add(Game.PASSED)
                    elif note.hit_time <= Game.PASSED_TIME - 10:
                        SCORE += Conf.SCORING["plusperfect"]
                    elif note.endtime <= Game.PASSED_TIME - 10:
                        SCORE += Conf.SCORING["plusperfect"]
                        note.remove(Game.ACTIVE)
                        note.add(Game.PASSED)

            render_ELEMENTS()

            Game.ACTIVE.update()

            for n in Game.PASSED:
                n.kill()
            Game.PASSED.empty()

            if HEALTH <= 0:
                failscreen()
                break
            elif QUIT_LEVEL:
                break
            elif AudioWrapper.song.get_busy() == False:
                INGAME = False
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
    def type(self) -> object:
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
    def required_key(self) -> str:
        table = {
            0: "s",
            1: "d",
            2: "f",
            3: " ",
            4: "j",
            5: "k",
            6: "l",
        }
        return table[self.lane - 1]

    _white_tex = None
    _blue_tex = None

    @property
    def image(self) -> Surface:
        if Note._white_tex is None:
            Note._white_tex = image.load(Conf.NOTE_TEX_WHITE)
            Note._white_tex = transform.scale(Note._white_tex, (200, 100))

        if Note._blue_tex is None:
            Note._blue_tex = image.load(Conf.NOTE_TEX_BLUE)
            Note._blue_tex = transform.scale(Note._blue_tex, (200, 100))

        return Note._white_tex if self.lane in [0, 2, 4, 6] else Note._blue_tex

    def calc_pos(self) -> int:
        out = (self.hit_time - Game.PASSED_TIME) * Conf.MULTIPLIER + Conf.CONSTANT
        return int(out)


class TapNote(Note):
    """
    tapnote logic
    """

    def __init__(self, lane: int, note_time: int) -> None:
        sprite.Sprite.__init__(self)
        self._lane = lane
        self._time = note_time

    def update(self) -> None:
        App.SCREEN.blit(self.image, self.position)

    @property
    def type(self):
        return TapNote

    @property
    def position(self) -> tuple[int, int]:
        return (self.lane, self.calc_pos())

    @property
    def hit_time(self) -> int:
        return self._time

    @property
    def lane(self) -> int:
        return self._lane

    @property
    def rect(self) -> Rect:
        return self.image.get_rect()


class LongNote(Note):
    """
    LN logic
    """

    def __init__(self, lane: int, note_time: int, note_endtime: int) -> None:
        sprite.Sprite.__init__(self)
        self._lane = lane
        self._time = note_time
        self._endtime = note_endtime

    def update(self) -> None:
        App.SCREEN.blit(self.image, self.position)
        App.SCREEN.blit(self.image_body, self.position)

    def calc_end_pos(self) -> int:
        out = (self.endtime - Game.PASSED_TIME) * Conf.MULTIPLIER + Conf.CONSTANT
        return int(out)

    @property
    def type(self):
        return LongNote

    @property
    def position(self) -> tuple[int, int]:
        return (self.lane, self.calc_pos())

    @property
    def hit_time(self) -> int:
        return self._time

    @property
    def endtime(self) -> int:
        return self._endtime

    @property
    def lane(self) -> int:
        return self._lane

    @property
    def rect(self) -> Rect:
        return self.image.get_rect()

    @property
    def image_body(self) -> Surface:
        tex = image.load(Conf.NOTE_TEX_BODY)
        tex = transform.scale(tex, (self.calc_end_pos() - self.calc_pos(), 100))
        return tex

    @property
    def rect_body(self) -> Rect:
        return self.image_body.get_rect()

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
        obj_type = None
        time = int(line[2])
        endtime = time
        lane = int(line[0])

        if int(line[3]) == 0:
            obj_type = TapNote
        elif int(line[3]) == 7:
            obj_type = LongNote
            endtime = int(line[5])

        if obj_type == TapNote:
            return TapNote(lane, time)
        elif obj_type == LongNote:
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
