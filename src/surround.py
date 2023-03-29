import copy
from collections import defaultdict
from itertools import product
from typing import TYPE_CHECKING

from src.utilities import (
    DIRECTIONS_EIGHT,
    DUPLICATE_CHECKS,
    TILE_DIRECTIONS,
    Direction,
    Positions,
)

if TYPE_CHECKING:
    from src.level import Level


class Surround:
    def update(self, level: "Level") -> None:

        self.path_adjacent = self.update_dict_path_adjacent(level)

        self.poss_surround_positions = self.set_poss_path_surround_positions(level)

    def update_dict_path_adjacent(self, level: "Level"):
        return {
            self.tile(level, position, direction): "fish"
            for position, direction in product(level.paths, DIRECTIONS_EIGHT)
            if self.tile(level, position, direction) not in level.paths
        }

    def set_poss_path_surround_positions(self, level: "Level"):

        d: dict[Positions, list[str]] = defaultdict(list)

        for position, direction in product(self.path_adjacent, DIRECTIONS_EIGHT):
            tile = (
                position[0] + (direction.x * level.GRID_SIZE),
                position[1] + (direction.y * level.GRID_SIZE),
            )
            if tile in level.paths:
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
        self, level: "Level", position: Positions, direction: Direction
    ) -> Positions:
        x = position.x + (direction.x * level.GRID_SIZE)
        y = position.y + (direction.y * level.GRID_SIZE)
        return Positions(x, y)
