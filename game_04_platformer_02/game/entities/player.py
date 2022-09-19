import pygame as pg


class Player:
    """Represents a Player Object

    TODO: make this a parent 'Entity' object with commont behavour!
    """
    DEFAULT_SIZE: tuple = (15, 75)
    DEFAULT_POSITION: tuple = (5, 20)

    def __init__(self, view: pg.Surface, world_gravity: float, world_gravity_max: float):
        self.view: pg.Surface = view
        self.world_gravity: float = world_gravity
        self.world_gravity_max: float = world_gravity_max

        self.move_left: bool = False
        self.move_right: bool = False
        self.jumping: bool = False
        self.gravity_force_applied: float = 0.00
        self.double_jump: int = False
        self.speed: int = 5

        self.rect: pg.draw.rect = pg.Rect(self.DEFAULT_POSITION[0], self.DEFAULT_POSITION[1], self.DEFAULT_SIZE[0],
                                          self.DEFAULT_SIZE[1])

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

    def render(self, tiles_with_collision: list) -> None:
        """Render the entity

        :param tiles_with_collision: list List of pygame.Rect with collision enabled
        :return: None
        """
        player_movement = [0, 0]
        if self.move_left:
            player_movement[0] -= self.speed
        elif self.move_right:
            player_movement[0] += self.speed

        # Apply Gravity
        self.gravity_apply(player_movement)
        self.collision_detect(tiles_with_collision, player_movement)
        pg.draw.rect(self.view, pg.Color("blue"), self.rect)


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
        self.rect.x += movement_x
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
        self.rect.y += movement_y
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
        if self.rect.right > view_rect.right:
            self.rect.right = view_rect.right

        if self.rect.left < view_rect.left:
            self.rect.left = view_rect.left