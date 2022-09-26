from __future__ import annotations
from typing import Any
import pygame as pg
from pygame.math import Vector2
import sys


class EventListener:
    MOUSE_BUTTON_MAP = {
        1: 'MOUSE_LEFT',
        2: 'MOUSE_CENTRAL',
        3: 'MOUSE_RIGHT',
        4: 'WHEEL_UP',
        5: 'WHEEL_DOWN'
    }

    def __init__(self, app):
        self.app = app
        self.events: dict = {}

    def events_new(self) -> None:
        """Clear the events container"""
        self.events.clear()

    def events_listen(self):
        """Register the events
            NOTE: we could do, as an approach to listen to ALL events and not arbitrarly
            add if - else statemens for target events
        """
        self.events_new()
        for event in pg.event.get():
            if event.type == pg.QUIT or (
                    event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):  # x button and esc terminates the game!
                self.app.switch_off()
                return
            if event.type not in self.events:
                self.events[event.type] = {}

            # ............. Mouse ............. #
            if event.type == pg.MOUSEBUTTONDOWN:
                self.events[event.type][self.MOUSE_BUTTON_MAP[event.button]] = True
            # ............. Keyboard ............. #
            if event.type in (pg.KEYDOWN, pg.KEYUP):
                self.events[event.type][event.key] = True


class App:
    DEFAULT_DISPLAY: int = 0

    def __init__(self, app_name: str, app: dict, world: dict, ):
        self.app_name: str = app_name
        self.run: bool = True
        # App data
        self.clock: pg.time.Clock = app["clock"]
        self.frames: int = app["frames"]

        # world data
        self.display_info: pg.display.Info = world["display_info"]
        self.screen_size: str = world["screen_size"]
        self.screen_size_type: str = world["screen_size_type"]
        self.display_width: int = world["display_width"]
        self.display_height: int = world["display_height"]

        self.win_flags: int = 0
        self.win_size: tuple = world["win_size"]
        self.win_width: int = world["win_width"]
        self.win_height: int = world["win_height"]
        self.chunk: int = world["chunk"]

        window, background = self.create_app()

        self.window: pg.Surface = window
        self.background: pg.Surface = background

        self.event_listener: EventListener = EventListener(self)

    def create_app(self) -> tuple:
        pg.display.set_caption(self.app_name)
        # screen
        if self.screen_size == "large":
            self.win_flags = pg.NOFRAME

        window = pg.display.set_mode(self.win_size, self.win_flags, 32, display=self.DEFAULT_DISPLAY)
        background = pg.Surface(self.win_size)
        return window, background

    def switch_off(self):
        """Stops the execution of the application. Add here any clean-up """
        self.run = False
        # ... clean-up resource , close db connections etc...


# Settings
GUI_STYLES = {

    'gui': {
        'font': {
            'font_family': 'ariel',
            'font_size': 18,
            'font_color': (190, 0, 150)
        },
        'panel': {
            'background_color': (120, 0, 150, 55),
            'border_color': (120, 0, 150),
            'border_width': 2,
            'border_radius': 5,
        },
        'button': {
            'background_color': (102, 255, 178),
            'border_color': (0, 204, 102),
            'border_width': 3,
            'border_radius': 10,
        }
    }
}


class GuiPanel(pg.sprite.Sprite):

    def __init__(self, pos: Vector2, size: Vector2, app: App, screen: pg.Surface, parent: GuiPanel = None,
                 settings: dict = None,
                 *args):
        super().__init__(*args)
        self.app: App = app

        setting_panel = GUI_STYLES["gui"]["panel"]

        self.settings: dict = settings and settings or {}
        self.background_color: tuple = "background_color" in self.settings and self.settings["background_color"] or \
                                       setting_panel["background_color"]
        self.border_color: tuple = "border_color" in self.settings and self.settings["border_color"] or setting_panel[
            "border_color"]
        self.border_width: int = "border_width" in self.settings and self.settings["border_width"] or setting_panel[
            "border_width"]
        self.border_radius: int = "border_radius" in self.settings and self.settings["border_radius"] or setting_panel[
            "border_radius"]

        self.register_default_element_values()

        self.image = pg.Surface(size, pg.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

        self.screen = screen
        self.pos = pos
        self.size = size
        self.parent = parent
        self.children: pg.sprite.Group = pg.sprite.Group()

        # font
        self.font_family: str = GUI_STYLES["gui"]["font"]["font_family"]
        self.font_size: int = GUI_STYLES["gui"]["font"]["font_size"]
        self.font_color: tuple = GUI_STYLES["gui"]["font"]["font_color"]
        self.font = pg.font.SysFont(self.font_family, self.font_size)

        # events
        # Note: Event names are analogous and inspired directly by Javascript DOM Api event
        # @docs https://developer.mozilla.org/en-US/docs/Web/Events#event_listing
        self.events: dict = {
            # .... mouse .... #
            'click': [],  # click with moouse
            'mouse_enter': [],  # hover inside element
            'mouse_leave': [],  # hover away from element (make sense it entered first)
            # .... keyboard .... #
            'keydown': [],  # press a keyboard
            'keyup': [],  # release a keyboard
        }
        self.mouse_pointer = pg.SYSTEM_CURSOR_ARROW
        self.mouse_over: bool = False
        self.mouse_action: str = "NO_ACTION"
        self.element_clicked: bool = False
        self.element_clicked_timer: int = 0

    def update(self, *args, **kwargs):
        # Update self
        self.draw_background()
        self.draw_border()

        # Check events
        self._register_mouse_hover()
        # ****** Mouse Events ****** #
        self._on_mouse_leave()
        self._on_mouse_enter()
        self._on_mouse_click()

        # Update childrens
        self.children.draw(self.screen)
        self.children.update()

    def children_add(self, child: GuiPanel) -> None:
        self.children.add(child)

    def draw_background(self) -> None:
        pg.draw.rect(self.image, self.background_color,
                     pg.Rect(*self.image.get_rect().topleft, *(self.size.x, self.size.y)),
                     border_radius=self.border_radius)

    def draw_border(self) -> None:
        pg.draw.rect(self.image, self.border_color,
                     pg.Rect(*self.image.get_rect().topleft, *(self.size.x, self.size.y)),
                     width=self.border_width, border_radius=self.border_radius)

    def surface_clear(self):
        """When do it in a button click it makes a cool effect"""
        self.image.fill(self.background_color)
        self.image.fill((0, 0, 0))

    def register_default_element_values(self):
        """Register to a secondary property a value that may change in time, so by calling
            [prop_name..]_default can have back the initial value

        """

        # hold default values in memory
        self.background_color_default: tuple = self.background_color
        self.border_color_default: tuple = self.border_color
        self.border_width_default: int = self.border_width
        self.border_radius_default: int = self.border_radius

    # -----------------------
    # Events handlers
    # -----------------------

    def add_event_listener(self, event: str, listener: callable) -> Any:
        """Sets up a function that will be called whenever the specified event is delivered to the target.

        Directly insprited by Javascript wep api EventTarget.addEventListener
        @docs https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener
        :param event: str A case-sensitive string representing the event type to listen for.
        :param listener: Callable that is called when an event of the specified type occurs.
        :return:
        :raises AttributeError: when event is not in self.events dictionary as key
        """
        if event not in self.events:
            raise AttributeError(f'Event {event} not supported in events list {list(self.events.keys())}')
        # register the event
        self.events[event].append(listener)

    def _register_mouse_hover(self) -> str:
        mouse_leaved = self._is_mouse_leave()
        mouse_entered = False
        if not mouse_leaved:
            mouse_entered = self._is_mouse_enter()
        if mouse_leaved:
            self.mouse_action = "MOUSE_LEAVED"
        elif mouse_entered:
            self.mouse_action = "MOUSE_ENTERED"
        else:
            self.mouse_action = "MOUSE_LEAVED"
        return self.mouse_action

    def _is_mouse_leave(self) -> bool:
        if not self.mouse_over:
            return False
        mouse_position = pg.mouse.get_pos()
        mouse_collider = pg.Rect(*mouse_position, 1, 1)
        collision = self.rect.colliderect(mouse_collider)
        if collision:
            return False

        self.mouse_over = False
        return True

    def _is_mouse_enter(self) -> bool:
        mouse_position = pg.mouse.get_pos()
        mouse_collider = pg.Rect(*mouse_position, 1, 1)
        collision = self.rect.colliderect(mouse_collider)
        if not collision:
            return False
        self.mouse_over = True
        return True

    def _on_mouse_enter(self) -> None:
        """@ovverride"""
        if self.mouse_action != "MOUSE_ENTERED":
            return

        events = self.events['mouse_enter']
        for event in events:
            event()

    def _on_mouse_leave(self) -> None:
        """@ovverride"""
        if self.mouse_action != "MOUSE_LEAVED":
            return


        events = self.events['mouse_leave']
        for event in events:
            event()

    def _on_mouse_click(self) -> None:
        """@ovverride"""
        if self.mouse_action != "MOUSE_ENTERED":
            return
        # Did the user click ? TODO: make event for each mouse button? or should be 'callable' that checks that?
        app_events = self.app.event_listener.events
        event_click = app_events.get(pg.MOUSEBUTTONDOWN, {})
        if not event_click:  # if empty, then user did not click
            return

        events = self.events['click']
        for event in events:
            event(event_click) # call callbacks


class GuiButton(GuiPanel):
    DEFAULT_BUTTON_SIZE: Vector2 = Vector2(150, 35)

    def __init__(self, text: str, *args):
        if not args[1]:
            args = list(args)
            args[1] = self.DEFAULT_BUTTON_SIZE
        # center the entity by x
        args[0].x -= args[1].x / 2

        super().__init__(*args)

        # if style_inherit_parent is True then gets the default Settings from Parent
        if "style_inherit_parent" not in self.settings or self.settings["style_inherit_parent"] != True:
            setting_panel = GUI_STYLES["gui"]["button"]

            self.background_color: tuple = "background_color" in self.settings and self.settings["background_color"] or \
                                           setting_panel["background_color"]
            self.border_color: tuple = "border_color" in self.settings and self.settings["border_color"] or \
                                       setting_panel[
                                           "border_color"]
            self.border_radius: int = "border_radius" in self.settings and self.settings["border_radius"] or \
                                      setting_panel[
                                          "border_radius"]
            self.border_width: int = "border_width" in self.settings and self.settings["border_width"] or setting_panel[
                "border_width"]

            self.register_default_element_values()  # re-register default values

        self.text: str = text
        self.text_img = self.font.render(self.text, True, self.font_color)

        # events
        self.mouse_pointer = pg.SYSTEM_CURSOR_HAND

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)

        # check if is clicked
        if self.mouse_action == "MOUSE_ENTERED":
            events = self.app.event_listener.events
            if pg.MOUSEBUTTONDOWN in events:
                button_clicks = events[pg.MOUSEBUTTONDOWN]
                if "MOUSE_LEFT" in button_clicks:
                    self.surface_clear()  # makes the button 'light-turn off'
                    topleft = self.rect.topleft
                    # makes button go down givin the impression that is pressed
                    self.rect = self.image.get_rect().move(topleft[0], topleft[1] + 3)
                    self.element_clicked = True
                    self.element_clicked_timer = 8
        if self.element_clicked:
            if self.element_clicked_timer <= 0:
                self.element_clicked = False
                self.element_clicked_timer = 0
                topleft = self.rect.topleft
                self.rect = self.image.get_rect().move(topleft[0], topleft[1] - 3)
            else:
                self.element_clicked_timer -= 1

        # render text
        self.image.blit(self.text_img, self.text_img.get_rect(center=self.image.get_rect().center))

    def _on_mouse_enter(self):
        super()._on_mouse_enter()
        if self.mouse_action != "MOUSE_ENTERED":
            return

        pg.mouse.set_cursor(self.mouse_pointer)

        # if not the same, new lighten background was set
        if self.background_color != self.background_color_default:
            return

        # ligth-up the background color
        new_background = []
        for c in self.background_color:
            new_color = c + 75
            if new_color > 250:
                new_color = 250
            new_background.append(new_color)
        self.background_color = tuple(new_background)

        new_border_color = []
        for c in self.border_color:
            new_c = c + 75
            if new_c > 250:
                new_c = 250
            new_border_color.append(new_c)
        self.border_color = tuple(new_border_color)

    def _on_mouse_leave(self):
        super()._on_mouse_leave()
        if self.mouse_action != "MOUSE_LEAVED":
            return
        self.background_color = self.background_color_default
        self.border_color = self.border_color_default
        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)


def run():
    # pygame init
    pg.init()
    # pygame constants
    CLOCK = pg.time.Clock()
    FRAMES: int = 60

    # world
    display_info = pg.display.Info()
    DISPLAY_WIDTH = display_info.current_w
    DISPLAY_HEIGHT = display_info.current_h
    FLOOR_CHUNK = 64
    SCREEN_SIZE = ["small", "medium", "large"]
    SCREEN_SELECT = SCREEN_SIZE[1]

    SCREEN_SIZE_CALCS = ["static", "dynamic"]  # static: fix number | dynamic : calcualtes from the pc display size
    SCREEN_SIZE_TYPE = SCREEN_SIZE_CALCS[1]

    if SCREEN_SIZE_TYPE == "static":
        if SCREEN_SELECT == "large":
            WIN_WIDTH = FLOOR_CHUNK * 30  # 1920
            WIN_HEIGHT = int(FLOOR_CHUNK * 16.875)  # 1080
        elif SCREEN_SELECT == "medium":
            WIN_WIDTH = FLOOR_CHUNK * 20  # 1280
            WIN_HEIGHT = FLOOR_CHUNK * 10  # 640
        else:  # Small
            WIN_WIDTH = FLOOR_CHUNK * 10  # 640
            WIN_HEIGHT = FLOOR_CHUNK * 5  # 320
    else:
        if SCREEN_SELECT == "large":
            WIN_WIDTH = DISPLAY_WIDTH - 0
            WIN_HEIGHT = DISPLAY_HEIGHT - 0
            FLOOR_CHUNK = WIN_WIDTH / 30  # at best should be 64
        elif SCREEN_SELECT == "medium":
            WIN_WIDTH = DISPLAY_WIDTH / 1.5
            WIN_HEIGHT = DISPLAY_HEIGHT / 1.5
            FLOOR_CHUNK = WIN_WIDTH / 20
        else:  # Small
            WIN_WIDTH = DISPLAY_WIDTH / 3
            WIN_HEIGHT = DISPLAY_HEIGHT / 3.375
            FLOOR_CHUNK = WIN_WIDTH / 10

    WIN_SIZE = (WIN_WIDTH, WIN_HEIGHT)
    # pygame setup
    app = App(
        "Drawings",
        {
            'clock': CLOCK,
            'frames': FRAMES
        },
        {
            'display_info': display_info,
            'screen_size': SCREEN_SELECT,
            'screen_size_type': SCREEN_SIZE_TYPE,
            'display_width': DISPLAY_WIDTH,
            'display_height': DISPLAY_HEIGHT,

            'win_size': WIN_SIZE,
            'win_width': WIN_WIDTH,
            'win_height': WIN_HEIGHT,
            'chunk': FLOOR_CHUNK,
        })

    window = app.window
    background = app.background

    # entities

    # initialize font

    # handlers
    events_handler = app.event_listener.events_listen
    screen_clear = lambda: background.fill((0, 0, 0))
    screen_paint = lambda: window.blit(background, (0, 0))
    game_update = lambda: pg.display.update()
    game_tick = lambda: CLOCK.tick(FRAMES)

    # create gui components
    # gui components
    components_gui = pg.sprite.Group()
    # panel
    panel_left_size = Vector2(250, WIN_HEIGHT)
    panel_left = GuiPanel(Vector2(0, 0), panel_left_size, app, background, None, {})
    components_gui.add(panel_left)

    # button
    def action(event: dict):
        if 'MOUSE_LEFT' not in event:
            return
        print("Ok clicked -> event")



    button = GuiButton("New Shape", Vector2((panel_left_size.x / 2), 50), None,
                       app, panel_left.image, panel_left, {})
    button.add_event_listener("click", action)
    # add child to panel
    panel_left.children_add(button)

    while app.run:
        screen_clear()  # screen clear

        # ==============================================================================
        #                               GAME LOGIC HERE
        # ==============================================================================

        # s = pg.Surface((1000, 750),)  # the size of your rect
        # s.set_alpha(128)  # alpha level
        # s.fill((120, 0, 150))  # this fills the entire surface

        # s = pg.Surface((1000, 750), pg.SRCALPHA)  # per-pixel alpha
        # s.fill((120, 0, 150, 40))  # notice the alpha value in the color
        # background.blit(s, (0, 0))

        # pg.draw.rect(s, (120, 0, 150), (0, 0, 1000, 750))

        # border_width = 5
        # # pg.draw.rect(background, (120, 0, 120, .2), (x, y, width, height))
        # pg.draw.rect(s, pg.Color("Green"), (500-50,500-50, 50, 50), width=border_width)

        # font = pg.font.SysFont(None, 100)
        # text = font.render(f'Alpha = 40', True, (255, 255, 255))
        # background.blit(text, text.get_rect(center=background.get_rect().center))

        # background.blit(s, (0, 0))
        # square
        # pg.draw.rect(background, (255, 0, 0), pg.Rect(Vector2(155, 390), Vector2(120, 120)))
        # Rectangle
        # pg.draw.rect(background, (255, 255, 75), pg.Rect(Vector2(WIN_WIDTH / 2, WIN_HEIGHT / 2), Vector2(200, 150)))
        # # Triangle
        # pg.draw.polygon(background, (0, 255, 175), ((triangle_point_1, 25), (320, 125), (250, 390)))
        # # Circle
        # pg.draw.circle(background, (0, 255, 0), Vector2(circle_x, 200), 140)
        # # Elispe 1 ( Inside square )
        # pg.draw.ellipse(background, (50, 120, 120), pg.Rect(Vector2(155, 390), Vector2(120, 120)), 200)
        # # Elispe 2
        # pg.draw.ellipse(background, (50, 120, 120), pg.Rect(Vector2(800, 100), Vector2(99, 320)), 200)
        # # Line 1
        # pg.draw.line(background, (255, 255, 255), Vector2(850, 50), Vector2(10, 500))
        # pg.draw.line(background, (255, 255, 255), Vector2(50, 850), Vector2(500, 10))
        # # Lines
        # pg.draw.lines(background, (0, 120, 245), True, (Vector2(980, 320), Vector2(235, 560)), width=20)

        components_gui.draw(background)
        components_gui.update()

        # ==============================================================================
        # ..............................................................................
        # ==============================================================================

        # This in order
        events_handler()  # 1) Evebts
        game_update()  # 2) Update the game
        screen_paint()  # 3) Repaint the screen
        game_tick()  # 4) Wait 60 Frames

    # Do some resource clean up ...
    pg.quit()
    sys.exit(0)


if __name__ == '__main__':
    run()
