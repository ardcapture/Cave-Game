from itertools import product
from collections import defaultdict

from utilities import debug_instance_variables


AROUND = [-1, 0, 1]

TILE_DIRECTIONS = {
    "T": (0, -1),
    "R": (1, 0),
    "B": (0, 1),
    "L": (-1, 0),
    "TR": (1, -1),
    "BR": (1, 1),
    "BL": (-1, 1),
    "TL": (-1, -1),
}


class Surround:
    def update(self, paths, grid_size):

        path_adjacent = self.set_dict_path_adjacent(paths, grid_size)  # todo may remove

        poss_surround_positions = self.set_poss_path_surround_positions(
            path_adjacent, paths, grid_size
        )

        surround_positions = self.set_path_surround_positions(
            poss_surround_positions,
        )

        debug_instance_variables(self)

        return surround_positions, path_adjacent

    def set_dict_path_adjacent(self, paths, grid_size):
        return {
            self.tile(path, x, y, grid_size): "fish"
            for path, x, y in product(paths, AROUND, AROUND)
            if self.tile(path, x, y, grid_size) not in paths
        }

    def set_path_surround_positions(self, poss_path_surround_positions):
        duplicate_checks = [
            "TR",
            "BR",
            "TL",
            "BL",
        ]
        for v, s in product(poss_path_surround_positions.values(), duplicate_checks):
            if s in v and any(i in list(s) for i in v):
                v.remove(s)
        return poss_path_surround_positions

    def set_poss_path_surround_positions(
        self, path_adjacent, light_positions, grid_size
    ):
        d = defaultdict(list)
        for i, j, k in product(path_adjacent, AROUND, AROUND):
            tile = (i[0] + (j * grid_size), i[1] + (k * grid_size))
            if tile in light_positions:
                res = list(TILE_DIRECTIONS.keys())[
                    list(TILE_DIRECTIONS.values()).index((j, k))
                ]
                d[i].append((res))
        return d

    def tile(self, path, x, y, grid_size):
        return (path[0] + (x * grid_size), path[1] + (y * grid_size))
