from src.Tile import Tile
from src.surround import Surround
from src.utilities import BlitData, Colors, Position, Color
from src.window import Window
from typing import TYPE_CHECKING
import os
import pygame
import sys
from src.TileGenerator import TileGenerator

if TYPE_CHECKING:
    from src.WaterFactory import WaterFactory
    from src.level import Level

WINDOW_CLOSE = pygame.WINDOWCLOSE


class View:
    PATH_IMAGES: str = "res"

    # pygame
    pygame.init()
    clock = pygame.time.Clock()

    run = True  # TODO CHECK WHAT IS USING

    pygame_special_flags = {"BLEND_RGB_ADD": pygame.BLEND_RGB_SUB}

    # Window
    title = "Maze Game"
    width = 35
    height = 22

    surround = Surround()

    def __init__(self, level: "Level") -> None:
        self.player_scale = level.GRID_SIZE // 16

        width = (level.GRID_SIZE * 2) + (level.GRID_SIZE * self.width)
        height = (level.GRID_SIZE * 2) + (level.GRID_SIZE * self.height)

        self.window = Window(self.title, width, height, 1, 1)
        self.tile = Tile(level)

        self.sky_V02 = TileGenerator(
            level=level,
            y_start=0,
            adjust=1,
            surface=self.imageSurface(level, "sky.png"),
        )

        self.rock_V02 = TileGenerator(
            level=level,
            y_start=0,
            adjust=1,
            surface=self.imageSurface(level, "rock.png"),
        )

        self.grass_V02 = TileGenerator(
            level=level,
            y_start=level.GRID_SIZE * (level.top_offset - 1),
            adjust=0,
            surface=self.imageSurface(level, "grass.png"),
        )

        self.surface_load_player.set_colorkey(Colors.WHITE.value)

    @property
    def filename_player(self):
        path = self.PATH_IMAGES
        paths = "player_tran.png"
        return os.path.join(path, paths)

    def update_display(self):
        pygame.display.update()

    def update_window_events(self):
        self.window.pygame_events = pygame.event.get()
        self.window.set_m_event()

    def set_route_light_positions_tiles(self, level: "Level"):
        self.route_light_positions_tiles = self.tile.set_path_surround_tiles(
            self, level
        )

    @property
    def pygame_font(self):
        return pygame.font.SysFont("monospace", 15)

    def get_surface_text(self, formatText: str) -> pygame.surface.Surface:
        font: pygame.font.Font = pygame.font.SysFont("monospace", 15)
        renderText: str = "{0}".format(formatText)
        antialias: bool = True
        return font.render(renderText, antialias, ((Colors.GREEN.value)))

    #! RECT > SURFACE - METHODS - START ******************
    def get_surface_lights(self, level: "Level", color: Color):
        surface = pygame.Surface(level.GRID_SIZE_2D)
        rect = surface.get_rect()
        pygame.draw.rect(surface, color, rect)
        return surface

    def get_surface_from_rect(self, level: "Level"):
        flag = pygame.SRCALPHA
        surface = pygame.Surface(level.GRID_SIZE_2D, flag)

        color = Colors.GREEN.value

        # pygame rect

        left = level.GRID_SIZE * 7 / 16
        top = 0
        width = level.GRID_SIZE / 8
        height = level.GRID_SIZE

        rect = pygame.Rect(left, top, width, height)

        pygame.draw.rect(surface, color, rect)

        return surface

    def rect_to_surface_outline(self, level: "Level", color: Color, position: Position):
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

            surface: pygame.surface.Surface = p.surface()
            pygame.draw.rect(surface, water.color, rect)

            # blit data
            source: pygame.surface.Surface = surface
            dest = p.position
            area = None  # PyGame
            special_flags = 0  # PyGame
            self.list_DataBlit.append(BlitData(source, dest, area, special_flags))

    #! RECT > SURFACE - METHODS - END *********************

    #! SURFACE > DataBlit - METHODS - START *****************

    def draw_coordinates(self):
        if not self.window.m_event:
            return

        # Font > Surface
        font = self.pygame_font
        text = str(self.window.m_event.pos)
        antialias = True
        color = Colors.RED.value

        surface_font = font.render(text, antialias, color)

        # DataBlit > ListBlit
        source = surface_font
        dest = Position(10, 10)
        area = None
        special_flags = 0

        self.list_DataBlit.append(BlitData(source, dest, area, special_flags))

    def draw_debug_ends(self, level: "Level"):
        for position, v in level.nav.positionInt.items():
            source: pygame.surface.Surface = self.get_surface_text(str(v))
            dest = Position(position[0] + 1, position[1] + 5)
            area = None
            special_flags = 0

            self.list_DataBlit.append(BlitData(source, dest, area, special_flags))

    def set_blit_objs(self, level: "Level"):
        for obj in level.lights.light_objs:
            source = self.get_surface_lights(level, obj.color)
            dest = obj.position
            area = None
            special_flags = self.pygame_special_flags["BLEND_RGB_ADD"]

            self.list_DataBlit.append(BlitData(source, dest, area, special_flags))

    def in_list_climb_positions(self, level: "Level"):
        for p in level.list_climb_positions:
            source = self.get_surface_from_rect(level)
            dest = Position(p.x, p.y)
            area = None
            special_flags = 0

            self.list_DataBlit.append(BlitData(source, dest, area, special_flags))

    #! SURFACE > DataBlit - METHODS - END *****************

    #! Blit - METHODS - START *****************

    def tile_adjacent(self, level: "Level", position: Position):
        surface = pygame.image.load(self.route_light_positions_tiles[position])
        return pygame.transform.scale(surface, (level.GRID_SIZE, level.GRID_SIZE))

    def draw_level(self, level: "Level"):
        TILE_LETTERS = [
            (self.rock_V02.positions, "R"),
            (self.surround.path_adjacent, "A"),
            (self.sky_V02.positions, "S"),
            (self.grass_V02.positions, "G"),
            (level.paths.positions, "P"),
        ]

        tiles: dict[Position, str] = {}
        for i in TILE_LETTERS:
            res_fromkeys = dict.fromkeys(*i)
            tiles |= res_fromkeys

        for position, v in tiles.items():
            pos = Position(position[0], position[1])
            if v == "A":
                surface = self.window.window_surface
                source = self.tile_adjacent(level, position)
                dest = pos
                area = None
                special_flags = 0
                surface.blit(source, dest, area, special_flags)

            elif v == "P":
                surface = self.window.window_surface
                source = self.rock_V02.surface
                dest = pos
                area = None
                special_flags = 0
                surface.blit(source, dest, area, special_flags)

            elif v == "S":
                surface = self.window.window_surface
                source = self.sky_V02.surface
                dest = pos
                area = None
                special_flags = 0
                surface.blit(source, dest, area, special_flags)

            elif v == "G":
                surface = self.window.window_surface
                source = self.grass_V02.surface
                dest = pos
                area = None
                special_flags = 0
                surface.blit(source, dest, area, special_flags)

    def Blit(self):
        surface = self.window.window_surface
        for l in self.list_DataBlit:
            surface.blit(l.source, l.dest, l.area, l.special_flags)

    def set_surface_to_window(self, level: "Level"):
        if not level.player_path_position:
            return

        source = self.player_image
        surface = self.window.window_surface

        width = source.get_width()
        x = int(level.player_path_position[0] + ((level.GRID_SIZE - width) / 2))

        height = source.get_height()
        y = level.player_path_position[1] + (level.GRID_SIZE - height)

        dest = Position(x, y)
        area = None
        special_flags = 0
        surface.blit(source, dest, area, special_flags)

    #! Blit - METHODS - END *****************

    def draw_debug_route(self, level: "Level"):
        for p in level.route.positions:
            color = Colors.GREEN.value
            position = Position(p[0], p[1])
            self.rect_to_surface_outline(level, color, position)

    def clear_blit_list(self):
        self.list_DataBlit: list[BlitData] = []

    def draw_debug_start_position(self, level: "Level"):
        position = level.paths.positions[0]
        self.rect_to_surface_outline(
            level, Colors.RED.value, Position(position.x, position.y)
        )

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

    def set_window_end(self):
        if not self.window.m_event:
            return

        if self.window.m_event.state == WINDOW_CLOSE:
            self.set_end()

    #! needs to be run?!
    def set_end(self):
        self.run = False
        self.window.close_window()
        sys.exit()  # TODO MOVE ELSEWHERE?

    def imageSurface(self, level: "Level", paths: str) -> pygame.surface.Surface:
        # paths: str = "rock.png"
        return self.getSurfaceFile(paths, level)

    def getSurfaceFile(self, paths: str, level: "Level") -> pygame.surface.Surface:
        path = self.PATH_IMAGES
        filename = os.path.join(path, paths)
        surface = pygame.image.load(filename)
        size = level.GRID_SIZE_2D
        return pygame.transform.scale(surface, size)
