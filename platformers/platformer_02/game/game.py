import pygame as pg
import pygame.event
from typing import Optional

from .entities.player import Player


class Game:
    """Game Class"""
    # TODO: Make .env file or similar!
    # Game Config
    GAME_NAME: str = "Starter App"
    FRAMES: int = 60

    WORLD_GRAVITY: float = .6
    WORLD_GRAVITY_MAX: float = 10.00
    WORLD_CHUNCK_SIZE: int = 32
    # Create Terrains TODO: make proper map with other type of file and not a list !
    WORLD_MAP: list = [
        [0, 0, -1, 0, 0, 0, 0, -1, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 2, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 2, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 2, 1, 2, 0, 0, 0, 1, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, 1, 1, 1, 2, 0, 2, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]

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

    # Palette
    PALETTE: dict = {
        'limit': (0, 0, 0),
        'cloud': (255, 255, 255),
        'sky': (204, 255, 255),
        'ground': (103, 51, 0),
        'grass': (0, 204, 0),

    }
    PALLETE_MAPPING: dict = {
        -2: 'limit',
        -1: 'cloud',
        0: 'sky',
        1: 'ground',
        2: 'grass',
    }
    MAP_COLLISION_MAPPING: dict = {
        -2: True,
        -1: False,
        0: False,
        1: True,
        2: True,
        3: True,
    }

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

        self.player = Player(self.background, self.WORLD_GRAVITY, self.WORLD_GRAVITY_MAX)

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

        while self.game_on:
            self.events()
            if not self.game_on:
                break

            self.game_tick()

    def events(self) -> None:
        """Handles User' events"""
        for event in pygame.event.get():

            if event.type == pygame.QUIT or (
                    event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):  # x button and esc terminates the game!
                self.game_on = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    self.player.move_left = True
                elif event.key == pg.K_RIGHT:
                    self.player.move_right = True
                elif event.key == pg.K_UP or event.key == pg.K_SPACE:
                    self.player.jump()
            if event.type == pg.KEYUP:
                self.player.change_direction(event)

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

        self.background.fill(self.WIN_BACKGROUND)
        _, tiles_with_collision = self.render_tiles()
        self.player.render(tiles_with_collision)
        # Update screen
        pg.display.update()

        self.window.blit(self.background, (0, 0))  # lay down background into the window
        self.game_clock.tick(self.FRAMES)

    def render_tiles(self):
        """Renders the worlds Tiles"""
        chunk = self.WORLD_CHUNCK_SIZE
        tiles_with_collision = []

        def make_chunk(y: int, x: int, cube: int) -> pg.draw.rect:
            """Makes a world chunk"""
            color: tuple = self.PALETTE[self.PALLETE_MAPPING[cube]]
            collision: bool = self.MAP_COLLISION_MAPPING[cube]

            block = pg.draw.rect(self.background, color, pg.Rect((x * chunk, y * chunk, chunk, chunk)))
            if collision:
                tiles_with_collision.append(block)
            return block

        recs = [make_chunk(y, x, cube)
                for y, row in enumerate(self.WORLD_MAP)
                for x, cube in enumerate(row)

                ]

        return recs, tiles_with_collision
