from typing import Any, NamedTuple, TYPE_CHECKING
from dataclasses import dataclass
import pygame
from pygame import Rect
import copy
import random

if TYPE_CHECKING:
    from WaterFactory import LevelObject


class Position(NamedTuple):
    x: int
    y: int


class Direction(NamedTuple):
    x: int
    y: int


class WindowEvent(NamedTuple):
    pos: Position
    key: int
    state: int


class Color(NamedTuple):
    red: int
    green: int
    blue: int


class DrawRectData(NamedTuple):
    surface: pygame.surface.Surface
    color: Color
    rect: Rect


class BlitData(NamedTuple):
    source: pygame.surface.Surface
    dest: Position
    area: None
    special_flags: int


# class Water(NamedTuple):
#     left: int
#     top: int
#     width: int
#     height: int


# DATARECT_CLIMB_POSITIONS = DataRect(
#     left=7 / 16,
#     top= 0,
#     width= 8,
#     height=0,
# )


@dataclass
class Colors:
    BLACK = Color(0, 0, 0)
    WHITE = Color(255, 255, 255)
    BLACK_VERY_LIGHT = Color(210, 210, 210)
    WHITE_4TH_4TH_4TH_4TH = Color(1, 1, 1)
    RED = Color(255, 0, 0)
    GREEN = Color(0, 255, 0)
    BLUE = Color(0, 0, 255)
    BLUE_LIGHT = Color(125, 125, 255)
    BLUE_VERY_LIGHT = Color(210, 210, 255)


@dataclass
class NavData:
    position_type: str


@dataclass
class Light_Data:
    surface: str = "LIGHT"  # TODO change type?
    to_surface: str = "WINDOW"  # TODO change type?
    font_size: int = 15
    color: Color = Color(0, 0, 0)
    special_flags: str = "BLEND_RGB_ADD"
    position: Position = Position(-1, -1)


LEFT_UP = Direction(x=-1, y=-1)
LEFT = Direction(x=-1, y=0)
LEFT_DOWN = Direction(x=-1, y=1)

UP = Direction(x=0, y=-1)
DOWN = Direction(x=0, y=1)

RIGHT_UP = Direction(x=1, y=-1)
RIGHT = Direction(x=1, y=0)
RIGHT_DOWN = Direction(x=1, y=1)


DIRECTIONS_FOUR: list[Direction] = [
    DOWN,
    LEFT,
    RIGHT,
    UP,
]
DIRECTIONS_EIGHT: list[Direction] = [
    LEFT_UP,
    LEFT,
    LEFT_DOWN,
    UP,
    DOWN,
    RIGHT_UP,
    RIGHT,
    RIGHT_DOWN,
]

TILE_DIRECTIONS: dict[str, Direction] = {
    "T": Direction(0, -1),
    "R": Direction(1, 0),
    "B": Direction(0, 1),
    "L": Direction(-1, 0),
    "TR": Direction(1, -1),
    "BR": Direction(1, 1),
    "BL": Direction(-1, 1),
    "TL": Direction(-1, -1),
}


DUPLICATE_CHECKS: list[str] = [
    "TR",
    "BR",
    "TL",
    "BL",
]


IMAGE_TYPES: list[str] = ["T", "R", "B", "L", "TR", "BR", "BL", "TL"]


LIGHTING_TILE_ROTATE: dict[str, tuple[str, int]] = {
    "T": ("TOP_image", 0),
    "TR": ("TOP_R_image", 0),
    "L": ("TOP_image", 90),
    "TL": ("TOP_R_image", 90),
    "B": ("TOP_image", 180),
    "BL": ("TOP_R_image", 180),
    "R": ("TOP_image", 270),
    "BR": ("TOP_R_image", 270),
}


class NoPositionFound(Exception):
    pass


def set_reduced_positions(grid_positions: list[Position]) -> list[Position]:
    res_grid: list[Position] = copy.deepcopy(grid_positions)
    num_removals: int = len(res_grid) // 3

    for _ in range(num_removals):
        random_position: Position = random.choice(res_grid)
        res_grid.remove(random_position)
    return res_grid


def debug_instance_variables(self: Any) -> None:
    print(f"* {self.__class__.__name__}.debug_instance_variables")

    for k in self.__dict__.keys():
        print(f"- {type(self).__name__}: {k}")


def get_distance_in_direction(
    position: Position, direction: str, grid_size: int
) -> Position:
    if direction == "RIGHT":
        return Position(position[0] + grid_size, position[1])
    if direction == "LEFT":
        return Position(position[0] - grid_size, position[1])
    if direction == "DOWN":
        return Position(position.x, position.y + grid_size)
    if direction == "UP":
        return Position(position.x, position.y - grid_size)
    else:
        return Position(position.x, position.y)


def position_to_grid_position(position: Position, grid_size: int) -> Position:
    x = (position.x // grid_size) * grid_size
    y = (position.y // grid_size) * grid_size

    return Position(x, y)


def get_list_difference(list01: list[Any], list02: list[Any]) -> list[Any]:
    return [x for x in list01 if x not in list02]


def get_list_position_difference(
    list01: list[Any], object_list: list["LevelObject"]
) -> list[Any]:
    list02 = [x.position for x in object_list]
    return [x for x in list01 if x not in list02]


# def path_directions_dict_to_class(self, my_dict):

#     for key in my_dict:
#         setattr(self, key, my_dict[key])
