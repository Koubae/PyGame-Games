import pygame as pg
from pygame.math import Vector2
import sys
from pygame.locals import *

GAME_ON = True

move_left = False
move_right = False
jump = False

def events() -> None:
    global move_left, move_right, jump, GAME_ON
    """Handles User' events"""
    for event in pg.event.get():

        if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):  # x button and esc terminates the game!
            GAME_ON = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                move_left = True
            elif event.key == pg.K_RIGHT:
                move_right = True
            elif event.key == pg.K_UP or event.key == pg.K_SPACE:
                jump = True

        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT:
                move_left = False
            elif event.key == pg.K_RIGHT:
                move_right = False
            elif event.key == pg.K_UP or event.key == pg.K_SPACE:
                jump = False

def run():
    # Init
    pg.init()
    pg.display.set_caption("Platformer: Camera")
    CLOCK = pg.time.Clock()

    WIN_SIZE = (900, 600)

    window = pg.display.set_mode(WIN_SIZE, 0, 32)
    background = pg.Surface(WIN_SIZE)

    player_rect = pg.Rect(100, 100, 5, 13)
    player_img = pg.Surface((15, 75))
    player_img.fill(pg.Color("red"))



    camera = Vector2(0, 0)
    count = 0
    while GAME_ON:
        background.fill((10, 0, 25)) # re-paint
        count += 1

        if count > 50:
            count = 0
            # camera.x += 5

        mouse_pos = pg.mouse.get_pos()
        camera.x = mouse_pos[0]
        camera.y = mouse_pos[1]

        # Render world
        world = [pg.Rect(x * 50, 550, 50, 50) for x in range(50)]
        for i, tale in enumerate(world):
            if i % 2 == 0:
                color = (25, 60, 50)
            else:
                color = (175, 80, 15)
            tale.x -= camera.x
            tale.y -= camera.y
            pg.draw.rect(background, color, tale)

        # Render Player


        # Events
        events()


        # Debug Stats
        font = pg.font.SysFont("Arial", 15, bold=True)
        font_img = font.render(f'Scoll X = {camera.x} Scroll Y = {camera.y}', True, pg.Color("red"))
        background.blit(font_img, (350, 10))

        window.blit(background, (0, 0))
        pg.display.update()
        CLOCK.tick(60)







if __name__ == '__main__':
    run()
