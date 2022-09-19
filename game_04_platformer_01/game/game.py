import random

import pygame as pg
import pygame.event
from typing import Optional

from .entities.entity import Entity


class Game:
    """Game Class"""
    # TODO: Make .env file or similar!
    # Game Config
    GAME_NAME: str = "Starter App"
    FRAMES: int = 60

    # Screen config
    WIN_SIZE: tuple = (850, 500)
    WIN_WIDTH: int = WIN_SIZE[0]
    WIN_HEIGHT: int = WIN_SIZE[1]
    WIN_RECT = pg.Rect(0, 0, *WIN_SIZE)
    WIN_BACKGROUND: tuple = (0, 0, 0)
    FULL_SCREEN: bool = False
    RESIZABLE: bool = False
    COLOR_BIT: int = 32
    VSYNC: bool = False  # TODO: learn what vsync does
    MOUSE_VISIBLE: bool = True

    # Style config
    FONT_FAMILY: str = "Times New Roman"
    FONT_COLOR: tuple = (255, 255, 255)
    FONT_SIZE: int = 16
    FONT_BASE = None

    # Audio Config
    MIXER_PRE_INIT: bool = True
    MIXER_CHANNELS_NUMBER: int = 64

    # DEBUG
    DEBUG_BALL_POS: bool = False

    def __init__(self):
        self.game_on: bool = True
        self.game_clock: pg.Clock = pygame.time.Clock()

        self.window: Optional[pg.Surface] = None
        self.background: Optional[pg.Surface] = None

        self.entities_all: Optional[pg.RenderUpdates] = pg.sprite.RenderUpdates()

        self.setup()
        self.window_setup()
        self.game_setup()

    # ---------------------
    #   CONFIGURATIONS + INIT
    # ---------------------

    def setup(self) -> None:
        """Setups Pygame"""

        if self.MIXER_PRE_INIT:
            pg.mixer.pre_init(44100, 32, 2, 1024)  # frequency, size, stereo (2), buffer
        pg.init()
        if self.MIXER_PRE_INIT and self.MIXER_CHANNELS_NUMBER:
            pg.mixer.set_num_channels(self.MIXER_CHANNELS_NUMBER)
        self.FONT_BASE: pg.Font = pg.freetype.SysFont(self.FONT_FAMILY, self.FONT_SIZE)
        pg.display.set_caption(self.GAME_NAME)
        # TODO: Add Game icon
        # icon = ...
        # pg.display.set_icon(icon)
        pg.mouse.set_visible(self.MOUSE_VISIBLE)

    def window_setup(self) -> None:
        """Initizialize and setup window and background"""
        flags = pygame.FULLSCREEN if self.FULL_SCREEN else pygame.RESIZABLE if self.RESIZABLE else 0
        bestdepth = pg.display.mode_ok(self.WIN_RECT.size, flags, 32) or self.COLOR_BIT
        window: pg.Surface = pg.display.set_mode(self.WIN_RECT.size, flags, bestdepth, vsync=self.VSYNC)

        background: pg.Surface = pg.Surface(window.get_size()).convert()
        background.fill(self.WIN_BACKGROUND)

        pg.display.flip()  # render the window
        window.blit(background, (0, 0))  # lay down background into the window
        self.window = window
        self.background = background

    def game_setup(self):
        """Set-up a new Game"""
        pass

    def _initialize_entities(self) -> None:
        """Loads entities for the level"""
        pass

    # ---------------------
    #   GAME
    # ---------------------

    def run(self) -> None:
        """RUn the game"""
        # if not self.entities_all:
        #     raise Exception("Error, Game UI not initialized")

        background_objects = [[0.25, [120, 10, 70, 400]], [0.25, [280, 30, 40, 400]], [0.5, [30, 40, 40, 400]],
                              [0.5, [130, 90, 100, 400]], [0.5, [300, 80, 120, 400]]]

        # Create Terrains
        map = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 1, 1, 1, 0, 0],
            [0, 1, 1, 1, 0, 0, 0, 1, 0, 0],
            [1, 1, 1, 1, 1, 0, 1, 1, 0, 0],
            [1, 1, 1, 1, 1, 0, 1, 1, 0, 0],
            [1, 1, 1, 1, 1, 0, 1, 1, 0, 0],
        ]


        map_width = len(map[0])
        map_height = len(map)
        w = round((self.WIN_WIDTH / map_width))
        h = round((self.WIN_HEIGHT / map_height))
        y = 0
        for r in map:
            x = 0
            for c in r:
                if c == 1:
                    color = (0, 255, 80)
                else:
                    color = (165, 42, 42)

                block = Entity.make_from_surface((w, h), (w * x, y * h), color)
                self.entities_all.add(block)

                x += 1
            y += 1

        count = 0

        while self.game_on:
            self.events()
            if not self.game_on:
                break
            count += 1
            self.background.fill(self.WIN_BACKGROUND)
            self.game_tick()

            self.window.blit(self.background, (0, 0))  # lay down background into the window

    def events(self) -> None:
        """Handles User' events"""
        for event in pygame.event.get():

            if event.type == pygame.QUIT or (
                    event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):  # x button and esc terminates the game!
                self.game_on = False

    def screen_clear(self) -> None:
        """Clear and updates the screen"""
        # clear/erase the last drawn sprites
        if not self.entities_all:
            return
        self.entities_all.clear(self.window, self.background)

    @staticmethod
    def screen_update(*args) -> None:
        """Update screen with given object

        :param args: tuple of entities to update
        :return: None
        """
        for a in args:
            pg.display.update(a)

    def game_tick(self) -> None:
        """Represents a 'Game tick'"""

        # ---------------
        # Padels
        # ---------------
        # move player 1
        keystates = pg.key.get_pressed()
        entities_dirty = None
        if self.entities_all:
            entities_dirty = self.entities_all.draw(self.window)
            self.entities_all.update()  # update all the sprites

        # Update screen
        self.screen_update(entities_dirty)

        self.game_clock.tick(self.FRAMES)
