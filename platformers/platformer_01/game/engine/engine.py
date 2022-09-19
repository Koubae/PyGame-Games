import pygame as pg

class GameEngine:

    @staticmethod
    def check_collision_points(item_a: pg.Rect, item_b: pg.Rect) -> dict:
        """Check which of the 9 points 2 rect collides with each other.

        Answers the question : Is Item A Colliding with Item b and in wich point?

        :param item_a pg.React Rect where we need to know if is colliding with wath
        :param item_b pg.React Rect where we check if item_a is colliding with
        :return dict topleft, topright, bottomleft, bottomright, midleft, midright, midtop, midbottom, center
        """
        return {
            'topleft': item_a.collidepoint(item_b.topleft),
            'topright': item_a.collidepoint(item_b.topright),

            'bottomleft': item_a.collidepoint(item_b.bottomleft),
            'bottomright': item_a.collidepoint(item_b.bottomright),

            'midleft': item_a.collidepoint(item_b.midleft),
            'midright': item_a.collidepoint(item_b.midright),
            'midtop': item_a.collidepoint(item_b.midtop),
            'midbottom': item_a.collidepoint(item_b.midbottom),
            'center': item_a.collidepoint(item_b.center),

        }

    @staticmethod
    def check_collision_sides(item_a: pg.Rect, item_b: pg.Rect) -> dict:
        """Check which SIDES 2 rect collides with each other.

        Answers the question : Is Item A Colliding with Item b and in which side?

        :param item_a pg.React Rect where we need to know if is colliding with wath
        :param item_b pg.React Rect where we check if item_a is colliding with
        :return dict dictionary with top, right, bottom, left sides
        """
        item_a_width = item_a.size[0]
        item_a_height = item_a.size[1]
        MARGIN = 5
        return {
            'top': (abs(item_a.bottom) - abs(item_b.top) - item_a_height) <= MARGIN,
            'right': ((abs(item_a.left) + item_a_width) - abs(item_b.right)) >= MARGIN,
            'bottom': (abs(item_a.top) - abs(item_b.bottom) + item_a_height) >= MARGIN,
            'left': ((abs(item_a.right) - item_a_width) - abs(item_b.left)) <= MARGIN,

        }
