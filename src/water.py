from typing import Any
from dataclasses import dataclass

from src.utilities import (
    debug_instance_variables,
    get_distance_in_direction,
    get_list_difference,
)

# todo - sort these types
T_Water = Any


@dataclass
class Water_Data:
    position: tuple[int, int]


class Water:
    def update(
        self, grid_size: int, height: int, paths: list[tuple[int, int]] = []
    ) -> list[T_Water]:

        water_above_rock = self._get_water_above_rock(paths, grid_size)
        water_collect_positions = self._get_water_collect_positions(
            paths, water_above_rock, grid_size
        )
        water_waterline_positions = self._get_water_waterline_positions(
            paths, grid_size, height
        )
        water_positions = self._get_water_positions(
            water_collect_positions, water_waterline_positions
        )

        debug_instance_variables(self)

        return [Water_Data(position=w) for w in water_positions]

    def _get_water_above_rock(
        self, paths: list[tuple[int, int]], grid_size: int
    ) -> list[tuple[int, int]]:
        return [
            (p[0], p[1])
            for p in paths
            if get_distance_in_direction(p, "DOWN", grid_size) not in paths
        ]

    def _get_position_either_side(self, position: tuple[int, int], grid_size: int):
        return [
            get_distance_in_direction(position, "RIGHT", grid_size),
            get_distance_in_direction(position, "LEFT", grid_size),
        ]

    def _get_water_collect_positions(
        self,
        paths: list[tuple[int, int]],
        water_above_rock: list[tuple[int, int]],
        grid_size: int,
    ) -> list[tuple[int, int]]:

        start = len(water_above_rock)
        for index, p in enumerate(water_above_rock):
            if any(
                item in self._get_position_either_side(p, grid_size)
                for item in get_list_difference(paths, water_above_rock)
            ):
                water_above_rock.pop(index)
        end = len(water_above_rock)

        if start != end:
            self._get_water_collect_positions(paths, water_above_rock, grid_size)

        return water_above_rock

    def _get_water_waterline_positions(
        self, paths: list[tuple[int, int]], grid_size: int, height: int
    ) -> list[tuple[int, int]]:
        return [p for p in paths if p[1] > ((height - grid_size * 2) * (2 / 3))]

    def _get_water_positions(
        self,
        water_collect_positions: list[tuple[int, int]],
        water_waterline_positions: list[tuple[int, int]],
    ):
        return [
            x for x in water_waterline_positions if x not in water_collect_positions
        ] + water_collect_positions
