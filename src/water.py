import copy
from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np

from src import utilities
from src.utilities import Position

if TYPE_CHECKING:
    from src.level import Level
    from src.level.path import Path


class Water:

    water: list[Position] = []

    def update(self, level: "Level", path: "Path"):

        self.water_add_above_rock(path, level)

        self.water_collect_positions = self.get_water_collect_positions(path, level)

        self.water_waterline_positions = self.get_water_waterline_positions(path, level)

    def water_add_above_rock(self, path: "Path", level: "Level") -> None:

        for p in path.paths:
            res_pos = utilities.get_distance_in_direction(p, "DOWN", level.GRID_SIZE)
            if res_pos not in path.paths:
                self.water.append(Position(p.x, p.y))

    def get_position_either_side(self, position: Position, level: "Level"):

        position_left = utilities.get_distance_in_direction(
            position, "LEFT", level.GRID_SIZE
        )
        position_right = utilities.get_distance_in_direction(
            position, "RIGHT", level.GRID_SIZE
        )

        return [position_left, position_right]

    def get_water_collect_positions(
        self,
        path: "Path",
        level: "Level",
    ) -> list[Position]:

        run = True
        while run:

            start = len(self.water)
            for index, p in enumerate(self.water):
                if any(
                    item in self.get_position_either_side(p, level)
                    for item in utilities.get_list_difference(path.paths, self.water)
                ):
                    self.water.pop(index)
            end = len(self.water)

            run = start != end

        return self.water

    def get_water_waterline_positions(
        self, path: "Path", level: "Level"
    ) -> list[Position]:

        return [position for position in path.paths if position.y > level.water_line]

    @property
    def water_positions(self):

        res_set = set(self.water_collect_positions + self.water_waterline_positions)
        res_list = list(res_set)
        return res_list
