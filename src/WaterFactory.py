from typing import TYPE_CHECKING

from src import utilities
from src.LevelObject import LevelObject
from src.utilities import Colors, Position
from src.WaterObject import WaterObject

if TYPE_CHECKING:
    from src.level import Level


class WaterFactory:
    poss_water: list[LevelObject] = []

    left: int = 0  # for Rect
    top: int = 0  #  for Rect

    color = Colors.BLUE_LIGHT.value  # for draw rect

    def __init__(self, level: "Level") -> None:
        print("init Water")

        self.HEIGHT_GS = level.HEIGHT_GS
        self.GRID_SIZE = level.GRID_SIZE

        self.width: int = level.GRID_SIZE  # for Rect and Surface
        self.height: int = level.GRID_SIZE  # for Rect ans Surface
        self.rect = (self.width, self.height)

        self.add_water_above_rock(level)

        self.water_collect_positions = self.get_water_collect_positions(level)

        self.water_waterline_positions = self.get_water_waterline_positions(level)

    @property
    def water_objects(self) -> list[LevelObject]:
        res_set = set(self.water_collect_positions + self.water_waterline_positions)
        return list(res_set)

    @property
    def water_line(self) -> float:
        grid_height = self.HEIGHT_GS - self.GRID_SIZE * 2
        water_level = grid_height * (2 / 3)
        return water_level

    def add_water_above_rock(self, level: "Level") -> None:
        for path in level.paths:
            new_position = utilities.get_distance_in_direction(
                path, "DOWN", level.GRID_SIZE
            )
            if new_position not in level.paths:
                position = Position(path.x, path.y)
                water_object = WaterObject(self.rect, position)
                self.poss_water.append(water_object)

    def get_position_either_side(self, position: Position, level: "Level"):
        direction = "LEFT"
        grid_size = level.GRID_SIZE
        position_left = utilities.get_distance_in_direction(
            position, direction, grid_size
        )

        direction = "RIGHT"
        grid_size = level.GRID_SIZE
        position_right = utilities.get_distance_in_direction(
            position, direction, grid_size
        )

        return [position_left, position_right]

    def get_water_collect_positions(self, level: "Level") -> list[LevelObject]:
        run = True
        while run:
            start = len(self.poss_water)
            for index, p in enumerate(self.poss_water):
                if any(
                    item in self.get_position_either_side(p.position, level)
                    for item in utilities.get_list_position_difference(
                        level.paths, self.poss_water
                    )
                ):
                    self.poss_water.pop(index)
            end = len(self.poss_water)

            run = start != end

        return self.poss_water

    def get_water_waterline_positions(self, level: "Level") -> list[LevelObject]:
        positions = level.filter_positions_above_height(level.paths, self.water_line)

        self.water_waterline_positions: list[LevelObject] = [
            WaterObject(self.rect, p) for p in positions
        ]

        return self.water_waterline_positions
