import pygame
import sys
import os
# import keyboard
# import mouse

from pygame.constants import BLEND_RGBA_ADD, BLEND_RGB_ADD, BLEND_RGB_SUB
from Controller import Level, GRID_SIZE
from dataclasses import dataclass


GRID_SCALE = GRID_SIZE

IMAGES_PATH = 'res'


DIRECTIONS = [(0, 1), (-1, 0), (1, 0), (0, -1)]


COLORS = {
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "BLACK_VERY_LIGHT": (210, 210, 210),
    "WHITE_4TH_4TH_4TH_4TH": (1, 1, 1),
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "BLUE_LIGHT": (125, 125, 255),
    "BLUE_VERY_LIGHT": (210, 210, 255),
}


class View:
    def __init__(self, controller):

        self.controller = controller
        self.level = self.controller.level
        # self.lights = self.controller.level.lights

        # pygame
        pygame.init()
        self.clock = pygame.time.Clock()

        # grid
        self.grid_size_2D = (GRID_SCALE, GRID_SCALE)

        self.events = []

        # self.input = View_Input(self.level)

        self.player_image = self.get_surface_character(
            os.path.join(IMAGES_PATH, 'player_tran.png'),
            (COLORS["WHITE"]),
            scale=(GRID_SCALE//16)
        )

        self.pygame_fonts = {
            "MONOSPACE": self.get_pygame_fonts,
        }

        self.window = Window(title="Maze Game", width=35, height=22, grid_size=GRID_SCALE)
        # self.window = Input_Window()
        self.keyboard = Keyboard(self)
        self.mouse = Mouse()

        # window
        self.window_surface = self.window.get_scaled_window_surface()
        self.window.set_window(self.window_surface)

        # timestep: int = 50

        self.run = True  # TODO CHECK WHAT IS USING

        self.pygame_surfaces = {
            "GRASS_IMAGE": self.get_surface_file('grass.png', IMAGES_PATH, self.grid_size_2D),
            "DIRT_IMAGE": self.get_surface_file('dirt.png', IMAGES_PATH, self.grid_size_2D),
            "ROCK_IMAGE": self.get_surface_file('rock.png', IMAGES_PATH, self.grid_size_2D),
            "WINDOW": self.window.window_surface,
            "TEXT": self.get_surface_text,
            "LIGHT": self.get_surface_lights
        }

        self.pygame_special_flags = {
            "BLEND_RGB_ADD": BLEND_RGB_SUB
        }

    def update(self, level, run_debug_state, current_position):

        # self.events_all = self.event_all()

        # window:
        self.window = self.window.update(self)

        self.events = self.window.events

        self.set_window_end(self.window.window_quit)

        # keyboard
        self.keyboard = self.keyboard.update(self)

        keyboard_set_position = self.set_event_keyboard(self.keyboard)

        # mouse
        self.mouse_data_list = self.mouse.update(self)

        self.draw_level(self.level)

        for m in self.mouse_data_list:
            mouse_event_run = self.set_mouse(m)
            self.draw_coordinates(self.window.window_surface, (m.mouse_motion), self.pygame_fonts["MONOSPACE"](15))

        # self.input.event()

        self.draw_water(level)

        self.set_surface_to_window(self.player_image, current_position)

        self.set_blit_objs(level.light_objs)

        self.draw_debug_start_position(level, run_debug_state)
        self.draw_debug_climb_positions(level, run_debug_state)
        self.draw_debug_ends(level, run_debug_state)
        self.draw_debug_route(level, run_debug_state)

        self.clock.tick(60)  # TODO Check what this is doing!!!

        pygame.display.update()

        return keyboard_set_position, mouse_event_run

    #!!!!! DRAWING OF SELF.SURFACE *****************************************************************

    def get_surface_lights(self, brightness):
        surface = pygame.Surface(self.grid_size_2D)
        pygame.draw.rect(surface, brightness, surface.get_rect())
        return surface

    # def set_lights(self, color, pos):
    #     surface_lights = pygame.Surface(self.grid_size_2D)
    #     pygame.draw.rect(surface_lights, color, surface_lights.get_rect())
    #     object_light = Draw_Object(surface_lights, pos, special_flags=BLEND_RGB_ADD)
    #     self.light_objs.append(object_light)
    #     # self.draw_object(object_light)

    def get_pygame_fonts(self, size):
        return pygame.font.SysFont("monospace", size)

    def draw_coordinates(self, surface, mouse_motion, pygame_font):
        if not mouse_motion:
            return

        surface_font = pygame_font.render(str(mouse_motion["pos"]), 1, (COLORS["RED"]))
        surface.blit(surface_font, (10, 10))

    def draw_debug_ends(self, level, run_debug):
        if not run_debug:
            return

        for k, v in dict.items(level.path.path_type):

            surface = self.pygame_surfaces["TEXT"](v, "MONOSPACE", 15)

            self.window.window_surface.blit(surface, (k[0] + 1, k[1] + 5))

    #!!!!! DRAW**********************************************************************************

    def get_surface_text(self, text: str, font, size):
        font = self.pygame_fonts[font](size)
        return font.render("{0}".format(text), 1, ((COLORS["GREEN"])))

    def set_surface_to_surface(self, surface, to_surface, pos, special_flags):
        to_surface.blit(surface, pos, special_flags=special_flags)

    # def blit_object(self, obj):
    #     self.window.window_surface.blit(obj.surface, obj.pos, special_flags=obj.special_flags)

    def set_blit_objs(self, lights):
        for obj in lights:
            self.pygame_surfaces[obj.to_surface].blit(
                self.pygame_surfaces[obj.surface](obj.color),
                obj.position,
                special_flags=self.pygame_special_flags["BLEND_RGB_ADD"]
            )

    #!!!!!! Create shape and draw?*******************************************************************************

    def draw_rect(self, color, pos):
        pygame.draw.rect(self.window.window_surface, color, (pos, (GRID_SCALE, GRID_SCALE)))

    # def draw_circle(self, color, x, y):
    #     pygame.draw.circle(self.surface, color, (x, y), GRID_SCALE / 4)

    def draw_outline(self, color, pos):
        pygame.draw.rect(self.window.window_surface, color, (pos, (GRID_SCALE - 1, GRID_SCALE - 1)), 2)

    def draw_climb_positions_visited(self):
        for p in self.climb_positions_visited:
            if p not in self.water_list:
                pygame.draw.rect(self.window.window_surface, COLORS["RED"], (p[0] + GRID_SCALE * 7/16, p[1], GRID_SCALE/8, GRID_SCALE))

    def draw_debug_climb_positions(self, model, debug):
        if debug:
            for p in model.path.list_climb_positions:
                pygame.draw.rect(self.window.window_surface, COLORS["GREEN"], (p[0] + GRID_SCALE * 7/16, p[1], GRID_SCALE/8, GRID_SCALE))

    #!!!! set draw locations???  ****************************************************************************

    def draw_debug_route(self, level, run_debug):
        if run_debug:
            for p in level.path.route:
                self.draw_outline(COLORS["GREEN"], (p[0], p[1]))

    def draw_level(self, level):
        for k, v in level.tiles.items():
            pos = k[0], k[1]
            if v == 'S':
                self.draw_rect((146, 244, 255), pos)
            if v == 'G':
                self.set_surface_to_surface(self.pygame_surfaces["GRASS_IMAGE"], self.window.window_surface, pos, special_flags=0)
            if v == 'E':
                self.set_surface_to_surface(self.pygame_surfaces["DIRT_IMAGE"], self.window.window_surface, pos, special_flags=0)
            if v == 'P':
                self.set_surface_to_surface(self.pygame_surfaces["ROCK_IMAGE"], self.window.window_surface, pos, special_flags=0)
            if v == 'A':
                tile01 = pygame.image.load(level.route_light_positions_tiles[k])
                tile01 = pygame.transform.scale(tile01, (GRID_SCALE, GRID_SCALE))
                self.set_surface_to_surface(tile01, self.window.window_surface, pos, special_flags=0)

    #!!!! WATER:

    def draw_water(self, model):
        for p in model.water_datas:
            self.draw_transparent(COLORS["BLUE_LIGHT"], p.position)

    def draw_transparent(self, color, pos):
        surface_water = pygame.Surface(self.grid_size_2D)
        surface_water.set_alpha(75)
        pygame.draw.rect(surface_water, color, surface_water.get_rect())

        self.window.window_surface.blit(surface_water, pos)

    #!!!! ****************

    def draw_build_grid(self, model):
        for i in model.grid:
            self.draw_rect(COLORS["BLACK_VERY_LIGHT"], i[0], i[1])

    def draw_debug_start_position(self, model, debug):
        if debug:
            p = model.path.build_positions[0]
            self.draw_outline(COLORS["RED"], (p[0], p[1]))

        """_summary_
        """    # def draw_build_wall_break_positions(self, level, build_debug):
    #     level02 = level
    #     if build_debug:
    #         self.draw(COLOURS["BLACK_VERY_LIGHT"], level02.list_wall_break_positions[-1][0], level02.list_wall_break_positions[-1][1])
    #         pygame.display.update()
    #         pygame.time.delay(20)

    def draw_build_grid_hide(self, model, build_debug):
        if not build_debug:
            return

        directions_list = []
        for g in model.list_grid:
            for d in DIRECTIONS:
                if (g[0] + (d[0] * GRID_SCALE), g[1] + (d[1] * GRID_SCALE)) not in model.list_wall_break_positions:
                    directions_list.append((d[0], d[1]))

            if len(directions_list) == 4:
                self.set_surface_to_surface(self.pygame_surfaces["DIRT_IMAGE"], self.window.window_surface, g[0], g[1])
            directions_list.clear()

    def set_surface_to_window(self, surface, current_position):
        self.set_surface_to_surface(
            surface,
            self.window.window_surface,
            (
                current_position[0] + ((GRID_SCALE - surface.get_width())/2),
                current_position[1] + (GRID_SCALE - surface.get_height())
            ),
            special_flags=0
        )

    #!!!! *********************************************************

    def get_dict_fonts(self):
        return

    def get_surface_file(self, image, path, scale):
        res = pygame.image.load(os.path.join(path, image))
        res = pygame.transform.scale(res, scale)
        return res

    def get_surface_character(self, file, key, scale):
        player_image = pygame.image.load(file)
        player_image.set_colorkey(key)
        res = pygame.transform.scale(player_image, (player_image.get_width() * scale, player_image.get_height() * scale))
        return res

    def set_window_surface_black(self):
        self.window_surface.fill(COLORS["BLACK"])

    def set_event_keyboard(self, keyboard):
        if keyboard.keydown:
            if keyboard.keydown[1] in self.level.set_position_keys:
                return keyboard.keydown[1]

    def set_mouse(self, mouse_data):
        if mouse_data.mouse_button_up:
            position = mouse_data.mouse_button_up["pos"]
            button = mouse_data.mouse_button_up["button"]
            if button:
                return position

    def set_window_end(self, event):
        if event:
            self.set_end()

    def set_end(self):
        self.run = False
        self.window.close_window()
        sys.exit()  # TODO MOVE ELSEWHERE?


class Window:
    def __init__(self, title: str, width: int, height: int, grid_size: int):

        self.width, self.height = list(map(lambda x: (GRID_SCALE * 2) + (GRID_SCALE * x), [width, height]))

        self.window_size_scaled = self.get_window_scale(self.width, self.height, scale=1)

        pygame.display.set_caption(title)
        self.window_surface = pygame.display.set_mode(size=(self.width * 1, self.height * 1), flags=0, depth=32)

        self.events = self.get_events()

    def update(self, parent):
        events = parent.events

        self.events = self.get_events()
        self.window_quit = self.get_window_quit(events)

        return self

    def get_window_scale(self, width, height, scale: int):
        return (width * scale, height * scale)

    def get_scaled_window_surface(self):
        res = pygame.transform.scale(self.window_surface, self.window_size_scaled)
        return res

        # draw window
    def set_window(self, surface):
        self.window_surface.blit(surface, (0, 0))

    def get_window_quit(self, events):
        for e in events:
            if e.type == pygame.QUIT:
                return True

    def get_events(self):
        return pygame.event.get()

    def close_window(self):
        pygame.quit()


class Keyboard:
    def __init__(self, parent):
        pass

        self.keyboard_events = {
            pygame.K_DOWN: "K_DOWN",
            pygame.K_LEFT: "K_LEFT",
            pygame.K_UP: "K_UP",
            pygame.K_RIGHT: "K_RIGHT",
            pygame.K_BACKQUOTE: "K_BACKQUOTE"
        }

    def update(self, parent):
        self.events = parent.events

        self.keydown = self._get_keydown(self.events)
        self.keyup = self._get_keyup(self.events)

        return self

    def _get_keydown(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                return ("KEYDOWN", self.keyboard_events.get(event.key, False))

    def _get_keyup(self, events):
        for event in events:
            if event.type == pygame.KEYUP:
                return ("KEYUP", self.keyboard_events.get(event.key, False))


class Mouse:
    def __init__(self):
        pass

    def update(self, parent):
        events = parent.events

        mouse_data = Mouse_Data(
            mouse_button_up=self._get_mouse_button_up(events),
            mouse_button_down=self._get_mouse_button_down(events),
            mouse_motion=self._get_mouse_motion(events),
        )

        return [mouse_data]

    def _get_mouse_button_up(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                return {"pos": event.pos, "button": event.button}

    def _get_mouse_button_down(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                return {"pos": event.pos, "button": event.button}

    def _get_mouse_motion(self, events):
        for e in events:
            if e.type == pygame.MOUSEMOTION:
                button = False
                if any(e.buttons):
                    button = e.buttons.index(1) + 1
                return {"pos": e.pos, "button": button}


@dataclass
class Mouse_Data:
    mouse_button_up: dict
    mouse_button_down: dict
    mouse_motion: dict
