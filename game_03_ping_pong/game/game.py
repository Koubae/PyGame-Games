import pygame as pg
import pygame.event
from typing import Optional

from .entities.padel import Padel
from .entities.ball import Ball


class Game:
    """Game Class"""
    # TODO: Make .env file or similar!
    # Game Config
    GAME_NAME: str = "Starter App"
    FRAMES: int = 60
    BALL_ZOMBIE: bool = False  # if Ball zombie is enable, the ball never ends on the horizontal axes, basically it never dies. just for fun
    BALL_MAX_SPEED: float = 20.00
    GAME_SPEED_RESET: int = 100
    GAME_SPEED_INCREASE: bool = True
    BALL_SPEED_INCREASE: float = .5
    PLAYER_1_SPEED_INCREASE: float = .3
    PLAYER_2_SPEED_INCREASE: float = .3

    # Screen config
    WIN_SIZE: tuple = (850, 550)
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

        self.entities_all: Optional[pg.RenderUpdates] = None
        self.player_1: Optional[Padel] = None
        self.player_2: Optional[Padel] = None
        self.winner: Optional[Padel] = None
        self.player_1_score: int = 0
        self.player_2_score: int = 0
        self.ball: Optional[pg.draw.circle] = None
        self.ball_speed_counter: int = 0

        self.leaderBoard = None

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

        window.blit(background, (0, 0))  # lay down background into the window
        pg.display.flip()  # render the window

        self.window = window
        self.background = background

    def game_setup(self):
        """Set-up a new Game"""
        self.winner = None
        self.entities_all: Optional[pg.RenderUpdates] = None
        self.player_1: Optional[Padel] = None
        self.player_2: Optional[Padel] = None
        self.winner: Optional[Padel] = None
        self.ball: Optional[pg.draw.circle] = None
        self.ball_speed_counter: int = 0
        self._initialize_entities()

    def _initialize_entities(self) -> None:
        """Loads entities for the level"""
        if not self.window or not self.background:
            raise Exception("Error, Game UI not initialized")
        default_font = pygame.font.get_default_font()
        font_renderer = pygame.font.Font(default_font, 18, bold=True)
        padel_color = (255, 255, 255)
        padel_width = 30
        padel_height = 200
        player_hpos = (self.WIN_HEIGHT / 2) - (padel_height / 2)
        self.entities_all = pg.sprite.RenderUpdates()

        player_xpos = 20
        self.player_1 = Padel.make_from_surface(
            (padel_width, padel_height),
            (player_xpos, player_hpos),
            padel_color,
            1,
            self.WIN_RECT
        )
        self.player_1.player = "Player 1"
        self.player_1.score = self.player_1_score
        label = font_renderer.render(f'{self.player_1_score}', True, (66, 245, 66))
        # To apply this surface to another you can do the following
        self.player_1.image.blit(
            label,  # The text to render
            (self.player_1.rect.width / 2 - 2,
             self.player_1.rect.height / 2))  # Where on the destination surface to render said font

        player_2_xpos = self.WIN_WIDTH - padel_width - player_xpos
        self.player_2 = Padel.make_from_surface(
            (padel_width, padel_height),
            (player_2_xpos, player_hpos),
            padel_color,
            1,
            self.WIN_RECT
        )
        self.player_2.player = "Player 2"
        self.player_2.score = self.player_2_score
        label = font_renderer.render(f'{self.player_2_score}', True, (203, 66, 245))
        # To apply this surface to another you can do the following
        self.player_2.image.blit(
            label,  # The text to render
            (self.player_2.rect.width / 2 - 2,
             self.player_2.rect.height / 2))  # Where on the destination surface to render said font

        self.entities_all.add(self.player_1)
        self.entities_all.add(self.player_2)

        # Set-up Ball Class
        Ball.ball_coord_x = self.WIN_WIDTH / 2
        Ball.ball_coord_y = self.WIN_HEIGHT / 2
        Ball.GAME = self
        Ball.WINDOW = self.window
        Ball.CLEAR_COLOR = self.WIN_BACKGROUND

    def game_new_round(self):
        """Makes a new game"""
        # Collect scores
        self.player_1_score = self.player_1.score
        self.player_2_score = self.player_2.score

        # Clear screen
        self.screen_clear()
        Ball.clear_ball()
        self.background.fill(self.WIN_BACKGROUND)
        # Update
        pg.display.update()
        # Reset Game
        Ball.reset()
        self.game_setup()

    # ---------------------
    #   GAME
    # ---------------------

    def run(self) -> None:
        """RUn the game"""
        if not self.entities_all or (not self.player_1 or not self.player_2):
            raise Exception("Error, Game UI not initialized")

        while self.game_on:
            if self.winner:
                self.winner.score_add()
                self.game_new_round()

            self.events()
            if not self.game_on:
                break

            self.screen_clear()
            self.game_tick()

    def events(self) -> None:
        """Handles User' events"""
        for event in pygame.event.get():

            if event.type == pygame.QUIT or (
                    event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):  # x button and esc terminates the game!
                self.game_on = False

    def screen_clear(self) -> None:
        """Clear and updates the screen"""
        # clear/erase the last drawn sprites
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
        direction_player_1 = keystates[pg.K_s] - keystates[pg.K_w]
        self.player_1.move(0, direction_player_1)
        # move player 2
        direction_player_2 = keystates[pg.K_DOWN] - keystates[pg.K_UP]
        self.player_2.move(0, direction_player_2)
        entities_dirty = self.entities_all.draw(self.window)

        # ---------------
        # Ball
        # ---------------
        self.speed_increase()  # increase speed of ball + padel
        self.ball, prev_ball = Ball.render(self.ball)  # Render and re-position the ball + bounce

        # Update screen
        # update all the sprites
        self.entities_all.update()
        self.screen_update(entities_dirty, self.ball, prev_ball)

        self.game_clock.tick(self.FRAMES)

    def speed_increase(self):
        if self.GAME_SPEED_INCREASE and Ball.ball_speed != self.BALL_MAX_SPEED:
            if self.ball_speed_counter > self.GAME_SPEED_RESET:
                Ball.ball_speed += self.GAME_SPEED_INCREASE
                self.player_1.speed += self.PLAYER_1_SPEED_INCREASE
                self.player_2.speed += self.PLAYER_2_SPEED_INCREASE
                self.ball_speed_counter = 0
            else:
                self.ball_speed_counter += 1
