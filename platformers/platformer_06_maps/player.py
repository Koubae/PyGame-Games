import pygame as pg
from pygame.math import Vector2
from typing import Optional
import effects


class Player:
    DEFAULT_COLOR: pg.Color = pg.Color("red")

    speed: int = 7
    gravity: float = .2
    air_resitance: float = .2
    gravity_max: int = 3

    def __init__(self):
        self.size: Vector2 = Vector2(64 / 4, 64)
        self.pos: Vector2 = Vector2(120, 100)
        self.pos_next: Optional[Vector2] = None
        self.rect: pg.React = pg.Rect(self.pos, self.size)

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

    def render(self, tales: list, screen, camera):
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

    def move(self, screen: pg.Surface, camera) -> None:
        """Moves entity"""
        self.player_new_pos = Vector2(self.rect.x - camera.x(), self.rect.y - camera.y())
        self.pos = self.player_new_pos
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

    def sprint_make(self, screen: pg.Surface) -> None:
        """Make Entity sprint"""
        if not self.sprint:
            return

        direction = "left" if self.move_left else "right"
        effects.make_particle_trail(direction, screen, self.player_new_pos, self.size)
