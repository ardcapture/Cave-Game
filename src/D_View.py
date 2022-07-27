from ast import arg
import pygame
import sys
import os
import keyboard
import mouse

from pygame.constants import BLEND_RGBA_ADD, BLEND_RGB_ADD, BLEND_RGB_SUB
from C_Model import Level


GRID_SIZE = 32
IMAGESPATH = 'res'


DIRECTIONS = [(0, 1), (-1, 0), (1, 0), (0, -1)]


COLOURS = {"BLACK": (0, 0, 0),
           "WHITE": (255, 255, 255),
           "BLACK_VERY_LIGHT": (210, 210, 210),
           "WHITE_4TH_4TH_4TH_4TH": (1, 1, 1),
           "RED": (255, 0, 0),
           "GREEN": (0, 255, 0),
           "BLUE_LIGHT": (125, 125, 255),
           "BLUE_VERY_LIGHT": (210, 210, 255)}


class Window:
    def __init__(self, title: str, width: int, height: int):

        self.grid_size = 32
        self.width, self.height = list(map(lambda x: (self.grid_size * 2) + (self.grid_size * x), [width, height]))

        pygame.display.set_caption(title)
        self.window = pygame.display.set_mode(size=(self.width * 1, self.height * 1), flags=0, depth=32)


class View:
    def __init__(self, window: Window):
        # def __init__(self, title: str, width: int, height: int, timestep: int = 50):

        self.window = window.window
        self.width = window.width
        self.height = window.height
        self.grid_size = window.grid_size
        self.grid_size_2D = (self.grid_size, self.grid_size)

        self.window_size = (self.width*1, self.height*1)

        pygame.init()
        self.clock = pygame.time.Clock()
        self.surface = pygame.Surface((self.width, self.height))  # surface in pixels

        self.current_position = (0, 0)

        self.initialize()

    def initialize(self):
        self.set_player_image()
        self.set_images()
        self.set_fonts()

    def run(self, level, run_debug_state, controller):

        # self.surface.fill((0,0,0))
        self.draw_level(level)
        self.draw_coordinates(controller.mouse.mousePos)

        self.draw_water(level)

        self.draw_player()

        self.draw_object_list(level.lights.light_objs)

        self.draw_debug_start_position(level, run_debug_state)
        self.draw_debug_climb_positions(level, run_debug_state)
        self.draw_debug_ends(level, run_debug_state)
        self.draw_debug_route(level, run_debug_state)

        self.draw_screen()

        self.clock.tick(60)  # TODO Check what this is doing!!!

        pygame.display.update()

    #!!! DRAWING OF SELF>SURFACE ON WINDOW ***********************************

    def draw_screen(self):
        surface_scaled = pygame.transform.scale(self.surface, self.window_size)

        # draw window
        self.window.blit(surface_scaled, (0, 0))

    #!!!!! DRAWING OF SELF.SURFACE *****************************************************************

    # def draw_lights(self, color, pos):
    #     surface_lights = pygame.Surface(self.grid_size_2D)
    #     pygame.draw.rect(surface_lights, color, surface_lights.get_rect())
    #     object_light = Draw_Object(surface_lights, pos, special_flags=BLEND_RGB_ADD)
    #     self.light_objs.append(object_light)
    #     # self.draw_object(object_light)

    def draw_transparent(self, color, pos):
        surface_water = pygame.Surface(self.grid_size_2D)
        surface_water.set_alpha(75)
        pygame.draw.rect(surface_water, color, surface_water.get_rect())
        self.surface.blit(surface_water, pos)

    def draw_coordinates(self, words):
        self.font = self.fonts["monospace 50"]
        words = str(words)
        text = self.font.render(words, 1, (COLOURS["RED"]))
        self.surface.blit(text, (10, 10))

    def draw_debug_ends(self, level, run_debug):
        if not run_debug:
            return
        self.font = self.fonts["monospace 15"]
        for k, v in dict.items(level.dict_path_type):
            text = self.font.render("{0}".format(v), 1, ((COLOURS["GREEN"])))
            self.surface.blit(text, (k[0] + 1, k[1] + 5))

    #!!!!! DRAW**********************************************************************************

    def draw(self, surface, pos, special_flags):
        self.surface.blit(surface, pos, special_flags=special_flags)

    def draw_object(self, obj):
        self.surface.blit(obj.surface, obj.pos, special_flags=obj.special_flags)

    def draw_object_list(self, objs):
        special_flags = BLEND_RGB_ADD
        for obj in objs:
            if obj.brightness[0] > 0:
                self.surface.blit(obj.surface, obj.pos, special_flags=special_flags)

    #!!!!!! Create shape and draw?*******************************************************************************

    def draw_rect(self, color, pos):
        pygame.draw.rect(self.surface, color, (pos, (self.grid_size, self.grid_size)))

    # def draw_circle(self, color, x, y):
    #     pygame.draw.circle(self.surface, color, (x, y), self.grid_size / 4)

    def draw_outline(self, color, pos):
        pygame.draw.rect(self.surface, color, (pos, (self.grid_size - 1, self.grid_size - 1)), 2)

    def draw_climb_positions_visited(self):
        for p in self.climb_positions_visited:
            if p not in self.water_list:
                pygame.draw.rect(self.surface, COLOURS["RED"], (p[0] + self.grid_size * 7/16, p[1], self.grid_size/8, self.grid_size))

    def draw_debug_climb_positions(self, model, run_debug):
        if run_debug:
            for p in model.list_climb_positions:
                pygame.draw.rect(self.surface, COLOURS["GREEN"], (p[0] + self.grid_size * 7/16, p[1], self.grid_size/8, self.grid_size))

    #!!!! set draw locations???  ****************************************************************************

    def draw_debug_route(self, level, run_debug):
        if run_debug:
            for p in level.list_route:
                self.draw_outline(COLOURS["GREEN"], (p[0], p[1]))

    def draw_level(self, level):
        for k, v in level.tiles.items():
            pos = k[0], k[1]
            if v == 'S':
                self.draw_rect((146, 244, 255), pos)
            if v == 'G':
                self.draw(self.images["GRASS_IMAGE"], pos, special_flags=0)
            if v == 'E':
                self.draw(self.images["DIRT_IMAGE"], pos, special_flags=0)
            if v == 'P':
                self.draw(self.images["ROCK_IMAGE"], pos, special_flags=0)
            if v == 'A':
                tile01 = pygame.image.load(level.route_light_positions_tiles[k])
                tile01 = pygame.transform.scale(tile01, (self.grid_size, self.grid_size))
                self.draw(tile01, pos, special_flags=0)

    def draw_water(self, model):
        for p in model.list_water_list:
            self.draw_transparent(COLOURS["BLUE_LIGHT"], (p[0], p[1]))

    def draw_build_grid(self, model):
        for i in model.grid:
            self.draw_rect(COLOURS["BLACK_VERY_LIGHT"], i[0], i[1])

    def draw_debug_start_position(self, model, debug):
        if debug:
            p = model.list_past_positions[0]
            self.draw_outline(COLOURS["RED"], (p[0], p[1]))

    # def draw_build_wall_break_positions(self, level, build_debug):
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
                if (g[0] + (d[0] * self.grid_size), g[1] + (d[1] * self.grid_size)) not in model.list_wall_break_positions:
                    directions_list.append((d[0], d[1]))

            if len(directions_list) == 4:
                self.draw(self.images["DIRT_IMAGE"], g[0], g[1])
            directions_list.clear()

    def draw_player(self):
        self.draw(
            self.player_image,
            (self.current_position[0] + ((self.grid_size - self.player_image.get_width())/2),
             self.current_position[1] + (self.grid_size - self.player_image.get_height())),
            special_flags=0
        )

    #!!!! *********************************************************

    def set_images(self):
        self.images = {"GRASS_IMAGE": self.return_image('grass.png', IMAGESPATH, self.grid_size_2D),
                       "DIRT_IMAGE": self.return_image('dirt.png', IMAGESPATH, self.grid_size_2D),
                       "ROCK_IMAGE": self.return_image('rock.png', IMAGESPATH, self.grid_size_2D)}

    def set_fonts(self):
        self.fonts = {"monospace 50": pygame.font.SysFont("monospace", 15),
                      "monospace 15": pygame.font.SysFont("monospace", 15)}

    def return_image(self, image, path, scale):
        res = pygame.image.load(os.path.join(path, image))
        res = pygame.transform.scale(res, scale)
        return res

    def set_player_image(self):
        player_image = pygame.image.load(os.path.join(IMAGESPATH, 'player_tran.png'))

        player_image.set_colorkey((COLOURS["WHITE"]))
        self.player_image = pygame.transform.scale(player_image, (player_image.get_width() * 2, player_image.get_height() * 2))

    def draw_reset(self):
        self.surface.fill(COLOURS["BLACK"])


class Input_Controller():
    def __init__(self, level):
        self.run = True  # TODO CHECK WHAT IS USING

        self.level = level

        self.window = Input_Window()
        self.keyboard = Input_Keyboard()
        self.mouse = Input_Mouse(GRID_SIZE)

    def events(self):
        for event in self.window.get_window_events():

            # mouse event
            self.mouse.mousePos = self.mouse.get_mouse_grid_position(self.mouse.get_mouse_position())  # returns tuple
            if event.type == self.mouse.is_mouse_button_up():
                self.mouse_event_run(self.mouse.mousePos)

            # keyboard event
            elif event.type == self.keyboard.is_key_pressed():
                res = self.keyboard.keyboard_keys[event.key]  # returns sting
                self.keyboard_event_run(res)

            # window event
            elif event.type == self.window.is_window_event_quit():
                self.end()

    def keyboard_event_run(self, res):
        if res in self.level.set_position_keys:
            self.level.set_position(res)

    def mouse_event_run(self, res: tuple):
        if res not in self.level.paths or res not in self.level.camp_positions:
            self.level.set_route(self.level.tuple_current_position, res, self.level)
            self.level.route_index = 0
            index = 1
            for i in self.level.route[self.level.route_index:]:  # TODO need breaking into steps
                index += 1
                self.level.set_position(i)
                self.route_list_index = + 1
                print("wooop", index)

    def end(self):
        self.run = False
        self.window.close_window()
        sys.exit()  # TODO MOVE ELSEWHERE?


class Input_Keyboard:
    def __init__(self):
        self.keyboard_keys = {
            pygame.K_DOWN: "K_DOWN",
            pygame.K_LEFT: "K_LEFT",
            pygame.K_UP: "K_UP",
            pygame.K_RIGHT: "K_RIGHT",
            pygame.K_BACKQUOTE: "K_BACKQUOTE"
        }

    def is_key_pressed(self):
        return pygame.KEYDOWN


class Input_Mouse:
    def __init__(self, grid_size):
        self.grid_size = grid_size

    def is_mouse_button_up(self):
        return pygame.MOUSEBUTTONUP

    def get_mouse_position(self):
        return pygame.mouse.get_pos()

    def get_mouse_grid_position(self, pos: tuple[int, int]):
        return tuple(map(lambda x: (x // self.grid_size) * self.grid_size, pos))


class Input_Window:
    def get_window_events(self):
        return pygame.event.get()

    def is_window_event_quit(self):
        return pygame.QUIT

    def close_window(self):
        pygame.quit()
