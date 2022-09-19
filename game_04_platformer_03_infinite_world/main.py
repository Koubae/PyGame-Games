"This app is broken"
import pygame as pg
import traceback

from game.game import Game

MINIMUM_PYGAME_VERSION: int = 2

def play():
    if pg.get_sdl_version()[0] < MINIMUM_PYGAME_VERSION:
        print(f"Error While opening the Game | Pygame versio {pg.get_sdl_version()[0]}, required 2 or above")
        exit(1) # TODO: make a error-pop-up ???

    try:
        game = Game()
        game.run()
    except Exception as exception:
        print(repr(exception))
        traceback.print_exc()
    finally:
        pg.quit()


if __name__ == '__main__':
    play()
