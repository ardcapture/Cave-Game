import copy
from collections import defaultdict
from itertools import product
from typing import TYPE_CHECKING

from src.utilities import (
    DIRECTIONS_EIGHT,
    DUPLICATE_CHECKS,
    TILE_DIRECTIONS,
    Direction,
    Position,
)

if TYPE_CHECKING:
    from src.level import Level


class Surround:
    def set_path_adjacent(self, level: "Level") -> dict[Position, str]:
        self.path_adjacent = {
            _tile(level, position, direction): "fish"
            for position, direction in product(level.paths, DIRECTIONS_EIGHT)
            if _tile(level, position, direction) not in level.paths
        }

    def surround_positions(self, level: "Level"):
        result_list = copy.copy(
            _set_possible_surrounding_positions(self.path_adjacent, level)
        )
        for values, duplicate in product(result_list.values(), DUPLICATE_CHECKS):
            if duplicate in values and any(i in list(duplicate) for i in values):
                values.remove(duplicate)
        return result_list


def _set_possible_surrounding_positions(
    path_adjacent: dict[Position, str], level: "Level"
):
    surrounding_positions: dict[Position, list[str]] = defaultdict(list)

    for position, direction in product(path_adjacent, DIRECTIONS_EIGHT):
        x_offset = direction.x * level.GRID_SIZE
        y_offset = direction.y * level.GRID_SIZE
        tile = (position.x + x_offset, position.y + y_offset)

        if tile in level.paths:
            direction_keys = list(TILE_DIRECTIONS.keys())
            direction_values = list(TILE_DIRECTIONS.values())
            direction_index = direction_values.index(direction)
            result = direction_keys[direction_index]
            surrounding_positions[position].append(result)
    return surrounding_positions


def _tile(level: "Level", position: Position, direction: Direction) -> Position:
    new_x = position.x + (direction.x * level.GRID_SIZE)
    new_y = position.y + (direction.y * level.GRID_SIZE)
    return Position(new_x, new_y)
