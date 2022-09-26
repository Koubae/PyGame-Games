import pygame as pg
from pygame.math import Vector2


def run():
    # pygame constants
    CLOCK = pg.time.Clock()
    FRAMES: int = 60
    WIN_WIDTH = 1280
    WIN_HEIGHT = 640
    WIN_SIZE = (WIN_WIDTH, WIN_HEIGHT)

    # pygame setup
    pg.init()
    pg.display.set_caption("Drawings")

    # screen
    window = pg.display.set_mode(WIN_SIZE, 0, 32)
    background = pg.Surface(WIN_SIZE)

    # entities
    FLOOR_CHUNK = 64
    FLOOR_SIZE = Vector2(FLOOR_CHUNK, FLOOR_CHUNK)
    floor_tiles = [pg.Rect(x * FLOOR_CHUNK, FLOOR_CHUNK *  8, FLOOR_CHUNK, FLOOR_CHUNK) for x in range(25)]

    # Game data
    game_data = {
        'run': True
    }

    # handlers
    def events_handler():

        for event in pg.event.get():
            if event.type == pg.QUIT or (
                    event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):  # x button and esc terminates the game!
                game_data["run"] = False

    screen_clear = lambda: background.fill((0, 0, 0))
    screen_paint = lambda: window.blit(background, (0, 0))
    game_update = lambda: pg.display.update()
    game_tick = lambda: CLOCK.tick(FRAMES)

    # entities
    player_size = Vector2(12*4, FLOOR_CHUNK*4)
    player_position = Vector2(WIN_WIDTH / 2 - (player_size.x / 2), WIN_HEIGHT / 2 - (player_size.y / 2))
    player = pg.Surface(player_size, flags=pg.SRCALPHA)

    player_rect = player.get_rect(topleft=player_position)

    mouth_elispe = True
    animation = ["close", "semi_open", "open", "semi_open"]
    animation_index = 0

    rounded_shape = True

    c = 0

    while game_data["run"]:
        screen_clear()  # screen clear

        if c > 5:
            c = 0
            animation_index += 1
            if animation_index > len(animation) - 1:
                animation_index = 0
        else:
            c += 1
        # ==============================================================================
        #                               GAME LOGIC HERE
        # ==============================================================================

        # Render entities
        # for i, tile in enumerate(floor_tiles):
        #     img = pg.Surface(FLOOR_SIZE)
        #     if i % 2 == 0:
        #         img.fill((75, 75, 175))
        #     else:
        #         img.fill((255, 250, 60))
        #
        #     background.blit(img, tile.topleft)

        # draw humanoid player
        if rounded_shape:
            pg.draw.rect(player, pg.Color("green"), (0, 0, *player_size), border_radius=5)
        else:
            player.fill(pg.Color("green"))


        # .... Eyes .... #
        # left
        pg.draw.circle(player, pg.Color("white"), (player.get_rect().topleft[0] + 15, player.get_rect().topleft[1] + 15), 12)
        pg.draw.circle(player, pg.Color("black"),
                       (player.get_rect().topleft[0] + 15, player.get_rect().topleft[1] + 15), 5)
        # right
        pg.draw.circle(player, pg.Color("white"), (player.get_rect().topright[0] - 15, player.get_rect().topright[1] + 15), 12)
        pg.draw.circle(player, pg.Color("black"), (player.get_rect().topright[0] - 15, player.get_rect().topright[1] + 15), 5)

        # .... face .... #
        # mouth
        pr = player.get_rect()
        animation_current = animation[animation_index]
        print(animation_current, animation_index)



        if animation_current == 'semi_open':
            pg.draw.ellipse(player, pg.Color("red"),
                            pg.Rect(
                                Vector2(pr.topleft[0] + 10, pr.topright[1] + 35),
                                Vector2(pr.topright[0] - 20, pr.topright[1] + 20)
                            ), 50)
            pg.draw.ellipse(player, pg.Color("black"),
                            pg.Rect(
                                Vector2(pr.topleft[0] + 13, pr.topright[1] + 37),
                                Vector2(pr.topright[0] - 25, pr.topright[1] + 16)
                            ), 38)

        elif animation_current == 'open':

            pg.draw.circle(player, pg.Color("red"),
                           (player.get_rect().top + player.get_rect().width / 2, player.get_rect().top + 45), 15)
            pg.draw.circle(player, pg.Color("black"),
                           (player.get_rect().top + player.get_rect().width / 2, player.get_rect().top + 45), 12)
        else:
            pg.draw.ellipse(player, pg.Color("red"),
                            pg.Rect(
                                Vector2(pr.topleft[0] + 10, pr.topright[1] + 35),
                                Vector2(pr.topright[0] - 20, pr.topright[1] + 10)
                            ), 50)
            pg.draw.ellipse(player, pg.Color("black"),
                            pg.Rect(
                                Vector2(pr.topleft[0] + 13, pr.topright[1] + 37),
                                Vector2(pr.topright[0] - 25, pr.topright[1] + 6)
                            ), 38)

        pg.draw.ellipse(background, (50, 120, 120), pg.Rect(Vector2(155, 390), Vector2(120, 120)), 200)

        background.blit(player, player_rect.topleft)
        # ==============================================================================
        # ..............................................................................
        # ==============================================================================

        # This in order
        events_handler()    # 1) Evebts
        game_update()       # 2) Update the game
        screen_paint()      # 3) Repaint the screen
        game_tick()         # 4) Wait 60 Frames


if __name__ == '__main__':
    run()
