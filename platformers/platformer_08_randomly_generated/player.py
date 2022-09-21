import pygame as pg
from pygame.math import Vector2
from typing import Optional
import effects


class Player:
    DEFAULT_COLOR: pg.Color = pg.Color("yellow")
    SHAPES: list = ["rectangle", "circle"]
    SHAPE: str = SHAPES[1]
    BLEND_ADD: bool = False

    speed: int = 25
    gravity: float = .2
    air_resitance: float = .2
    gravity_max: int = 3

    # Attack
    attack_reach: int = 80
    attack_strength: int = 15

    def __init__(self, max_l: float, max_t: float):
        self.size: Vector2 = Vector2(64 / 2, 64 / 2)
        self.pos: Vector2 = Vector2(120, 100)
        self.pos_next: Optional[Vector2] = None
        self.rect: pg.React = pg.Rect(self.pos, self.size)

        self.max_l: float = max_l
        self.max_t: float = max_t

        if self.SHAPE == 'circle':
            self.img: pg.Surface = pg.Surface(self.size, flags=pg.SRCALPHA)
            pg.draw.circle(self.img, self.DEFAULT_COLOR, self.img.get_rect().center, 64 / 4)
        elif self.SHAPE == 'rectangle':
            self.img: pg.Surface = pg.Surface(self.size)
            self.img.fill(self.DEFAULT_COLOR)
        else:
            self.img: pg.Surface = pg.Surface(self.size)
            self.img.fill(self.DEFAULT_COLOR)

        self.move_left: bool = False
        self.move_right: bool = False
        self.jump: bool = False
        self.jump_force: int = 5
        self.jump_timer: float = 0.00
        self.sprint: float = 0.00
        self.gravity_applied: float = 0.00
        self.collisions: dict = {'top': False, 'right': False, 'bottom': False, 'left': False}

        self.attacking: bool = False

    def render(self, tales: list, screen, camera, enemy):
        # jump
        self.jump_timer_decrease()
        # apply gravity to player
        self.apply_gravity()
        # prepare player movement
        player_movement = self.move_calculate()
        # calcualte collision
        self.collision_calculate(player_movement, tales)
        # Render Player
        self.move(screen, camera)

        # .........
        # Player abilities
        # .........
        # Sprint
        self.sprint_make(screen)
        self.on_attack(enemy)

    def move(self, screen: pg.Surface, camera) -> None:
        """Moves entity"""

        self.player_new_pos = Vector2(self.rect.x - camera.x(), self.rect.y - camera.y())

        # if self.pos.x < 0:
        #     self.player_new_pos.x = 0
        # elif self.pos.x / 64 > self.max_l - 64:
        #     self.player_new_pos.x -= self.rect.x - camera.x()

        # if self.pos.y < 0:
        #     self.player_new_pos.y = 0
        # elif self.pos.y / 64 > self.max_t - 64:
        #     self.player_new_pos.y -= self.rect.y - camera.y()

        self.pos = self.player_new_pos
        if self.BLEND_ADD:
            screen.blit(self.img, self.player_new_pos, special_flags=pg.BLEND_ADD)
        else:
            screen.blit(self.img, self.player_new_pos)

    def move_calculate(self) -> Vector2:
        """Calculates the next Player movement"""
        player_movement = Vector2(0, self.gravity_applied / self.air_resitance)

        if self.move_left:
            player_movement.x -= (self.speed + self.sprint)
        elif self.move_right:
            player_movement.x += (self.speed + self.sprint)

        return player_movement

    def jump_timer_decrease(self) -> None:
        """Decrease the jump time"""
        if self.jump_timer:
            self.jump_timer -= 1

    def apply_gravity(self) -> None:
        """Applies Gravity to Player"""
        self.gravity_applied += self.gravity
        if self.gravity_applied > self.gravity_max:
            self.gravity_applied = self.gravity_max

    def collision_calculate(self, player_movement: Vector2, tales: list):
        """CAlcualte entity collision"""
        # reset - collisions
        self.collisions = {'top': False, 'right': False, 'bottom': False, 'left': False}
        # collision x
        self.rect.move_ip(player_movement.x, 0)
        collision_x = [t for t in tales if self.rect.colliderect(t)]
        for tile in collision_x:
            if player_movement.x > 0:
                self.collisions['right'] = True
                self.rect.right = tile.left
            elif player_movement.x < 0:
                self.collisions['left'] = True
                self.rect.left = tile.right

        # collision y
        self.rect.move_ip(0, player_movement.y)
        collision_y = [t for t in tales if self.rect.colliderect(t)]
        for tile in collision_y:
            if player_movement.y > 0:
                self.collisions['bottom'] = True
                self.rect.bottom = tile.top
            elif player_movement.y < 0:
                self.collisions['top'] = True
                self.gravity_applied = 0  # Cancel any jump or upper forces
                self.rect.top = tile.bottom

    # -----------------
    # Abilities | Actions
    # -----------------

    def sprint_make(self, screen: pg.Surface) -> None:
        """Make Entity sprint"""
        if not self.sprint:
            return

        direction = "left" if self.move_left else "right"
        effects.make_particle_trail(direction, screen, self.player_new_pos, self.size)

    def on_attack(self, enemey):
        if not self.attacking:
            return
        self.attacking = False  # prevent the attack to go on multiple times

        # get enemy position
        enemy_rect: pg.Rect = enemey.rect

        entity_center_pos = Vector2(enemy_rect.center)
        self_center_pos = Vector2(self.rect.center)
        diff_x = abs(self_center_pos.x - entity_center_pos.x)

        if diff_x <= self.attack_reach:
            enemey.attack_timer = self.attack_strength
            enemey.img.fill(enemey.COLOR_ATTACK)
