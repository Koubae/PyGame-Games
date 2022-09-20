import pygame as pg
from pygame.math import Vector2
import sys
from pygame.locals import *
import random
GAME_ON = True
player_speed = 7
move_left = False
move_right = False
jump = False
jump_force = 5
jump_timer = 0.00
sprint = 0.00

gravity = .2
air_resitance = .2
gravity_max = 3
gravity_applied = 0.00


def events() -> None:
    global move_left, move_right, jump, GAME_ON, jump_timer, gravity_applied, sprint
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
                if not jump and jump_timer == 0:
                    jump = True
                    jump_timer = 0
                    gravity_applied = -jump_force
                else:
                    jump = False
            elif event.key == pg.K_LSHIFT:
                sprint = 12

        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT:
                move_left = False
            elif event.key == pg.K_RIGHT:
                move_right = False
            elif event.key == pg.K_UP or event.key == pg.K_SPACE:
                jump = False
            elif event.key == pg.K_LSHIFT:
                sprint = 0


def make_particle_trail(screen: pg.Surface, entity_pos: Vector2, enitty_size: Vector2) -> None:
    """Generates a trail of particle behind a entity Good for turbo effects

    :param screen: pg.Surface Screen where the particle is drawn
    :param entity_pos:  Vector2  x, y position coordinates
    :param enitty_size: Vector2  x, y entity size
    :return: None
    """
    particle_color: pg.Color = pg.Color("white")
    total_particle: int = 25
    particle_min_size: int = 1
    particle_max_size: int = 10
    # by increasing the number, we draw particle more far away from the entity
    # creating a trail behind it
    for particle_x_pos in range(total_particle):
        particle_y_side = (entity_pos.y + (enitty_size.y - random.randint(1, 10)))
        if move_left:
            particle_x_side = (entity_pos.x + (random.randint(1, 10) * particle_x_pos)) # depending on the player direction , draw particle on the opposite side
        else:
            particle_x_side = (entity_pos.x - (random.randint(1, 10) * particle_x_pos)) # depending on the player direction , draw particle on the opposite side
        pg.draw.circle(
            screen,
            particle_color,
            (particle_x_side, particle_y_side),
            random.randint(particle_min_size, particle_max_size)
        )



def run():
    global gravity_applied, jump_timer

    # Init
    pg.init()
    pg.display.set_caption("Platformer: Camera")
    CLOCK = pg.time.Clock()

    WIN_SIZE = (900, 600)

    WIN_WIDTH = WIN_SIZE[0]
    WIN_WIDTH_HALF = WIN_WIDTH / 2

    WIN_HEIGHT = WIN_SIZE[1] / 2
    WIN_HEIGHT_HALF = WIN_HEIGHT / 2

    window = pg.display.set_mode(WIN_SIZE, 0, 32)
    background = pg.Surface(WIN_SIZE)

    player_size = Vector2(15, 75)
    player_pos = Vector2(120, 100)
    player_rect = pg.Rect(player_pos, player_size)
    player_img = pg.Surface(player_size)
    player_img.fill(pg.Color("red"))

    # blocks
    grass = pg.Surface((50, 50))
    grass.fill(pg.Color("green"))

    ground = pg.Surface((50, 50))
    ground.fill(pg.Color("brown"))


    camera = Vector2(0, 0)
    camera_smoother = 20
    count = 0
    while GAME_ON:
        background.fill((10, 0, 25)) # re-paint
        count += 1

        if count > 50:
            count = 0
            # camera.x += 5

        # Set camera

        x = WIN_WIDTH_HALF / 2
        y = (WIN_HEIGHT_HALF / 2) + 200
        if move_left:
            x += 300
        camera_offset_x = ( player_rect.x - camera.x - (x + player_size.x / 2) ) / camera_smoother
        camera_offset_y = ( player_rect.y - camera.y - (y + player_size.y / 2) ) / camera_smoother

        # if camera_offset_x < 0:
        #     camera_offset_x = 0
        # if camera_offset_y < 0:
        #     camera_offset_y = 0
        print(f'offset x {camera_offset_x} offset y {camera_offset_y}')

        camera.x += camera_offset_x
        camera.y += camera_offset_y
        print(f'Camera = {camera}')





        # Render world
        tales = [pg.Rect(x * 50, 400, 50, 50) for x in range(150)]

        tales += [pg.Rect(3 * 50, 350, 50, 50)]
        tales += [pg.Rect(5 * 50, 350, 50, 50)]
        tales += [pg.Rect(8 * 50, 350, 50, 50)]
        tales += [pg.Rect(8 * 50, 30, 50, 50)]
        tales += [pg.Rect(8 * 50, 300, 50, 50)]

        for i, tale in enumerate(tales):
            # tale.x -= int(camera.x)
            # tale.y -= int(camera.y)


            if i % 2 == 0:
                background.blit(grass, (tale.x - int(camera.x), tale.y - int(camera.y)))
                # pg.draw.rect(background,  (25, 60, 50), tale)
            else:
                background.blit(ground,  (tale.x - int(camera.x), tale.y - int(camera.y)))
                # pg.draw.rect(background,  (175, 80, 15), tale)

        # jump
        if jump_timer:
            jump_timer -= 1

        # apply gravity to player
        gravity_applied += gravity
        if gravity_applied > gravity_max:
            gravity_applied = gravity_max


        # move player
        player_movement = Vector2(0, gravity_applied / air_resitance)

        if move_left:
            player_movement.x -= (player_speed + sprint)
        elif move_right:
            player_movement.x += (player_speed + sprint)


        # collisions
        collisions = {'top': False, 'right': False, 'bottom': False, 'left': False}
        # collision x
        player_rect.move_ip(player_movement.x, 0)
        collision_x = [t for t in tales if player_rect.colliderect(t)]
        for tile in collision_x:
            if player_movement.x > 0:
                collisions['right'] = True
                player_rect.right = tile.left
            elif player_movement.x < 0:
                collisions['left'] = True
                player_rect.left = tile.right

        # collision y
        player_rect.move_ip(0, player_movement.y)
        collision_y = [t for t in tales if player_rect.colliderect(t)]
        for tile in collision_y:
            if player_movement.y > 0:
                collisions['bottom'] = True
                player_rect.bottom = tile.top
            elif player_movement.y < 0:
                collisions['top'] = True
                gravity_applied = 0 # Cancel any jump or upper forces

                player_rect.top = tile.bottom

        # player_rect.move_ip(player_movement)
        # Render Player
        # player_rect.clamp_ip(background.get_rect()) # in order to don't make the player escape the window1
        player_new_pos = Vector2(player_rect.x - int(camera.x), player_rect.y - int(camera.y))
        background.blit(player_img, player_new_pos)
        if sprint:
            make_particle_trail(background, player_new_pos, player_size)

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
