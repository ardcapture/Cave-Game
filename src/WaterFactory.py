from typing import TYPE_CHECKING

from src import utilities
from src.LevelObject import LevelObject
from src.utilities import Colors, Positions
from src.WaterObject import WaterObject

if TYPE_CHECKING:
    from src.level import Level
    from src.nav import Nav


class WaterFactory:
    poss_water: list[LevelObject] = []

    left: int = 0  # for Rect
    top: int = 0  #  for Rect

    color = Colors.BLUE_LIGHT  # for draw rect

    def __init__(self, level: "Level", path: "Nav") -> None:
        print("init Water")

        self.width: int = level.GRID_SIZE  # for Rect and Surface
        self.height: int = level.GRID_SIZE  # for Rect ans Surface
        self.rect = (self.width, self.height)

        self.water_add_above_rock(level)

        self.water_collect_positions = self.get_water_collect_positions(level)

        self.water_waterline_positions = self.get_water_waterline_positions(level)

    def water_add_above_rock(self, level: "Level") -> None:
        for p in level.paths:
            res_pos = utilities.get_distance_in_direction(p, "DOWN", level.GRID_SIZE)
            if res_pos not in level.paths:
                position = Positions(p.x, p.y)
                self.poss_water.append(WaterObject(self.rect, position))

    def get_position_either_side(self, position: Positions, level: "Level"):
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
        positions = [
            position for position in level.paths if position.y > level.water_line
        ]

        self.water_waterline_positions: list[LevelObject] = [
            WaterObject(self.rect, p) for p in positions
        ]

        return self.water_waterline_positions

    @property
    def water_objects(self) -> list[LevelObject]:
        res_set = set(self.water_collect_positions + self.water_waterline_positions)
        return list(res_set)
