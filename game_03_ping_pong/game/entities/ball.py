from __future__ import annotations
from typing import Optional, Tuple
import pygame as pg
import random

from ..engine.engine import GameEngine


class Ball:
    """Represents a Ball object"""
    CLEAR_COLOR: tuple = (0, 0, 0)
    WINDOW: Optional[pg.Surface] = None
    GAME = None

    ball_diameter = 10
    ball_speed: float = 5.00
    ball_coord_x: float = 0
    ball_coord_y: float = 0
    ball_speed_x: float = random.choice((-1, 1))
    ball_speed_y: float = random.choice((-1, 1))

    def __init__(self):
        raise NotImplementedError("Ball object cannot be instanced!")

    @classmethod
    def reset(cls):
        cls.ball_diameter = 10
        cls.ball_speed: float = 5.00
        cls.ball_coord_x: float = 0
        cls.ball_coord_y: float = 0
        cls.ball_speed_x: float = random.choice((-1, 1))
        cls.ball_speed_y: float = random.choice((-1, 1))

    @classmethod
    def render(cls, current_ball: Optional[Ball] = None) -> Tuple[pg.draw.circle, Optional[pg.draw.circle]]:
        """Renders the current ball into window and clears the previous one

        :param current_ball: ?Ball the current ball that needs to be cleared
        :return: tuple with the new ball and previous one cleared
        """
        prev_ball = None

        # Check collision with Padel
        if current_ball:
            prev_ball = cls.clear_ball()

            # erase previous ball

        if cls.GAME.DEBUG_BALL_POS:
            mouse_position = pg.mouse.get_pos()
            cls.ball_coord_x = mouse_position[0]
            cls.ball_coord_y = mouse_position[1]
        else:
            # calculate speed
            cls.ball_coord_x += (cls.ball_speed_x * cls.ball_speed)
            cls.ball_coord_y += (cls.ball_speed_y * cls.ball_speed)

        cls.bounce_check(current_ball)

        # Create new ball
        ball = pg.draw.circle(
            cls.WINDOW,
            (255, 220, 240),
            (cls.ball_coord_x, cls.ball_coord_y),
            cls.ball_diameter
        )
        return ball, prev_ball

    @classmethod
    def clear_ball(cls) -> pg.draw.circle:
        """Clears the previous ball from the screen"""
        prev_ball = pg.draw.circle(
            cls.WINDOW,
            cls.CLEAR_COLOR,
            (cls.ball_coord_x, cls.ball_coord_y),
            cls.ball_diameter
        )
        return prev_ball

    @classmethod
    def collision_check(cls, item_a: pg.Rect, item_b: pg.Rect) -> bool:
        """Check if item_a collided with item_b

        :param item_a: pg.Rect
        :param item_b: pg.Rect
        :return: bool
        """
        return item_a.colliderect(item_b)

    @classmethod
    def wall_collision(cls) -> None:
        """Collision Check: 4 walls inside a window"""

        # X walls (left - right)
        if cls.ball_coord_x < 0:
            if not cls.GAME.BALL_ZOMBIE:
                cls.GAME.winner = cls.GAME.player_2
                return
            cls.bounce('wall_x_left')
            # get y coords and direction
        elif cls.ball_coord_x > cls.GAME.WIN_WIDTH:
            if not cls.GAME.BALL_ZOMBIE:
                cls.GAME.winner = cls.GAME.player_1
                return
            cls.bounce('wall_x_right')

        # Y walls (top - bottom)
        if cls.ball_coord_y < 0:
            cls.bounce('wall_y_top')
        elif cls.ball_coord_y > cls.GAME.WIN_HEIGHT:
            cls.bounce('wall_y_bottom')


    @classmethod
    def bounce_check(cls, current_ball: Optional[Ball]):
        """Checks if the ball requires a bounce in a wall or padel"""
        if current_ball:
            collided = cls.collision_check(cls.GAME.player_1.rect, cls.GAME.ball)
            if collided:
                cls.bounce('left')
            collided = cls.collision_check(cls.GAME.player_2.rect, cls.GAME.ball)
            if collided:
                cls.bounce('right')

        cls.wall_collision()

    @classmethod
    def bounce(cls, bounce_from: str) -> None:
        """Bounces the ball requires a bounce in a wall or padel. If goes out the side then terminates the round"""

        bounce_randomize_direction = lambda orientation: orientation * random.randint(0, 10)
        padel_rect = None
        # -------------- Wall Bounce
        if 'wall' in bounce_from:
            if bounce_from == 'wall_x_left':
                cls.ball_coord_y += bounce_randomize_direction(cls.ball_speed_y)
                cls.ball_coord_x = 1  # Keep ball in-game
                cls.ball_speed_x = 1
            elif bounce_from == 'wall_x_right':
                cls.ball_coord_y += bounce_randomize_direction(cls.ball_speed_y)
                cls.ball_coord_x = cls.GAME.WIN_WIDTH  # Keep ball in-game
                cls.ball_speed_x = -1
            elif bounce_from == 'wall_y_top':
                cls.ball_coord_x += bounce_randomize_direction(cls.ball_speed_x)
                cls.ball_coord_y = 1
                cls.ball_speed_y = 1
            elif bounce_from == 'wall_y_bottom':
                cls.ball_coord_x += bounce_randomize_direction(cls.ball_speed_x)
                cls.ball_coord_y = cls.GAME.WIN_HEIGHT
                cls.ball_speed_y = -1
            else:
                raise NotImplementedError(f"Error, bounce_from {bounce_from} not Implemented!")
            return
        # -------------- Padel Bounce
        elif bounce_from == 'left':
            padel_rect = cls.GAME.player_1.rect
        elif bounce_from == 'right':
            padel_rect = cls.GAME.player_2.rect
        else:
            raise NotImplementedError(f"Error, bounce_from {bounce_from} not Implemented!")

        if not padel_rect:
            raise ValueError("Error in Ball.bounce | Padel rect not found!")

        collisions = [
            key for key, collided in
                GameEngine.check_collision_sides(cls.GAME.ball, padel_rect).items() if collided
        ]

        if collisions == ['top' 'left']:
            cls.ball_speed_x = -1
            cls.ball_speed_y = -1
        elif collisions == ['top']:
            cls.ball_speed_y = -1
        elif collisions == ['top', 'right']:
            cls.ball_speed_x = 1
            cls.ball_speed_y = -1
        elif collisions == ['right']:
            cls.ball_speed_x = 1
        elif collisions == ['bottom', 'right']:
            cls.ball_speed_x = 1
            cls.ball_speed_y = 1
        elif collisions == ['bottom']:
            cls.ball_speed_y = 1
        elif collisions == ['bottom', 'left']:
            cls.ball_speed_x = -1
            cls.ball_speed_y = 1
        elif collisions == ['left']:
            cls.ball_speed_x = -1
        else:  # default bounce
            cls.ball_speed_x = -1
