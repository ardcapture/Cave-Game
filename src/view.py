import os
import sys
from typing import TYPE_CHECKING

import pygame
from pygame import Surface
from pygame.constants import BLEND_RGB_SUB

from src import pygame_surface_maker

# from src.input import Keyboard
from src.Level import Level
from src.Surround import Surround
from src.Tile import Tile
from src.utilities import BlitData, Colors, Positions
from src.Window import Window

if TYPE_CHECKING:
    from src.Nav import Nav
    from src.Game import Game
    from src.Lights import Lights
    from src.WaterFactory import WaterFactory

WINDOW_CLOSE = pygame.WINDOWCLOSE


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

    def setup(self, level: "Level"):
        self.player_scale = level.GRID_SIZE // 16

        self.window = Window(self, level)

        self.tile = Tile(level.GRID_SIZE)
        self.surround = Surround()

        self.player_init()

        self.pygame_fonts = {"MONOSPACE": self.get_pygame_fonts}

    @property
    def filename_player(self):
        path = self.PATH_IMAGES
        paths = "player_tran.png"
        return os.path.join(path, paths)

    # TODO convert return to dataclass
    def update(self, game: "Game", level: Level, paths: "Nav", window: "Window"):

        self.clear_blit_list()

        # update surround:

        # TODO level.path should not be here?!
        self.surround.update(level)
        self.path_adjacent = self.surround.path_adjacent
        self.poss_surround_positions = self.surround.poss_surround_positions

        # update tile:
        self.tile.create_tile_locations(level)
        self.route_light_positions_tiles = self.tile.set_path_surround_tiles(self)
        self.tiles = self.tile.create_dict_tiles(self, level)

        # update window:
        self.window.update()

        # more stuff!:
        self.set_window_end(self.window)

        #! DRAW WINDOW START
        self.draw_level(level, window)  # blit (via set_surface_to_surface)

        self.draw_coordinates(self.window)  # append list_blit

        self.draw_water(level.water)  # append list_blit

        self.set_surface_to_window(
            self.window, level, paths
        )  # blit (via set_surface_to_surface)

        self.set_blit_objs(level, level.lights)  # append list_blit

        if game.run_debug_state:
            self.in_list_climb_positions(paths, level)  # append list_blit
            self.draw_debug_start_position(level)  # draw rect (via draw_outline)
            self.draw_debug_ends(level)  # blit
            self.draw_debug_route(level)  # draw rect (via draw_outline)

        # self.if_debug(game, level, paths)

        self.Blit(self.list_DataBlit, window)  # run list_blit
        #! DRAW WINDOW END

        self.clock.tick(60)  # TODO Check what this is doing!!!

        pygame.display.update()

    @property
    def pygame_font(self):
        return self.pygame_fonts["MONOSPACE"](15)

    def get_pygame_fonts(self, size: int):
        name = "monospace"
        return pygame.font.SysFont(name, size)

    def get_surface_text(self, text: str, font, size):
        font = self.pygame_fonts[font](size)
        return font.render("{0}".format(text), 1, ((Colors.GREEN)))

    #! RECT > SURFACE - METHODS - START ******************
    def get_surface_lights(self, level: "Level", color):
        surface = pygame.Surface(level.GRID_SIZE_2D)
        rect = surface.get_rect()
        pygame.draw.rect(surface, color, rect)
        return surface

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

    def rect_to_surface_outline(
        self, level: "Level", color: Colors, position: Positions
    ):

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

    def draw_water(self, water: "WaterFactory"):
        for p in water.water_objects:

            rect = pygame.Rect(water.left, water.top, self.width, self.height)

            surface = p.surface()
            pygame.draw.rect(surface, water.color, rect)

            # blit data
            source = surface
            dest = p.position
            area = None  # PyGame
            special_flags = 0  # PyGame
            self.list_DataBlit.append(BlitData(source, dest, area, special_flags))

    #! RECT > SURFACE - METHODS - END *********************

    #! SURFACE > DataBlit - METHODS - START *****************

    def draw_coordinates(self, window: Window):
        if not window.m_event:
            return

        # Font > Surface
        font = self.pygame_font
        text = str(window.m_event.pos)
        antialias = True
        color = Colors.RED

        surface_font = font.render(text, antialias, color)

        # DataBlit > ListBlit
        source = surface_font
        dest = Positions(10, 10)
        area = None
        special_flags = 0

        self.list_DataBlit.append(BlitData(source, dest, area, special_flags))

    def draw_debug_ends(self, level: Level):
        for k, v in dict.items(level.nav.d_position_str):

            source = self.get_surface_text(v, "MONOSPACE", 15)
            dest = Positions(k[0] + 1, k[1] + 5)
            area = None
            special_flags = 0

            self.list_DataBlit.append(BlitData(source, dest, area, special_flags))

    def set_blit_objs(self, level: "Level", lights: "Lights"):
        for obj in lights.light_objs:

            source = self.get_surface_lights(level, obj.color)
            dest = obj.position
            area = None
            special_flags = self.pygame_special_flags["BLEND_RGB_ADD"]

            self.list_DataBlit.append(BlitData(source, dest, area, special_flags))

    def in_list_climb_positions(self, path: "Nav", level: "Level"):
        for p in level.list_climb_positions:

            source = self.get_surface_from_rect(level)
            dest = (p.x, p.y)
            area = None
            special_flags = 0

            self.list_DataBlit.append(BlitData(source, dest, area, special_flags))

    #! SURFACE > DataBlit - METHODS - END *****************

    #! Blit - METHODS - START *****************

    def set_surface_to_surface(
        self,
        surface: Surface,
        source: Surface,
        dest: Positions,
        area: bool,
        special_flags: int,
    ):

        # self.list_DataBlit.append(DataBlit(surface, source, dest, area, special_flags))

        surface.blit(source, dest, area, special_flags)

    def draw_level(self, level: "Level", window: "Window"):
        for position, v in self.tiles.items():
            pos = position[0], position[1]
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
            elif v == "E":
                surface = self.window.window_surface
                source = pygame_surface_maker.dirt_image(level)
                dest = pos
                area = None
                special_flags = 0

            elif v == "G":
                surface = self.window.window_surface
                source = pygame_surface_maker.grass_image(level)
                dest = pos
                area = None
                special_flags = 0
                surface.blit(source, dest, area, special_flags)

            elif v == "P":
                PATH_BLIT = BlitData(
                    source=pygame_surface_maker.rock_image(level),
                    dest=pos,
                    area=None,
                    special_flags=0,
                )

                self.Blit([PATH_BLIT], window)

            elif v == "S":
                self.draw_rect(level, (146, 244, 255), pos)

    def Blit(self, list_blit: list[BlitData], window: "Window"):
        surface = window.window_surface
        for l in list_blit:
            surface.blit(l.source, l.dest, l.area, l.special_flags)

    def set_surface_to_window(self, window: "Window", level: "Level", paths: "Nav"):
        if not level.player_path_position:
            return

        source = self.player_image
        surface = window.window_surface

        width = source.get_width()
        x = level.player_path_position[0] + ((level.GRID_SIZE - width) / 2)

        height = source.get_height()
        y = level.player_path_position[1] + (level.GRID_SIZE - height)

        dest = Positions(x, y)
        area = None
        special_flags = 0
        surface.blit(source, dest, area, special_flags)

    #! Blit - METHODS - END *****************

    def draw_debug_route(self, level: "Level"):
        for p in level.route:
            color = Colors.GREEN
            position = Positions(p[0], p[1])
            self.rect_to_surface_outline(level, color, position)

    def clear_blit_list(self):
        self.list_DataBlit: list[BlitData] = []

    def draw_debug_start_position(self, level: "Level"):
        p = level.paths[0]
        self.rect_to_surface_outline(level, Colors.RED, (p.x, p.y))

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

    def set_window_end(self, window: "Window"):
        if not window.m_event:
            return

        if window.m_event.state == WINDOW_CLOSE:
            self.set_end()

    #! needs to be run?!
    def set_end(self):
        self.run = False
        self.window.close_window()
        sys.exit()  # TODO MOVE ELSEWHERE?
