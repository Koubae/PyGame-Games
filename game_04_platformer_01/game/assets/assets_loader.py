import os
from ..application import DIR_ASSETS
import pygame as pg
from typing import Union

ASSETS_SPRITES = "sprites"
ASSETS_SOUNDS = "sounds"


def loader_sprite(name: str, colorkey: Union[int, tuple] = None, scale: int = 1) -> pg.Surface:
    """Loads a Sprite in memory

    :param name: str Name of sprite to import
    :param colorkey: -1  lookup the color at the topleft pixel of the image, and use that color for the colorkey.
    else a tuple as RGB value, example (255, 255, 255)
    :param scale: int Scale of the sprite, 1 means original scale

    @throws FileNotFoundError If assets is not found
    :return:
    """
    try:
        fullname = os.path.join(DIR_ASSETS, ASSETS_SPRITES, name)
        image = pg.image.load(fullname)
    except FileNotFoundError as err:
        print(f"Error while loading sprite {name} \n {err}")
        raise err

    else:
        size = image.get_size()
        size = (size[0] * scale, size[1] * scale)
        image = pg.transform.scale(image, size)

        image = image.convert()
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pg.RLEACCEL)
        return image


class SoundDummy:
    """Dummy class that implements the pg.mixer.Sound interface
        To be used when a sound asset is not found or for testing
    """

    def play(self):
        pass


def loader_sound(name: str) -> Union[pg.mixer.Sound, SoundDummy]:
    """Loads a sound

    :param name: FIle name of the sound
     @throws FileNotFoundError If assets is not found
    :return:
    """
    if not pg.mixer or not pg.mixer.get_init():
        return SoundDummy()

    try:
        fullname = os.path.join(DIR_ASSETS, ASSETS_SOUNDS, name)
        sound = pg.mixer.Sound(fullname)
    except FileNotFoundError as err:
        print(f"Error while loading sound {name} \n {err}")
        raise err

    return sound
