from src.utilities import Position
from . import utilities
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from WaterFactory import LevelObject


class Positions:
    def __init__(self, positions: list[Position] = []):
        self._positions = positions

    def positions_above_height(self, positions: list[Position], height: float):
        filtered_positions = [position for position in positions if position.y > height]
        return filtered_positions

    def add_position(self, positions: list[Position]):
        return self._positions + positions

    def positions_vertical_in_distance(self, distance: int) -> list[Position]:
        return [
            position
            for position in self._positions
            if (
                utilities.get_distance_in_direction(position, "UP", distance)
                in self._positions
                or utilities.get_distance_in_direction(position, "DOWN", distance)
                in self._positions
            )
        ]

    def add_water_above_rock(self, distance: int) -> list[Position]:
        positions: list[Position] = []
        for position in self._positions:
            new_position = utilities.get_distance_in_direction(
                position, "DOWN", distance
            )
            if new_position not in self._positions:
                positions.append(Position(position.x, position.y))

        return positions

    def get_list_position_difference(
        self,
        level_objects: list["LevelObject"],
    ) -> list[Position]:
        level_positions = [level_obj.position for level_obj in level_objects]

        return [
            position for position in self._positions if position not in level_positions
        ]

    def filter_positions_above_height(self, height: float):
        filtered_positions = [
            position for position in self._positions if position.y > height
        ]
        return filtered_positions

    @property
    def positions(self):
        return self._positions

    def append(self, position: Position):
        self._positions.append(position)

    @property
    def last(self):
        return self._positions[-1]
