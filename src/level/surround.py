from collections import defaultdict
from itertools import product
from typing import Any

import utilities
from constants import AROUND, DUPLICATE_CHECKS, TILE_DIRECTIONS

# todo needs fixing
TypeAny = Any
TypeMultiple = Any


class Surround:
    def update(self, paths: list[tuple[int, int]], grid_size: int) -> TypeMultiple:

        path_adjacent = self.set_dict_path_adjacent(paths, grid_size)  # todo may remove

        poss_surround_positions = self.set_poss_path_surround_positions(
            path_adjacent, paths, grid_size
        )

        surround_positions = self.set_path_surround_positions(
            poss_surround_positions,
        )

        utilities.debug_instance_variables(self)

        return surround_positions, path_adjacent

    def set_dict_path_adjacent(
        self, paths: list[tuple[int, int]], grid_size: int
    ) -> dict[tuple[int, int], str]:
        return {
            self.tile(path, x, y, grid_size): "fish"
            for path, x, y in product(paths, AROUND, AROUND)
            if self.tile(path, x, y, grid_size) not in paths
        }

    def set_path_surround_positions(
        self, poss_path_surround_positions: dict[tuple[int, int], list[str]]
    ) -> dict[tuple[int, int], list[str]]:

        for v, s in product(poss_path_surround_positions.values(), DUPLICATE_CHECKS):
            if s in v and any(i in list(s) for i in v):
                v.remove(s)
        return poss_path_surround_positions

    def set_poss_path_surround_positions(
        self,
        path_adjacent: list[tuple[int, int]],
        light_positions: list[tuple[int, int]],
        grid_size: int,
    ) -> defaultdict[tuple[int, int], list[str]]:

        d: dict[tuple[int, int], list[str]] = defaultdict(list)

        for i, j, k in product(path_adjacent, AROUND, AROUND):
            tile = (i[0] + (j * grid_size), i[1] + (k * grid_size))
            if tile in light_positions:
                res = list(TILE_DIRECTIONS.keys())[
                    list(TILE_DIRECTIONS.values()).index((j, k))
                ]
                d[i].append((res))
        return d

    def tile(
        self, path: tuple[int, int], x: int, y: int, grid_size: int
    ) -> tuple[int, int]:
        return (path[0] + (x * grid_size), path[1] + (y * grid_size))
