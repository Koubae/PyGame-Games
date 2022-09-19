import pygame as pg
from typing import List
from pygame.math import Vector2

class Player:
    """Represents a Player Object

    TODO: make this a parent 'Entity' object with commont behavour!
    """
    DEFAULT_SIZE: tuple = (15, 75)
    DEFAULT_POSITION: tuple = (5, 20)
    DEFAULT_PLAYER_COLOR: pg.Color = pg.Color("blue")

    def __init__(self, view: pg.Surface, world_gravity: float, world_gravity_max: float, camera: Vector2):
        self.view: pg.Surface = view
        self.world_gravity: float = world_gravity
        self.world_gravity_max: float = world_gravity_max

        self.move_left: bool = False
        self.move_right: bool = False
        self.jumping: bool = False
        self.gravity_force_applied: float = 0.00
        self.double_jump: int = False
        self.speed: int = 5

        self.rect: pg.draw.rect = pg.Rect(
            self.DEFAULT_POSITION[0],
            self.DEFAULT_POSITION[1],
            self.DEFAULT_SIZE[0],
            self.DEFAULT_SIZE[1]
        )
        self.pos: Vector2 = Vector2(5, 20)
        self.vel = Vector2(0, 0)

        self.img = pg.Surface((15, 75))
        self.img.fill(self.DEFAULT_PLAYER_COLOR)
        self.camera: Vector2 = camera


    # --------------------
    #   User' Event
    # --------------------
    def change_direction(self, event: pg.event) -> None:
        """Sends signal to entity to move at next Frame

        :param event: pg.even
        :return: None
        """
        if event.key == pg.K_LEFT:
            self.move_left = False
        elif event.key == pg.K_RIGHT:
            self.move_right = False

    def jump(self) -> None:
        """Makes the player jump"""
        if not self.gravity_force_applied >= 3 or self.double_jump:
            return

        if self.jumping and self.double_jump:
            return  # Player can double jump only once
        elif self.jumping and not self.double_jump:  # Double Jump
            self.double_jump = True
            self.gravity_force_applied = -12
        elif not self.jumping and not self.double_jump:  # Normal Jump
            self.jumping = True
            self.gravity_force_applied = -10


    # --------------------
    #  Rendering and Animations
    # --------------------

    def update(self):
        # Move the player.
        self.pos += self.vel
        # self.rect.center = self.pos

    def render(self, o) -> None:
        # self.view.blit(self.img, (self.rect.x , self.rect.y))
        t = self.rect.topleft
        # a = [t[0] - int(self.camera[0]), t[1] - int(self.camera[1])]
        self.view.blit(self.img, t + o)
        # self.pos = self.rect.center


    def movement_process(self, tiles_with_collision: list) -> None:
        """Render the entity

        :param tiles_with_collision: list List of pygame.Rect with collision enabled
        :return: None
        """
        player_movement = [0, 0]
        if self.move_left:
            player_movement[0] -= self.speed
            self.vel.x = -self.speed
        elif self.move_right:
            player_movement[0] += self.speed
            self.vel.x = self.speed

        # Apply Gravity
        self.gravity_apply(player_movement)
        self.collision_detect(tiles_with_collision, player_movement)


    def move_x(self, movement_x: float) -> None:
        """Move Entity in X Axis (left - right)

        :param movement_x: float X movement negative is left positive right
        :return:
        """

        self.rect.x += movement_x
        # self.pos.x = movement_x

    def move_y(self, movement_y: float) -> None:
        """Move Entity in Y Axis (up - down)

        :param movement_y: float X movement negative is Up positive Down
        :return:
        """
        self.rect.y += movement_y
        # self.pos.y = movement_y

    def gravity_apply(self, player_movement: list) -> None:
        """Applies gravity to the Player"""
        player_movement[1] += self.gravity_force_applied
        self.gravity_force_applied += self.world_gravity
        if self.gravity_force_applied > self.world_gravity_max:
            self.gravity_force_applied = self.world_gravity_max

    def collision_detect(self, tiles_with_collision: list, player_movement: list) -> None:
        """Detects entity collision

        :param tiles_with_collision: list list of pygame.Rect with collision enabled
        :param player_movement: list [x, y] player movements
        :return: None
        """
        # TODO:
        # 1. Improve this
        # 2. DO we really need to iterate 2 times???
        # 3. Refactor this
        # 4. Find a better algorithm
        # Move player
        movement_x = player_movement[0]
        movement_y = player_movement[1]

        # Move X Axis and check left-right collisions
        self.move_x(movement_x)
        # self.move_x(movement_x - camera_x)
        collided = [tile for tile in tiles_with_collision if self.rect.colliderect(tile)]
        if collided:
            for tile in collided:
                if movement_x > 0:
                    self.rect.right = tile.left
                elif movement_x < 0:
                    self.rect.left = tile.right

        self.collision_view_walls()

        # Move Y Axis and check top-bottom collisions
        # TODO: Make collision mapping
        self.move_y(movement_y)
        collided = [tile for tile in tiles_with_collision if self.rect.colliderect(tile)]
        if collided:
            for tile in collided:
                if movement_y > 0:
                    self.rect.bottom = tile.top
                    self.jumping = False
                    self.double_jump = False
                    self.gravity_force_applied = 3.00

                elif movement_y < 0:
                    self.rect.top = tile.bottom


    def collision_view_walls(self):
        """Collides with left and right wall of the window and re-set the player so that cannot transpas"""
        # Check left - right movement
        view_rect: pg.draw.rect = self.view.get_rect()
        if self.rect.right > view_rect.right + (view_rect.right - self.camera[0]):
            self.rect.right = view_rect.right

        if self.rect.left < view_rect.left:
            self.rect.left = view_rect.left