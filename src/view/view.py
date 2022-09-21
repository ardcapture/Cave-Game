import os
import sys

import pygame
from pygame.constants import BLEND_RGB_SUB
from src.level import Level, Surround
from src.level.level import GRID_SIZE, HEIGHT_GS, WIDTH_GS
from src.utilities import DIRECTIONS, Colors, Position
from src.view import Mouse, Tile, Window
from src.view.keyboard import Keyboard

Type_Surface = pygame.Surface

GRID_SCALE = GRID_SIZE


class View:

    IMAGES_PATH: str = "res"
    player_file = "player_tran.png"
    filename_player = os.path.join(IMAGES_PATH, player_file)
    player_key = Colors.WHITE
    player_scale = GRID_SCALE // 16

    # pygame
    pygame.init()
    clock = pygame.time.Clock()

    # grid
    grid_size_2D = (GRID_SCALE, GRID_SCALE)

    window_events = []

    run = True  # TODO CHECK WHAT IS USING

    pygame_special_flags = {"BLEND_RGB_ADD": BLEND_RGB_SUB}

    # Window
    title = "Maze Game"
    width = 35
    height = 22
    grid_size = GRID_SCALE

    def __init__(self):

        self.window = Window(
            self,
            title=self.title,
            view_width=self.width,
            view_height=self.height,
            grid_size=self.grid_size,
        )

        # self.keyboard = Keyboard()
        self.mouse = Mouse()
        self.keyboard = Keyboard()

        self.tile = Tile(GRID_SCALE)
        self.surround = Surround()

        self.player_init()

        self.pygame_fonts = {
            "MONOSPACE": self.get_pygame_fonts,
        }

        # timestep: int = 50

        self.pygame_surfaces = {
            "GRASS_IMAGE": self.get_surface_file(
                "grass.png", self.IMAGES_PATH, self.grid_size_2D
            ),
            "DIRT_IMAGE": self.get_surface_file(
                "dirt.png", self.IMAGES_PATH, self.grid_size_2D
            ),
            "ROCK_IMAGE": self.get_surface_file(
                "rock.png", self.IMAGES_PATH, self.grid_size_2D
            ),
            "WINDOW": self.window.window_surface,
            "TEXT": self.get_surface_text,
            "LIGHT": self.get_surface_lights,
        }

        self.set_window()

    #! DRAW
    def set_window(self):
        self.window.window_surface.blit(self.window.scaled_window_surface, (0, 0))

    # def setup_view_event_handlers(self):
    #     # subscribe("user_registered", handle_user_registered_event)
    #     event.subscribe("update", self.update)

    # TODO convert return to dataclass
    def update(self, level: Level, run_debug_state: bool, current_position: Position):

        self.surround_positions, self.path_adjacent = self.surround.update(
            paths=level.path_obj.paths, grid_size=GRID_SCALE
        )

        self.route_light_positions_tiles, self.tiles = self.tile.update(
            surround_positions=self.surround_positions,
            width=WIDTH_GS,
            top_offset=level.top_offset,
            path_adjacent=self.path_adjacent,
            path_obj=level.path_obj,
            grid_size=GRID_SCALE,
            height=HEIGHT_GS,
        )

        #! circle with window!
        self.window_events = self.window.get_events()
        self.window.update(self.window_events)

        self.set_window_end()

        # keyboard

        keyboard_set_position = self.keyboard.update(self)

        # mouse
        self.mouse.update(self)

        self.draw_level(level)
        # print(f"{len(self.mouse_data_list)=}")

        # for m in self.mouse_data_list:

        surface = self.window.window_surface
        mouse_motion = self.mouse.mouse_motion
        pygame_font = self.pygame_fonts["MONOSPACE"](15)

        self.draw_coordinates(
            surface,
            mouse_motion,
            pygame_font,
        )

        #!return result 01

        self.draw_water(level)

        self.set_surface_to_window(self.player_image, current_position)

        self.set_blit_objs(level.light_objs)

        self.draw_debug_start_position(level, run_debug_state)
        self.draw_debug_climb_positions(level, run_debug_state)
        self.draw_debug_ends(level, run_debug_state)
        self.draw_debug_route(level, run_debug_state)

        self.clock.tick(60)  # TODO Check what this is doing!!!

        pygame.display.update()

        return keyboard_set_position, self.mouse.mouse_event_run

    #!!!!! DRAWING OF SELF.SURFACE *****************************************************************

    def get_surface_lights(self, brightness):
        surface = pygame.Surface(self.grid_size_2D)
        pygame.draw.rect(surface, brightness, surface.get_rect())
        return surface

    def get_pygame_fonts(self, size):
        return pygame.font.SysFont("monospace", size)

    def draw_coordinates(self, surface: Type_Surface, mouse_motion, pygame_font):
        if not mouse_motion:
            return

        surface_font = pygame_font.render(str(mouse_motion.pos), 1, (Colors.RED))
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

    def set_blit_objs(self, lights):
        for obj in lights:
            self.pygame_surfaces[obj.to_surface].blit(
                self.pygame_surfaces[obj.surface](obj.color),
                obj.position,
                special_flags=self.pygame_special_flags["BLEND_RGB_ADD"],
            )

    #!!!!!! Create shape and draw?*******************************************************************************

    def draw_rect(self, color, pos):
        pygame.draw.rect(
            self.window.window_surface, color, (pos, (GRID_SCALE, GRID_SCALE))
        )

    def draw_outline(self, color, pos):
        pygame.draw.rect(
            self.window.window_surface,
            color,
            (pos, (GRID_SCALE - 1, GRID_SCALE - 1)),
            2,
        )

    def draw_climb_positions_visited(self):
        for p in self.climb_positions_visited:
            if p not in self.water_list:
                pygame.draw.rect(
                    self.window.window_surface,
                    COLORS["RED"],
                    (p[0] + GRID_SCALE * 7 / 16, p[1], GRID_SCALE / 8, GRID_SCALE),
                )

    def draw_debug_climb_positions(self, model, debug):
        if debug:
            for p in model.path.list_climb_positions:
                pygame.draw.rect(
                    self.window.window_surface,
                    COLORS["GREEN"],
                    (p[0] + GRID_SCALE * 7 / 16, p[1], GRID_SCALE / 8, GRID_SCALE),
                )

    #!!!! set draw locations???  ****************************************************************************

    def draw_debug_route(self, level, run_debug):
        if run_debug:
            for p in level.path.route:
                self.draw_outline(COLORS["GREEN"], (p[0], p[1]))

    def draw_level(self, level):
        for k, v in self.tiles.items():
            pos = k[0], k[1]
            if v == "S":
                self.draw_rect((146, 244, 255), pos)
            if v == "G":
                self.set_surface_to_surface(
                    self.pygame_surfaces["GRASS_IMAGE"],
                    self.window.window_surface,
                    pos,
                    special_flags=0,
                )
            if v == "E":
                self.set_surface_to_surface(
                    self.pygame_surfaces["DIRT_IMAGE"],
                    self.window.window_surface,
                    pos,
                    special_flags=0,
                )
            if v == "P":
                self.set_surface_to_surface(
                    self.pygame_surfaces["ROCK_IMAGE"],
                    self.window.window_surface,
                    pos,
                    special_flags=0,
                )
            if v == "A":
                # todo sometimes this key 'k' below is not present causing an error!!!
                tile01 = pygame.image.load(self.route_light_positions_tiles[k])
                tile01 = pygame.transform.scale(tile01, (GRID_SCALE, GRID_SCALE))
                self.set_surface_to_surface(
                    tile01, self.window.window_surface, pos, special_flags=0
                )

    #!!!! WATER:

    def draw_water(self, model):
        for p in model.water_datas:
            self.draw_transparent(Colors.BLUE_LIGHT, p.position)

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

    def draw_build_grid_hide(self, model, build_debug):
        if not build_debug:
            return

        directions_list = []
        for g in model.list_grid:
            for d in DIRECTIONS:
                if (
                    g[0] + (d[0] * GRID_SCALE),
                    g[1] + (d[1] * GRID_SCALE),
                ) not in model.list_wall_break_positions:
                    directions_list.append((d[0], d[1]))

            if len(directions_list) == 4:
                self.set_surface_to_surface(
                    self.pygame_surfaces["DIRT_IMAGE"],
                    self.window.window_surface,
                    g[0],
                    g[1],
                )
            directions_list.clear()

    def set_surface_to_window(self, surface, current_position):
        if not current_position:
            return

        self.set_surface_to_surface(
            surface,
            self.window.window_surface,
            (
                current_position[0] + ((GRID_SCALE - surface.get_width()) / 2),
                current_position[1] + (GRID_SCALE - surface.get_height()),
            ),
            special_flags=0,
        )

    #!!!! *********************************************************

    def get_dict_fonts(self):
        return

    def get_surface_file(self, image, path, scale):
        res = pygame.image.load(os.path.join(path, image))
        res = pygame.transform.scale(res, scale)
        return res

    @property
    def surface_load_player(self):
        filename = self.filename_player
        return pygame.image.load(filename)

    @property
    def player_image(self):

        res_get_width = self.surface_load_player.get_width() * self.player_scale
        res_get_height = self.surface_load_player.get_height() * self.player_scale

        size = (res_get_width, res_get_height)

        surface_scale = pygame.transform.scale(self.surface_load_player, size)

        return surface_scale

    def player_init(self):
        self.surface_load_player.set_colorkey(self.player_key)

    #! needs to be run?!
    def set_window_end(self):
        if self.window.window_quit:
            self.set_end()

    #! needs to be run?!
    def set_end(self):
        self.run = False
        self.window.close_window()
        sys.exit()  # TODO MOVE ELSEWHERE?
