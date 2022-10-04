import os
import sys
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, NamedTuple

import pygame
from pygame import Surface
from pygame.constants import BLEND_RGB_SUB
from src import pygame_surface_maker
from src.level import Level
from src.utilities import DIRECTIONS_FOUR, Colors, Position
from src.view import Keyboard, Mouse, Surround, Tile, Window

if TYPE_CHECKING:
    from src.game import Game
    from src.level.path import Path
    from src.view.window import Window
    from src.water import Water


class DataBlit(NamedTuple):
    surface: Surface
    source: Surface
    dest: Position
    area: bool
    special_flags: int


# class DataRect:
#     def __init__(self, level: "Level") -> None:
#         self.left = level.GRID_SIZE
#         self.top: int
#         self.width: int
#         self.height: int


# DATARECT_CLIMB_POSITIONS = DataRect(
#     left=7 / 16,
#     top= 0,
#     width= 8,
#     height=0,
# )


class View:

    PATH_IMAGES: str = "res"
    player_key = Colors.WHITE

    # pygame
    pygame.init()
    clock = pygame.time.Clock()

    # window_events = []

    run = True  # TODO CHECK WHAT IS USING

    pygame_special_flags = {"BLEND_RGB_ADD": BLEND_RGB_SUB}

    # Window
    title = "Maze Game"
    width = 35
    height = 22

    def __init__(self, level: Level):

        self.player_scale = level.GRID_SIZE // 16

        self.window = Window(
            title=self.title,
            view_width=self.width,
            view_height=self.height,
            grid_size=level.GRID_SIZE,
        )

        # self.keyboard = Keyboard()
        self.mouse = Mouse()
        self.keyboard = Keyboard()

        self.tile = Tile(level.GRID_SIZE)
        self.surround = Surround()

        self.player_init()

        self.pygame_fonts = {
            "MONOSPACE": self.get_pygame_fonts,
        }

        # timestep: int = 50

        self.pygame_surfaces = {
            "GRASS_IMAGE": self.get_surface_file(
                "grass.png",
                self.PATH_IMAGES,
                level.GRID_SIZE_2D,
            ),
            "DIRT_IMAGE": self.get_surface_file(
                "dirt.png",
                self.PATH_IMAGES,
                level.GRID_SIZE_2D,
            ),
            "ROCK_IMAGE": self.get_surface_file(
                "rock.png",
                self.PATH_IMAGES,
                level.GRID_SIZE_2D,
            ),
            "WINDOW": self.window.window_surface,
            "TEXT": self.get_surface_text,
            "LIGHT": self.get_surface_lights,
        }

        # self.set_window()

    #! DRAW

    #! not sure how this is not needed
    # def set_window(self):

    #     surface = self.window.window_surface
    #     source = self.window.scaled_window_surface
    #     dest = (0, 0)
    #     area = None
    #     special_flags = 0

    #     self.list_DataBlit.append(DataBlit(surface, source, dest, area, special_flags))

    @property
    def filename_player(self):
        path = self.PATH_IMAGES
        paths = "player_tran.png"
        return os.path.join(path, paths)

    # TODO convert return to dataclass
    def update(self, game: "Game", level: Level, paths: "Path"):

        self.clear_blit_list()

        # update surround:

        # TODO level.path should not be here?!
        self.surround.update(level, level.path)
        self.path_adjacent = self.surround.path_adjacent
        self.poss_surround_positions = self.surround.poss_surround_positions

        # update tile:
        self.tile.create_tile_locations(level)
        self.route_light_positions_tiles = self.tile.set_path_surround_tiles(self)
        self.tiles = self.tile.create_dict_tiles(self, level.path)

        # update window:
        self.window_events = self.window.win_event
        self.window_quit = self.window.get_window_quit(self)

        # mouse
        self.mouse.update(self)

        # keyboard
        self.keyboard.update(self)

        # more stuff!:
        self.set_window_end()

        #! DRAW WINDOW START
        self.draw_level(level)  # blit (via set_surface_to_surface)

        self.draw_coordinates(self.window, self.mouse)  # append list_blit

        self.draw_water(self.window, level, level.water)  # append list_blit

        self.set_surface_to_window(
            self.window, level, paths
        )  # blit (via set_surface_to_surface)

        self.set_blit_objs(level)  # append list_blit

        if game.run_debug_state:
            self.in_list_climb_positions(paths, level)  # append list_blit
            self.draw_debug_start_position(level, paths)  # draw rect (via draw_outline)
            self.draw_debug_ends(level)  # blit
            self.draw_debug_route(level, paths)  # draw rect (via draw_outline)

        # self.if_debug(game, level, paths)

        self.Blit(self.list_DataBlit)  # run list_blit
        #! DRAW WINDOW END

        self.clock.tick(60)  # TODO Check what this is doing!!!

        pygame.display.update()

    #!!!!! DRAWING OF SELF.SURFACE *****************************************************************

    @property
    def pygame_font(self):
        return self.pygame_fonts["MONOSPACE"](15)

    def get_surface_lights(self, level: "Level", color):
        surface = pygame.Surface(level.GRID_SIZE_2D)
        rect = surface.get_rect()
        pygame.draw.rect(surface, color, rect)
        return surface

    def get_pygame_fonts(self, size: int):
        name = "monospace"
        return pygame.font.SysFont(name, size)

    def draw_coordinates(self, window: Window, mouse: Mouse):
        if not mouse.m_event:
            return

        # Font > Surface
        font = self.pygame_font
        text = str(mouse.m_event.pos)
        antialias = True
        color = Colors.RED

        surface_font = font.render(text, antialias, color)

        # DataBlit > ListBlit
        surface = window.window_surface
        source = surface_font
        dest = Position(10, 10)
        area = None
        special_flags = 0

        self.list_DataBlit.append(DataBlit(surface, source, dest, area, special_flags))

    def draw_debug_ends(self, level: Level):
        for k, v in dict.items(level.path.dict_position_str):

            surface = self.window.window_surface
            source = self.pygame_surfaces["TEXT"](v, "MONOSPACE", 15)
            dest = Position(k[0] + 1, k[1] + 5)
            area = None
            special_flags = 0

            self.list_DataBlit.append(
                DataBlit(surface, source, dest, area, special_flags)
            )

    #!!!!! DRAW**********************************************************************************

    def get_surface_text(self, text: str, font, size):
        font = self.pygame_fonts[font](size)
        return font.render("{0}".format(text), 1, ((Colors.GREEN)))

    def set_surface_to_surface(
        self,
        surface: Surface,
        source: Surface,
        dest: Position,
        area: bool,
        special_flags: int,
    ):

        # self.list_DataBlit.append(DataBlit(surface, source, dest, area, special_flags))

        surface.blit(source, dest, area, special_flags)

    def set_blit_objs(self, level: "Level"):
        for obj in level.light_objs:

            surface = self.pygame_surfaces[obj.to_surface]
            source = self.pygame_surfaces[obj.surface](level, obj.color)
            dest = obj.position
            area = None
            special_flags = self.pygame_special_flags["BLEND_RGB_ADD"]

            self.list_DataBlit.append(
                DataBlit(surface, source, dest, area, special_flags)
            )

    #!!!!!! Create shape and draw?*******************************************************************************

    def draw_rect(self, level: "Level", color, pos):

        surface = self.window.window_surface
        rect = (pos, (level.GRID_SIZE, level.GRID_SIZE))
        pygame.draw.rect(surface, color, rect)

    def get_surface_from_rect(self, level: "Level"):
        flag = pygame.SRCALPHA
        surface = pygame.Surface(level.GRID_SIZE_2D, flag)

        color = Colors.GREEN

        # pygame rect

        left = level.GRID_SIZE * 7 / 16
        top = 0
        width = level.GRID_SIZE / 8
        height = level.GRID_SIZE

        rect = pygame.Rect(left, top, width, height)

        pygame.draw.rect(surface, color, rect)

        return surface

    def draw_outline(self, level: "Level", color: Colors, position: Position):

        #  pygame rect
        left = position[0]
        top = position[1]
        width = level.GRID_SIZE - 1
        height = level.GRID_SIZE - 1

        rect_02 = pygame.Rect(left, top, width, height)

        # pygame draw rect
        surface = self.window.window_surface
        width_02 = 2
        pygame.draw.rect(surface, color, rect_02, width_02)

    def in_list_climb_positions(self, path: "Path", level: "Level"):
        for p in path.list_climb_positions:

            source = self.get_surface_from_rect(level)
            surface = self.window.window_surface
            dest = (p.x, p.y)
            area = None
            special_flags = 0

            self.list_DataBlit.append(
                DataBlit(surface, source, dest, area, special_flags)
            )

    #!!!! set draw locations???  ****************************************************************************

    def draw_debug_route(self, level: "Level", path: "Path"):
        for p in level.route:
            color = Colors.GREEN
            position = Position(p[0], p[1])
            self.draw_outline(level, color, position)

    def draw_level(self, level):
        for position, v in self.tiles.items():
            pos = position[0], position[1]
            if v == "S":
                self.draw_rect(level, (146, 244, 255), pos)
            if v == "G":

                surface = self.window.window_surface
                source = pygame_surface_maker.grass_image(level)
                dest = pos
                area = None
                special_flags = 0
                surface.blit(source, dest, area, special_flags)

            if v == "E":
                surface = self.window.window_surface
                source = pygame_surface_maker.dirt_image(level)
                dest = pos
                area = None
                special_flags = 0

            if v == "P":
                PATH_BLIT = DataBlit(
                    surface=self.window.window_surface,
                    source=pygame_surface_maker.rock_image(level),
                    dest=pos,
                    area=None,
                    special_flags=0,
                )

                self.Blit([PATH_BLIT])

            if v == "A":
                # todo sometimes this key 'k' below is not present causing an error!!!
                tile01 = pygame.image.load(self.route_light_positions_tiles[position])
                tile01 = pygame.transform.scale(
                    tile01, (level.GRID_SIZE, level.GRID_SIZE)
                )
                self.set_surface_to_surface(
                    self.window.window_surface,
                    tile01,
                    pos,
                    area=None,
                    special_flags=0,
                )

    #!!!! WATER:

    def draw_water(self, window: Window, level: "Level", water: "Water"):
        for p in water.water_positions:

            surface_alpha = pygame.Surface(level.GRID_SIZE_2D)
            value = 75
            surface_alpha.set_alpha(value)

            color = Colors.BLUE_LIGHT
            # rect = surface_alpha.get_rect()
            left = 0
            top = 0
            width = level.GRID_SIZE
            height = level.GRID_SIZE
            rect = pygame.Rect(left, top, width, height)
            pygame.draw.rect(surface_alpha, color, rect)

            surface = window.window_surface
            source = surface_alpha
            dest = p
            area = None
            special_flags = 0
            self.list_DataBlit.append(
                DataBlit(surface, source, dest, area, special_flags)
            )

    def clear_blit_list(self):
        self.list_DataBlit: list[DataBlit] = []

    def Blit(self, list_blit: list[DataBlit]):
        for l in list_blit:
            l.surface.blit(l.source, l.dest, l.area, l.special_flags)

    #!!!! ****************

    def draw_debug_start_position(self, level: "Level", path: "Path"):
        p = path.paths[0]
        self.draw_outline(level, Colors.RED, (p.x, p.y))

    def set_surface_to_window(self, window: "Window", level: "Level", paths: "Path"):
        if not paths.player_path_position:
            return

        source = self.player_image
        surface = window.window_surface

        width = source.get_width()
        x = paths.player_path_position[0] + ((level.GRID_SIZE - width) / 2)

        height = source.get_height()
        y = paths.player_path_position[1] + (level.GRID_SIZE - height)

        dest = Position(x, y)
        area = None
        special_flags = 0
        surface.blit(source, dest, area, special_flags)

    #!!!! *********************************************************

    def get_surface_file(self, paths, path, size):
        filename = os.path.join(path, paths)
        surface = pygame.image.load(filename)
        return pygame.transform.scale(surface, size)

    @property
    def surface_load_player(self):
        filename = self.filename_player
        return pygame.image.load(filename)

    @property
    def player_image(self):
        surface = self.surface_load_player
        x = surface.get_width() * self.player_scale
        y = surface.get_height() * self.player_scale
        size = (x, y)
        return pygame.transform.scale(surface, size)

    def player_init(self):
        color = self.player_key
        self.surface_load_player.set_colorkey(color)

    def set_window_end(self):
        if not self.window_quit:
            return

        self.set_end()

    #! needs to be run?!
    def set_end(self):
        self.run = False
        self.window.close_window()
        sys.exit()  # TODO MOVE ELSEWHERE?
