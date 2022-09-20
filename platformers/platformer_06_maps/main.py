import pygame as pg
from pygame.math import Vector2
from player import Player
from camera import Camera2D
import csv


def load_map():
    MAP_NAME = "map.csv"

    map_struct = []
    with open(MAP_NAME, 'r') as map_csv:
        csv_reader = csv.reader(map_csv, delimiter=',')
        for row in csv_reader:
            map_struct.append([int(cell) for cell in row])

    return map_struct


def run():
    # Init
    pg.init()
    pg.display.set_caption("Platformer: Camera")
    CLOCK = pg.time.Clock()
    TILE_SIZE = 64
    TILE_WIDTH = TILE_SIZE * 20  # 1280
    TILE_HEIGHT = TILE_SIZE * 10  # 640

    MAP_LENGTH = 20  # The visible map length
    MAP_TALL = 10  # THe Visible Map tall
    MAP_LENGTH_TOTAL = MAP_LENGTH * 20  # The total map legnth
    MAP_TALL_TOTAL = MAP_TALL * 4  # The Total Map hegith

    TILE_MAX_COLLISION = TILE_SIZE * 2 # distance where the collision from a entity should be check

    WIN_SIZE = (TILE_WIDTH, TILE_HEIGHT)
    WIN_WIDTH = WIN_SIZE[0]
    WIN_WIDTH_HALF = WIN_WIDTH / 2
    WIN_HEIGHT = WIN_SIZE[1] / 2
    WIN_HEIGHT_HALF = WIN_HEIGHT / 2
    window = pg.display.set_mode(WIN_SIZE, 0, 32)
    background = pg.Surface(WIN_SIZE)

    # map
    map_level = load_map()
    # blocks
    blocks = {
        -1: {  # cloud
            'img': pg.Surface((TILE_SIZE, TILE_SIZE)),
            'color': pg.Color("white"),
            'collision': True
        },
        0: {  # empty
            'img': pg.Surface((TILE_SIZE, TILE_SIZE)),
            'color': pg.Color("black"),
            'collision': False
        },

        # ground blocks
        1: {  # ground
            'img': pg.Surface((TILE_SIZE, TILE_SIZE)),
            'color': pg.Color("brown"),
            'collision': True
        },
        2: {  # grass
            'img': pg.Surface((TILE_SIZE, TILE_SIZE)),
            'color': pg.Color("green"),
            'collision': True
        },
        3: {  # rock
            'img': pg.Surface((TILE_SIZE, TILE_SIZE)),
            'color': pg.Color("grey"),
            'collision': True
        },
        4: {  # water
            'img': pg.Surface((TILE_SIZE, TILE_SIZE)),
            'color': pg.Color("blue"),
            'collision': True # TODO: make water effect?
        },
    }

    TERRAIN_LABELS = {
        -1: "cloud",
        0: "empty",

        # ground blocks
        1: "ground",
        2: "grass",
        3: "rock",
        4: "water",
    }

    # fill blocks
    for block in blocks.values():
        block_color = block['color']
        block['img'].fill(block_color)

    # Plaer
    player = Player()

    # CAMERA
    camera = Camera2D(player, WIN_WIDTH_HALF, WIN_HEIGHT_HALF)
    GAME_ON = True

    def events():
        nonlocal GAME_ON
        for event in pg.event.get():

            if event.type == pg.QUIT or (
                    event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):  # x button and esc terminates the game!
                GAME_ON = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    player.move_left = True
                elif event.key == pg.K_RIGHT:
                    player.move_right = True
                elif event.key == pg.K_UP or event.key == pg.K_SPACE:
                    if not player.jump and player.jump_timer == 0:
                        player.jump = True
                        player.jump_timer = 0
                        player.gravity_applied = -player.jump_force
                    else:
                        player.jump = False
                elif event.key == pg.K_LSHIFT:
                    player.sprint = 12

            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT:
                    player.move_left = False
                elif event.key == pg.K_RIGHT:
                    player.move_right = False
                elif event.key == pg.K_UP or event.key == pg.K_SPACE:
                    player.jump = False
                elif event.key == pg.K_LSHIFT:
                    player.sprint = 0

    def generate_world() -> list:
        """Generates a World adding its talese in multidimensional array by its tall"""

        tales = []
        for height_index, row in enumerate(map_level):
            tale_rows = []
            for width_index, col in enumerate(row):
                block_type = blocks[col]
                # get the block
                block = block_type['img']
                rect = pg.Rect(width_index * TILE_SIZE, height_index * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                # add it to the screen
                background.blit(block, rect.topleft)
                block_id = f"{height_index}-{width_index}"
                tale_struct = {
                    'terrain': col,
                    'terrain_label': TERRAIN_LABELS[col],
                    'block_id': block_id,
                    'height_index': height_index,
                    'width_index': width_index,
                    'img': block,
                    'rect': rect,
                    'collision': False
                }
                # has Collision?
                if block_type['collision']:
                    tale_struct['collision'] = True
                tale_rows.append(tale_struct)
            tales.append(tale_rows)

        return tales

    def render_world(world: list):
        """Render the world in chunks"""
        tales_with_collisions = []

        cell_count = 0

        # ------------
        #  Chunk Loader
        # ------------
        # | In order to laod a chunk of the world map we need to follow this algorithm
        # | 1) Get Player position
        # | 2) Calculate the block index by deviding x-y coordinates by the Tile px sixe. Also a margin is added
        # | 3) Get the current off x -y block index
        # | 4) Get the max block index on the view chunk by adding the MAP_TALL|MAP_LENGTH + some margin
        # | 5) Iterate through row line (by its tall)
        # | 6) Iterate through col line (by its lenght)
        # | 7) Move The camera accordingly

        view_margin: int = 10 #  arbitrary additional 'padding' to add in the camera view. so that the actual block rendered is bigger than the camera
        player_pos = Vector2(player.rect.topleft) # | 1) Get Player position
        block_position_index = Vector2((player_pos.x / TILE_SIZE) - view_margin, (player_pos.y / TILE_SIZE) - view_margin) # | 2) Calculate the block index

        block_length_index = int(block_position_index.x)  # | 3) Get the current off x -y block index
        block_height_index = int(block_position_index.y)
        block_length_index = 0 if block_length_index < 0 else block_length_index
        block_height_index = 0 if block_height_index < 0 else block_height_index
        # | 4) Get the max block index on the view chunk by adding the MAP_TALL|MAP_LENGTH + some margin
        block_length_index_max = int(block_position_index.x + MAP_LENGTH + view_margin)
        block_height_index_max = int(block_position_index.y + MAP_TALL + view_margin )

        for height_index, row in enumerate(world[block_height_index:block_height_index_max]):  # | 5) Iterate through row line (by its tall)
            for width_index, block_data in enumerate(row[block_length_index:block_length_index_max]):  # | 6) Iterate through col line (by its lenght)

                cell_count += 1
                block_img: pg.Surface = block_data['img']
                block_rect: pg.Rect = block_data['rect']  # | 7) Move The camera accordingly
                block_pos_updated = Vector2(block_rect.x - camera.x(), block_rect.y - camera.y())
                # add it to the screen
                background.blit(block_img, block_pos_updated)
                if block_data['collision']:

                    # Check if block is close enugh to entity to check the collision
                    # by loading collisions only if are close enough to the entity
                    player_position = player.pos
                    diff_x = abs(block_pos_updated.x - player_position.x)
                    diff_y = abs(block_pos_updated.y - player_position.y)
                    if diff_x < TILE_MAX_COLLISION and diff_y < TILE_MAX_COLLISION:
                        tales_with_collisions.append(block_rect)

        return tales_with_collisions


    world = generate_world()

    while GAME_ON:
        # background.fill((10, 0, 25))  # re-paint
        background.fill((200,200,200))  # re-paint

        camera.calcualte_len_position(player.move_left)

        # Render world
        tales_with_collisions = render_world(world)

        player.render(tales_with_collisions, background, camera)
        # Events
        events()

        # Debug Stats
        font = pg.font.SysFont("Arial", 15, bold=True)
        chunk_x = camera.x() / 64
        chunk_y = camera.y() / 64
        p_pos = player.rect
        font_img = font.render(f'S={camera.x()},{camera.y()} C={chunk_x},{chunk_y} Player position -> {p_pos.topleft}', True, pg.Color("red"))
        background.blit(font_img, (350, 10))

        window.blit(background, (0, 0))
        pg.display.update()
        CLOCK.tick(60)


if __name__ == '__main__':
    run()
