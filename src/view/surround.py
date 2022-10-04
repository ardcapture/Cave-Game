from collections import defaultdict
from itertools import product
from typing import TYPE_CHECKING
import copy

from src.utilities import (
    DUPLICATE_CHECKS,
    TILE_DIRECTIONS,
    Position,
    DIRECTIONS_EIGHT,
    Direction,
)


if TYPE_CHECKING:
    from src.level import Level
    from src.view.view import View
    from src.level.path import Path


class Surround:
    def update(self, level: "Level", path: "Path") -> None:

        self.path_adjacent = self.update_dict_path_adjacent(level, path)

        self.poss_surround_positions = self.set_poss_path_surround_positions(
            level, path
        )

    def update_dict_path_adjacent(self, level: "Level", path: "Path"):
        path_adjacent = {}
        for position, direction in product(path.paths, DIRECTIONS_EIGHT):
            if self.tile(level, position, direction) not in path.paths:
                path_adjacent[self.tile(level, position, direction)] = "fish"

        return path_adjacent

    def set_poss_path_surround_positions(self, level: "Level", path: "Path"):

        d: dict[Position, list[str]] = defaultdict(list)

        for position, direction in product(self.path_adjacent, DIRECTIONS_EIGHT):
            tile = (
                position[0] + (direction.x * level.GRID_SIZE),
                position[1] + (direction.y * level.GRID_SIZE),
            )
            if tile in path.paths:
                res = list(TILE_DIRECTIONS.keys())[
                    list(TILE_DIRECTIONS.values()).index(direction)
                ]
                d[position].append((res))
        return d

    @property
    def surround_positions(self):
        res_list = copy.copy(self.poss_surround_positions)
        for v, s in product(res_list.values(), DUPLICATE_CHECKS):
            if s in v and any(i in list(s) for i in v):
                v.remove(s)
        return res_list

    def tile(
        self, level: "Level", position: Position, direction: Direction
    ) -> Position:
        x = position.x + (direction.x * level.GRID_SIZE)
        y = position.y + (direction.y * level.GRID_SIZE)
        return Position(x, y)
