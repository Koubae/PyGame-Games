from __future__ import annotations
import pygame as pg
from typing import Tuple, Optional
from ..assets.assets_loader import loader_sprite, loader_sound


class Entity(pg.sprite.Sprite):

    def __init__(self, sprite: pg.Surface, size: tuple, pos: tuple, *args):
        super().__init__(*args)

        # Define Sprite image and rect and  set size
        self.image: pg.Surface = sprite
        self.rect: pg.Rect = sprite.get_rect()

        # set position and size
        self.size: tuple = size
        self.pos: tuple = pos
        self.rect.topleft = pos

    @classmethod
    def make_from_sprite(cls,
                         asset: str,
                         size: tuple,
                         pos: tuple,
                         color: Tuple[int, tuple] = -1,
                         scale: int = 1
                         ) -> Entity:
        """Creates a new Entity from a sprite

        :param asset:
        :param size:
        :param pos:
        :param color:
        :param scale:
        :return: Entity
        """
        return Entity(loader_sprite(asset, color, scale), size, pos)

    @classmethod
    def make_from_surface(cls,
                          size: tuple,
                          pos: tuple,
                          color: Optional[tuple] = None,
                          scale: int = 1

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
        return Entity(surface, size, pos)

    def update(self):
        """@mustinherit"""
        pass
