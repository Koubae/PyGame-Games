from __future__ import annotations
import pygame as pg
from typing import Tuple, Optional
from ..assets.assets_loader import loader_sprite, loader_sound


class Entity(pg.sprite.Sprite):
    DEFAULT_SPEED: int = 0  # by default entity can't move

    def __init__(self, sprite: pg.Surface, size: tuple, pos: tuple, container: pg.Rect = None, *args):
        super().__init__(*args)

        # Define Sprite image and rect and  set size
        self.image: pg.Surface = sprite
        self.rect: pg.Rect = sprite.get_rect()

        # set position and size
        self.size: tuple = size
        self.pos: tuple = pos
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.speed = self.DEFAULT_SPEED
        self.container: pg.Rect = container

    @classmethod
    def make_from_sprite(cls,
                         asset: str,
                         size: tuple,
                         pos: tuple,
                         color: Tuple[int, tuple] = -1,
                         scale: int = 1,
                         *args
                         ) -> Entity:
        """Creates a new Entity from a sprite

        :param asset:
        :param size:
        :param pos:
        :param color:
        :param scale:
        :return: Entity
        """
        return cls(loader_sprite(asset, color, scale), size, pos, *args)

    @classmethod
    def make_from_surface(cls,
                          size: tuple,
                          pos: tuple,
                          color: Optional[tuple] = None,
                          scale: int = 1,
                          *args,
                          ) -> Entity:
        """Creates a new Entity from a surface

        :param size:
        :param pos:
        :param color:
        :param scale:
        :return:
        """
        surface = pg.Surface(size)
        if not color:
            color = (0, 0, 0)
        surface.fill(color)
        return cls(surface, size, pos, *args)

    def update(self):
        """@mustinherit"""
        pass

    def move(self, step_x, step_y):
        self.rect.move_ip(step_x * self.speed, step_y * self.speed)
        if self.container:  # Clip Sprite inside container , won't go outside of it
            self.rect = self.rect.clamp(self.container)
