import pygame as pg
import pygame.event

from game.entities.entity import Entity


def run():
    # TODO: Make .env file or similar!

    # Game Config
    GAME_NAME = "Starter App"
    FRAMES = 60

    # Screen config
    WIN_SIZE = (650, 500)
    WIN_BACKGROUND = (125, 125, 155)
    FULL_SCREEN = False
    COLOR_BIT = 32
    VSYNC = False  # TODO: learn what vsync does
    MOUSE_VISIBLE = True

    # Audio Config
    MIXER_PRE_INIT = True
    MIXER_CHANNELS_NUMBER = 64

    game_clock = pygame.time.Clock()
    game_on = True

    def game_setup():
        if MIXER_PRE_INIT:
            pg.mixer.pre_init(44100, -16, 2, 512)  # frequency, size, stereo (2), buffer
        pg.init()
        if MIXER_PRE_INIT and MIXER_CHANNELS_NUMBER:
            pg.mixer.set_num_channels(MIXER_CHANNELS_NUMBER)

        pg.display.set_caption(GAME_NAME)
        # TODO: Add Game icon
        # icon = ...
        # pg.display.set_icon(icon)
        pg.mouse.set_visible(MOUSE_VISIBLE)

    def window_setup():
        flags = pygame.FULLSCREEN if FULL_SCREEN else pygame.RESIZABLE
        window = pg.display.set_mode(WIN_SIZE, flags, COLOR_BIT, vsync=VSYNC)
        window.fill(WIN_BACKGROUND)
        return window

    def events():
        nonlocal game_on

        for event in pygame.event.get():

            if event.type == pygame.QUIT or (
                    event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):  # x button and esc terminates the game!
                game_on = False

    def paint():
        pygame.draw.circle(screen, (0, 0, 255), (250, 250), 120)

        sprites_all = pg.sprite.Group()

        sprites_all.add(Entity.make_from_sprite("alien1.gif",  (120, 160),  (50, 90)))
        sprites_all.add(Entity.make_from_sprite("alien1.gif", (20, 20), (130, 150)))

        sprites_all.add(Entity.make_from_surface((200, 200), (300, 200), color=(167, 255, 100)))
        return sprites_all

    def loop():

        while game_on:
            events()
            sprites_all = paint()

            sprites_all.update()
            sprites_all.draw(screen)
            pygame.display.update()
            game_clock.tick(FRAMES)

    game_setup()
    screen = window_setup()
    loop()


def play():
    try:
        run()
    except Exception as exception:
        print(exception)
    finally:
        pg.quit()


if __name__ == '__main__':
    play()
