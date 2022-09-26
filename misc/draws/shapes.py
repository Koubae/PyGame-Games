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
    player_leg_length = player_size.y / 4
    player_body = Vector2(player_size.x, player_size.y - player_leg_length)
    player_position = Vector2(WIN_WIDTH / 2 - (player_size.x / 2), WIN_HEIGHT / 2 - (player_size.y / 2))
    player = pg.Surface(player_size, flags=pg.SRCALPHA)

    player_rect = player.get_rect(topleft=player_position)

    mouth_elispe = True

    # animation face
    animation_face = ["close", "semi_open", "open", "semi_open"]
    animation_face_index = 0

    # animation arms
    # animation_arms = ["left", "rest", "right"] # make a middle 'rest' ?
    animation_arms = ["left", "right"]
    animation_arms_index = 0
    # animation legs
    animation_leg = ["left", "right"]
    animation_leg_index = 0

    rounded_shape = True

    animation_counter_face = 0
    animation_counter_arms = 0
    animation_counter_leg = 0

    while game_data["run"]:
        screen_clear()  # screen clear

        # Animation counters

        if animation_counter_face > 5:
            animation_counter_face = 0
            animation_face_index += 1
            if animation_face_index > len(animation_face) - 1:
                animation_face_index = 0
        else:
            animation_counter_face += 1

        if animation_counter_arms > 15:
            animation_counter_arms = 0
            animation_arms_index += 1
            if animation_arms_index > len(animation_arms) - 1:
                animation_arms_index = 0
        else:
            animation_counter_arms += 1

        if animation_counter_leg > 15:
            animation_counter_leg = 0

            animation_leg_index += 1
            if animation_leg_index > len(animation_leg) - 1:
                animation_leg_index = 0
        else:
            animation_counter_leg += 1
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
            pg.draw.rect(player, pg.Color("green"), (0, 0, *player_body), border_radius=5)
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
        animation_face_current = animation_face[animation_face_index]
        if animation_face_current == 'semi_open':
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

        elif animation_face_current == 'open':

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

        # Note: IN order for this to work, the player surface HAS DO BE blitted to the target screen
        # why? Because, the 'extemities' arent really attached to the body, byt rather painted directly on
        # the background, BUT using the plaer coordinates which are valid only once are painted in screen
        background.blit(player, player_rect.topleft)
        
        # # .... arms .... #

        animation_arms_current = animation_arms[animation_arms_index]
        if animation_arms_current == "left":
            # .... left arm (lifted -back) .... #
            arm_left = pg.Surface(Vector2(10, player_body.y / 2), pg.SRCALPHA)
            pg.draw.rect(arm_left, pg.Color("orange"), pg.Rect(
                (arm_left.get_rect().topleft[0], arm_left.get_rect().topleft[1]),
                Vector2(10, player_body.y / 2 - 16)
            ), border_radius=5)
            arm_left = pg.transform.rotate(arm_left, -8)
            background.blit(arm_left, Vector2(player_rect.topleft[0] - 22, player_rect.topleft[1] + player_body.y / 4))
            # .... right arm (lifted front) .... #
            arm_left = pg.Surface(Vector2(10, player_body.y / 2), pg.SRCALPHA)
            pg.draw.rect(arm_left, pg.Color("orange"), pg.Rect(
                (arm_left.get_rect().topleft[0], arm_left.get_rect().topleft[1]),
                Vector2(10, player_body.y / 2 - 8)
            ), border_radius=5)
            arm_left = pg.transform.rotate(arm_left, -2)
            background.blit(arm_left, Vector2(player_rect.topright[0] -5, player_rect.topright[1] + player_body.y / 4))

        elif animation_arms_current == "right":
            # .... left arm (lifted front) .... #
            arm_left = pg.Surface(Vector2(10, player_body.y / 2), pg.SRCALPHA)
            pg.draw.rect(arm_left, pg.Color("orange"), pg.Rect(
                (arm_left.get_rect().topleft[0], arm_left.get_rect().topleft[1]),
                Vector2(10, player_body.y / 2 - 8)
            ), border_radius=5)
            arm_left = pg.transform.rotate(arm_left, +2)
            background.blit(arm_left, Vector2(player_rect.topleft[0] - 5, player_rect.topleft[1] + player_body.y / 4))

            # .... right arm (lifted -back) .... #
            arm_left = pg.Surface(Vector2(10, player_body.y / 2), pg.SRCALPHA)
            pg.draw.rect(arm_left, pg.Color("orange"), pg.Rect(
                (arm_left.get_rect().topleft[0], arm_left.get_rect().topleft[1]),
                Vector2(10, player_body.y / 2 - 16)
            ), border_radius=5)
            arm_left = pg.transform.rotate(arm_left, +8)
            background.blit(arm_left, Vector2(player_rect.topright[0], player_rect.topright[1] + player_body.y / 4))
        else: # rest
            # .... left arm (normal) .... #
            arm_left = pg.Surface(Vector2(10, player_body.y / 2), pg.SRCALPHA)
            pg.draw.rect(background, pg.Color("orange"), pg.Rect(
                Vector2(player_rect.topleft[0] - 10, player_rect.topleft[1] + player_body.y / 4),
                Vector2(10, player_body.y / 2)
            ), border_radius=5)
            background.blit(arm_left, player_rect.topleft)

            # .... right arm (normal) .... #
            arm_left = pg.Surface(Vector2(10, player_body.y / 2), pg.SRCALPHA)
            pg.draw.rect(background, pg.Color("orange"), pg.Rect(
                Vector2(player_rect.topright[0] , player_rect.topright[1] + player_body.y / 4),
                Vector2(10, player_body.y / 2)
            ), border_radius=5)
            background.blit(arm_left, player_rect.topright)



        # arm_left = pg.Surface(Vector2(10, player_body.y / 2), pg.SRCALPHA)
        # pg.draw.rect(background, pg.Color("orange"), pg.Rect(
        #     Vector2(player_rect.topleft[0] - 10, player_rect.topleft[1] + player_body.y / 4),
        #     Vector2(10, player_body.y / 2)
        # ), border_radius=5)
        # background.blit(arm_left, player_rect.topleft)
        #
        # arm_left = pg.Surface(Vector2(10, player_body.y / 2), pg.SRCALPHA)
        # pg.draw.rect(arm_left, pg.Color("orange"), pg.Rect(
        #     (arm_left.get_rect().topleft[0], arm_left.get_rect().topleft[1]),
        #     Vector2(10, player_body.y / 2)
        # ), border_radius=5)
        # arm_left = pg.transform.rotate(arm_left, -8)
        # background.blit(arm_left, Vector2(player_rect.topleft[0] - 20, player_rect.topleft[1] + player_body.y / 4))


        # left_sur = pg.Surface(Vector2(10, player_leg_length-5 ), pg.SRCALPHA)
        # left_sur.fill((0, 0, 255))
        # left_sur = pg.transform.rotate(left_sur, -5)
        # rect = left_sur.get_rect(topright=Vector2(player_rect.left + 5, player_rect.centery + (player_leg_length )))
        # background.blit(left_sur, rect.topleft)

        # background.blit(left_sur,  Vector2(player_rect.left + 5, player_rect.centery + player_leg_length))


        # .... legs .... #
        # Some sketch code
        # Sketch: working fine but not movement,
        # pg.draw.rect(background, pg.Color("blue"), pg.Rect( ##  left
        #     Vector2(player_rect.left + 5,player_rect.centery + player_leg_length),
        #     Vector2(10, player_leg_length)
        # ), border_radius=5)
        #
        # pg.draw.rect(background, pg.Color("blue"), pg.Rect( ## right
        #     Vector2(player_rect.right - 15, player_rect.centery + player_leg_length),
        #     Vector2(10, player_leg_length)
        # ), border_radius=5)
        # also (right)

        # Implementation with surface

        # left_leg = pg.Surface(Vector2(10, player_leg_length ), pg.SRCALPHA)
        # left_leg.fill((0, 0, 255))
        # pg.draw.rect(background, pg.Color("blue"), pg.Rect(
        #     Vector2(player_rect.left + 5, player_rect.centery + player_leg_length),
        #     Vector2(10, player_leg_length)
        # ), border_radius=5)
        # background.blit(left_leg, player_rect.topleft)

  

        animation_leg_current = animation_leg[animation_leg_index]
        if animation_leg_current == "right":
            leg_left_length = player_leg_length - 8
            leg_right_length = player_leg_length
        else:
            leg_left_length = player_leg_length
            leg_right_length = player_leg_length - 8


        # left leg (lifetd)
        left_leg = pg.Surface(Vector2(10, player_leg_length), pg.SRCALPHA)
        pg.draw.rect(background, pg.Color("blue"), pg.Rect(
            Vector2(player_rect.left + 5, player_rect.centery + player_leg_length),
            Vector2(10, leg_left_length)
        ), border_radius=5)
        background.blit(left_leg, player_rect.topleft)

        # right leg (normal)
        right_leg = pg.Surface(Vector2(10, player_leg_length), pg.SRCALPHA)
        pg.draw.rect(background, pg.Color("blue"), pg.Rect(
            Vector2(player_rect.right - 15, player_rect.centery + player_leg_length),
            Vector2(10, leg_right_length)
        ), border_radius=5)
        background.blit(right_leg, player_rect.topleft)


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
