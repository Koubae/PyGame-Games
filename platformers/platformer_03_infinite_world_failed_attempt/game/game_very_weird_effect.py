"""Because of a mistake, it makes a super weird effect !"""
import pygame as pg
import pygame.event
from typing import Optional, List

from .entities.player import Player


class Game:
    """Game Class"""
    # TODO: Make .env file or similar!
    # Game Config
    GAME_NAME: str = "Starter App"
    FRAMES: int = 30

    WORLD_GRAVITY: float = .6
    WORLD_GRAVITY_MAX: float = 10.00
    WORLD_CHUNCK_SIZE: int = 32
    WORLD_CAMERA_MOVE_RIGHT: int = 650
    WORLD_CAMERA_MOVE_LEFT: int = 80
    # Create Terrains TODO: make proper map with other type of file and not a list !
    WORLD_MAP: list = [
        [0, 0, -1, 0, 0, 0, 0, -1, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 2, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 2, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 2, 1, 2, 0, 0, 0, 1, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
         2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, 1, 1, 1, 2, 0, 2, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
         1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
         1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
         1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
         1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
         1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]

    # Screen config
    # WIN_SIZE: tuple = (850, 500)
    WIN_SIZE: tuple = (600, 400)
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

        self.camera: List[float] = [0.00, 0.00]
        self.camera_momentum: int = 20

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
        window: pg.Surface = pg.display.set_mode(self.WIN_RECT.size, pygame.RESIZABLE, bestdepth, vsync=self.VSYNC)

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

        # player_right_offset = self.player.rect.right
        # if player_right_offset >= self.WORLD_CAMERA_MOVE_RIGHT and self.player.move_right:
        #     if (player_right_offset - self.WORLD_CAMERA_MOVE_RIGHT) < self.WORLD_CHUNCK_SIZE:
        #         self.camera_next = player_right_offset - self.WORLD_CAMERA_MOVE_RIGHT
        #         # if self.camera_next > len(self.WORLD_MAP[0]):
        #         #     self.camera_next = len(self.WORLD_MAP[0])
        #
        # player_left_offset = self.player.rect.left
        # if player_left_offset <= self.WORLD_CAMERA_MOVE_LEFT and self.player.move_left:
        #     if player_left_offset < self.WORLD_CAMERA_MOVE_LEFT:
        #         # self.camera_next = -1
        #         self.camera_next = - ( player_left_offset - self.WORLD_CAMERA_MOVE_LEFT)
        #         # if self.camera_next < 0:
        #         #     self.camera_next = 0
        # print(self.camera_next, player_left_offset, self.WORLD_CAMERA_MOVE_LEFT,  self.player.move_left )
        # if self.camera_next != 0:
        #     if self.camera_next < 1:
        #         self.camera_offset_right = "LEFT"
        #         self.camera_next += 1
        #     else:
        #         self.camera_offset_right = "RIGHT"
        #         self.camera_next -= 1
        
        # Claer screen
        self.background.fill(self.WIN_BACKGROUND)
        
        # Move Camera
        self.camera_move()
        # Render World
        _, tiles_with_collision = self.render_world()
        self.player.render(tiles_with_collision, self.camera)

        # Update screen
        pg.display.update()

        self.window.blit(self.background, (0, 0))  # lay down background into the window
        self.game_clock.tick(self.FRAMES)

    def camera_move(self):
        self.camera[0] += (((self.player.rect.x - self.camera[0]) - self.WIN_WIDTH / 2) / self.camera_momentum)
        self.camera[1] += (((self.player.rect.y - self.camera[1]) - self.WIN_HEIGHT / 2) / self.camera_momentum)

    def render_world(self):
        """Renders the worlds Tiles"""
        chunk = self.WORLD_CHUNCK_SIZE
        tiles_with_collision = []

        def make_chunk(y: int, row: list, x: int, chunk_index: int) -> pg.draw.rect:
            """Makes a world chunk"""

            try:
                cube: int = row[chunk_index]
            except IndexError as _:
                return

            color: tuple = self.PALETTE[self.PALLETE_MAPPING[cube]]
            collision: bool = self.MAP_COLLISION_MAPPING[cube]
            # offset = self.camera_offset_right if self.camera_offset_right else 1
            # x_o = (x * (chunk + offset))
            # if x_o < 0:
            #     x_o = 0

            # if self.camera_offset_right == "LEFT":
            #     offset = - ( self.player.speed )
            # elif self.camera_offset_right == "RIGHT":
            #     offset = + (self.player.speed)

            camera_x = int(self.camera[0])
            camera_y = int(self.camera[1])

            block = pg.draw.rect(self.background, color, pg.Rect(((x * chunk) - camera_x, (y * chunk) - camera_y, chunk, chunk)))

            # if self.camera_offset_right:
            #     print(x_o)
            #
            #     if self.camera_offset_right < 0:
            #         block = block.move(x_o,  y * chunk)
            #     else:
            #         block = block.move(x_o,  y * chunk)

            if collision:
                tiles_with_collision.append(block)
            return block

        max_lenght = len(self.WORLD_MAP[0])
        # offset = 30 + self.camera_offset_right
        # if offset > max_lenght:
        #     offset = max_lenght
        # if offset < 30:
        #     offset = 30
        # min_distance = max_lenght - 30
        # start = self.camera_offset_right
        # if start < 0:
        #     start = 0
        # elif start > min_distance:
        #     start = min_distance
        #
        # diff = abs(offset) -abs(start)
        # print(f"off {offset} | start {start} diff -> {diff}")
        # if abs(diff) < 30:
        #     start -= abs(diff)
        #     print("wowowow ->", start)

        # print(start, self.camera_offset_right, offset)

        recs = [make_chunk(y, row, x, chunk_index)
                for y, row in enumerate(self.WORLD_MAP)
                for x, chunk_index in enumerate(range(0, max_lenght))
                ]

        return recs, tiles_with_collision
