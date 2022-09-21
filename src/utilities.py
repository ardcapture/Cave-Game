from typing import Any, NamedTuple
from dataclasses import dataclass


class Position(NamedTuple):
    x: int
    y: int


class Direction(NamedTuple):
    x: int
    y: int


class MouseEvent(NamedTuple):
    pos: tuple[int, int]
    button: bool


class Color(NamedTuple):
    red: int
    green: int
    blue: int


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


DOWN = Direction(x=0, y=1)
LEFT = Direction(x=-1, y=0)
RIGHT = Direction(x=1, y=0)
UP = Direction(x=0, y=-1)


DIRECTIONS: list[Direction] = [DOWN, LEFT, RIGHT, UP]

TILE_DIRECTIONS: dict[str, tuple[int, int]] = {
    "T": (0, -1),
    "R": (1, 0),
    "B": (0, 1),
    "L": (-1, 0),
    "TR": (1, -1),
    "BR": (1, 1),
    "BL": (-1, 1),
    "TL": (-1, -1),
}

AROUND: list[int] = [-1, 0, 1]

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


def debug_instance_variables(self: Any) -> None:
    print(f"* {self.__class__.__name__}.debug_instance_variables")

    for k in self.__dict__.keys():
        print(f"- {type(self).__name__}: {k}")


def get_distance_in_direction(
    position: tuple[int, int], direction: str, grid_size: int
) -> tuple[int, int]:
    if direction == "RIGHT":
        return (position[0] + grid_size, position[1])
    if direction == "LEFT":
        return (position[0] - grid_size, position[1])
    if direction == "DOWN":
        return (position[0], position[1] + grid_size)
    if direction == "UP":
        return (position[0], position[1] - grid_size)
    else:
        return (position[0], position[1])


def position_to_grid_position(pos: tuple[int, int], grid_size: int) -> tuple[int, int]:
    return tuple(map(lambda x: (x // grid_size) * grid_size, pos))


def get_list_difference(list01: list[Any], list02: list[Any]) -> list[Any]:
    return [x for x in list01 if x not in list02]
