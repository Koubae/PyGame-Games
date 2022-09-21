import pygame as pg
from pygame.math import Vector2

WORLD_GRAVITY = 5
WORLD_GRAVITY_MAX = 15
FLOOR_CHUNK = 64
FLOOR_SIZE = Vector2(FLOOR_CHUNK, FLOOR_CHUNK)
FLOOR_CHUNK_COLLISION_DISTANCE = FLOOR_CHUNK * 2


class Player:

    player_size = Vector2(12, 64)
    hand_size = 5
    speed: int = 8
    jump_force: float = 20
    weight: float = 5

    # sword
    sword_color = (224, 224, 224)
    sword_thickness = 3
    sword_tilt = 0



    def __init__(self, screen: pg.Surface, start_position: Vector2):
        self.screen: pg.Surface = screen
        self.pos: Vector2 = start_position
        self.pos_new: Vector2 = start_position
        self.collisions: dict = {'top': False, 'right': False, 'bottom': False, 'left': False}

        self.img: pg.Surface = pg.Surface(self.player_size, flags=pg.SRCALPHA)
        self.img.fill((102, 255, 178))
        self.rect: pg.React = self.img.get_rect(topleft=start_position)

        self.move_left: bool = False
        self.move_right: bool = False
        self.jump: bool = False
        self.gravity_applied: float = 0

        self.attacking: bool = False
        self.attack_reach: float = 0.00

    def move(self, collision_entities: list):
        self.pos_new = Vector2(0, 0)
        self.collisions = {'top': False, 'right': False, 'bottom': False, 'left': False}

        self.gravity_apply()
        self.movement(collision_entities)

        self.screen.blit(self.img, self.rect.topleft)

        # # draw sword
        if self.attacking:
            self.sword_tilt = 18
        else:
            self.sword_tilt = 0

        if self.move_left: # left hand
            sword_position_hand = self.rect.left + -(self.hand_size * 2)
            sword_position_body_middle = self.rect.y + self.player_size.y / 2
            sword_position = Vector2(sword_position_hand, sword_position_body_middle)
            sword_size = Vector2(self.rect.x - 35 - self.sword_tilt, self.rect.y + self.sword_tilt)
            self.attack_reach = abs(sword_size.x)
        else: # right hadn
            sword_position_hand = self.rect.right + self.hand_size
            sword_position_body_middle = self.rect.y + self.player_size.y / 2
            sword_position = Vector2(sword_position_hand, sword_position_body_middle)
            sword_size = Vector2(self.rect.x + 35 + self.sword_tilt, self.rect.y + self.sword_tilt)
            self.attack_reach = abs(sword_size.x)



        pg.draw.line(self.screen, self.sword_color, sword_position, sword_size, width=self.sword_thickness)



    def movement(self, collision_entities: list):
        if self.move_left:
            self.pos_new.x -= self.speed

        elif self.move_right:
            self.pos_new.x += self.speed
        self.rect.move_ip(self.pos_new.x, 0)
        self.collision_check(collision_entities)

        if self.jump:
            # self.pos_new.y -= self.jump_force
            self.gravity_applied =  -self.jump_force * 2
        self.rect.move_ip(0, self.pos_new.y)
        self.collision_check(collision_entities, "y")

        # Update PLayer position
        self.pos = Vector2(self.rect.x, self.rect.y)

    def gravity_apply(self):
        self.gravity_applied += (self.weight + WORLD_GRAVITY)
        if self.gravity_applied > WORLD_GRAVITY_MAX:
            self.gravity_applied = WORLD_GRAVITY_MAX
        self.pos_new.y += self.gravity_applied

    def collision_check(self, collision_entities: list, direction: str = "x"):
        collided = self.rect.collidelistall(collision_entities)
        if collided:
            for index in collided:
                entity = collision_entities[index]
                if direction == "x":
                    if self.pos_new.x < 0:      # left
                        self.collisions["left"] = True
                        self.rect.left = entity.right
                    elif self.pos_new.x > 0:    # right
                        self.collisions["right"] = True
                        self.rect.right = entity.left
                    continue

                if self.pos_new.y < 0:  # top
                    self.collisions["top"] = True
                    self.rect.top = entity.bottom
                elif self.pos_new.y > 0:  # bottom
                    self.collisions["bottom"] = True
                    self.rect.bottom = entity.top


class Enemy:

    size = Vector2( FLOOR_CHUNK / 4, FLOOR_CHUNK)
    enemy_pos = Vector2(6 * FLOOR_CHUNK, FLOOR_CHUNK * 7)

    color_rest = pg.Color("green")
    color_hit = pg.Color("red")

    # sword
    sword_color = (224, 224, 224)
    sword_thickness = 3
    sword_tilt = 0



    def __init__(self, screen: pg.Surface):
        self.screen: pg.Surface = screen
        self.pos: Vector2 = self.enemy_pos

        self.img: pg.Surface = pg.Surface(self.size, flags=pg.SRCALPHA)
        self.img.fill(self.color_rest)
        self.rect: pg.React = self.img.get_rect(topleft=self.enemy_pos)

        self.is_hit: bool = False

    def render(self):
        self.screen.blit(self.img, self.rect.topleft)

    def collide(self, player: Player) -> bool:
        distance_x = abs(player.rect.x - self.rect.x)
        distance_y = abs(player.rect.y - self.rect.y)
        if distance_x < FLOOR_CHUNK_COLLISION_DISTANCE and distance_y < FLOOR_CHUNK_COLLISION_DISTANCE:
            return True
        return False

def run():
    # pygame constants
    CLOCK = pg.time.Clock()
    FRAMES: int = 60
    WIN_WIDTH = 1280
    WIN_HEIGHT = 640
    WIN_SIZE = (WIN_WIDTH, WIN_HEIGHT)

    # Sound init
    # freq, size, channel, buffsize
    pg.mixer.pre_init(44100, 16, 1, 512)

    # pygame setup
    pg.init()
    pg.display.set_caption("Drawings")

    # screen
    window = pg.display.set_mode(WIN_SIZE, 0, 32)
    background = pg.Surface(WIN_SIZE)

    # entities
    floor_tiles = [pg.Rect(x * FLOOR_CHUNK, FLOOR_CHUNK * 8, FLOOR_CHUNK, FLOOR_CHUNK) for x in range(25)]


    player_position = Vector2(FLOOR_CHUNK * 4, FLOOR_CHUNK * 4)

    # Game data
    game_data = {
        'run': True,
        'player': Player(background, player_position),
        'enemy': Enemy(background),
        'sound': {
            'player_attack': pg.mixer.Sound("sword_01_attack.wav"),
        }
    }

    # handlers
    def events_handler():

        for event in pg.event.get():
            if event.type == pg.QUIT or (
                    event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):  # x button and esc terminates the game!
                game_data["run"] = False

            if event.type == pg.KEYDOWN:
                if event.key in (pg.K_LEFT, pg.K_a):
                    game_data["player"].move_left = True
                elif event.key in (pg.K_RIGHT, pg.K_d):
                    game_data["player"].move_right = True
                elif event.key in (pg.K_UP, pg.K_SPACE):
                    game_data["player"].jump = True

            if event.type == pg.KEYUP:
                if event.key in (pg.K_LEFT, pg.K_a):
                    game_data["player"].move_left = False
                elif event.key in (pg.K_RIGHT, pg.K_d):
                    game_data["player"].move_right = False
                elif event.key in (pg.K_UP, pg.K_SPACE):
                    game_data["player"].jump = False

            # ............. Mouse ............. #
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    game_data["player"].attacking = True
                    game_data["sound"]["player_attack"].play()

            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    game_data["player"].attacking = False
                    game_data["sound"]["player_attack"].stop()

    screen_clear = lambda: background.fill((0, 0, 0))
    screen_paint = lambda: window.blit(background, (0, 0))
    game_update = lambda: pg.display.update()
    game_tick = lambda: CLOCK.tick(FRAMES)

    while game_data["run"]:
        screen_clear()  # screen clear

        # ==============================================================================
        #                               GAME LOGIC HERE
        # ==============================================================================

        # Render entities
        collision_entities = []
        for i, tile in enumerate(floor_tiles):
            img = pg.Surface(FLOOR_SIZE)
            if i % 2 == 0:
                img.fill((75, 75, 175))
            else:
                img.fill((255, 250, 60))

            background.blit(img, tile.topleft)
            distance_x = abs(game_data["player"].rect.x - tile.x)
            distance_y = abs(game_data["player"].rect.y - tile.y)
            if distance_x < FLOOR_CHUNK_COLLISION_DISTANCE and distance_y < FLOOR_CHUNK_COLLISION_DISTANCE:
                collision_entities.append(tile)

        # Render enemy
        game_data["enemy"].render()
        # Check if enemy is close enough to test the collision
        did_collide = game_data["enemy"].collide(game_data["player"])
        if did_collide:
            collision_entities.append(game_data["enemy"].rect)

        game_data["player"].move(collision_entities)

        # ==============================================================================
        # ..............................................................................
        # ==============================================================================

        # This in order
        events_handler()  # 1) Events
        game_update()  # 2) Update the game
        screen_paint()  # 3) Repaint the screen
        game_tick()  # 4) Wait 60 Frames


if __name__ == '__main__':
    run()
