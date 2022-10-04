import random
from dataclasses import dataclass
from itertools import chain, groupby
from operator import itemgetter
from typing import TYPE_CHECKING
import copy

from src.utilities import DIRECTIONS_FOUR, Position

if TYPE_CHECKING:
    from src.level import Level


@dataclass
class Light_Data:
    surface: str = "LIGHT"
    to_surface: str = "WINDOW"
    font_size: int = 15
    color: tuple = (0, 0, 0)
    special_flags: str = "BLEND_RGB_ADD"
    position: tuple = None


class Lights:
    def __init__(self, level) -> None:

        self.grid_size = level.GRID_SIZE
        self.grid_size_2D = (level.GRID_SIZE, level.GRID_SIZE)

        self.objs = []
        self.brightness_list: list = []

    def update(self, level: "Level", path):

        self.light_positions = dict.fromkeys(path.paths, (0, 0, 0))
        self.character_light_positions = dict.fromkeys(path.paths, (0, 0, 0))

        x, self.brightness_list = self.set_color_value(1)

        # self.set_lights_debug(level)

        self.source = self.set_light_source(level, path)

        self.sun_light_positions = self.get_positions_sun(level, path)

        self.character_light_positions = self.update_character_light_positions(
            level, path
        )

        light_positions = self.update_light_positions()

        light_objs = [
            Light_Data(position=pos, color=color)
            for pos, color in light_positions.items()
            if color[0] > 0
        ]

        return light_objs

    def get_light_positions_adjacent(
        self,
        level: "Level",
        light_positions_adjacent: list[Position],
    ) -> list[Position]:
        """Recursive"""

        result = []
        for light in light_positions_adjacent:
            pos = (
                light["position"][0] + (light["direction"][0] * self.grid_size),
                light["position"][1] + (light["direction"][1] * self.grid_size),
            )
            if pos in level.path_obj.paths:
                result.append(
                    {
                        "position": pos,
                        "direction": light["direction"],
                        "adjacent_by": light["adjacent_by"] + 1,
                    }
                )

        if len(result) > 0:
            result = self.get_light_positions_adjacent(level, result)

        light_positions_adjacent += result

        return light_positions_adjacent

    def get_light_positions_adjacent_source(self, level: "Level"):
        result = []
        for direction in DIRECTIONS_FOUR:
            pos = (
                self.source[0] + (direction[0] * self.grid_size),
                self.source[1] + (direction[1] * self.grid_size),
            )
            if pos in level.path_obj.paths:
                result.append(
                    {
                        "position": pos,
                        "direction": direction,
                        "adjacent_by": 1,
                    }
                )
        return result

    def set_light_source(self, level: "Level", path) -> Position:
        seq = path.paths
        return random.choice(seq)

    def set_color_value(self, x: int):
        """Recursive"""
        self.brightness_list = []

        if x < 256:
            res, self.brightness_list = self.set_color_value((x * 2))
            res = int(res)
            if res >= 255:
                res += -1
            self.brightness_list.append(tuple([res] * 3))

        return x, self.brightness_list

    #! uses itself
    def update_character_light_positions(self, level: "Level", path) -> list[Position]:

        character_light_positions_copy = copy.copy(self.character_light_positions)

        mylist = [level.GRID_SIZE, -level.GRID_SIZE]
        for i in mylist:
            poss_light_position = path.player_path_position
            brightness = 0
            run = True
            while run:
                if poss_light_position in path.paths:
                    character_light_positions_copy[
                        poss_light_position
                    ] = self.brightness_list[brightness]
                    poss_light_position = Position(
                        poss_light_position[0] + i, poss_light_position[1]
                    )
                    if brightness < len(self.brightness_list) - 1:
                        brightness += 1
                else:
                    run = False
        for i in mylist:
            poss_light_position = path.player_path_position
            brightness = 0
            run = True
            while run:
                if poss_light_position in path.paths:
                    character_light_positions_copy[
                        poss_light_position
                    ] = self.brightness_list[brightness]
                    poss_light_position = Position(
                        poss_light_position[0], poss_light_position[1] + i
                    )
                    if brightness < len(self.brightness_list) - 1:
                        brightness += 1
                else:
                    run = False
        character_light_positions_copy[path.player_path_position] = (0, 0, 0)
        return character_light_positions_copy

    #! takes itself
    def get_positions_sun(self, level: "Level", path):
        sun_light_positions = dict.fromkeys(path.paths, (0, 0, 0))

        for light_position in [
            path.path_start_position,
            path.path_finish_position,
        ]:
            brightness = 1

            while True:
                if not light_position in path.paths:
                    break
                sun_light_positions[light_position] = self.brightness_list[brightness]
                light_position = (light_position[0], light_position[1] + self.grid_size)
                if brightness < len(self.brightness_list) - 1:
                    brightness += 1

        return sun_light_positions

    #! takes self
    def update_light_positions(self):

        get_key, get_val = itemgetter(0), itemgetter(1)

        merged_data = sorted(
            chain(
                self.light_positions.items(),
                self.sun_light_positions.items(),
                self.character_light_positions.items(),
            ),
            key=get_key,
        )
        return {k: max(map(get_val, g)) for k, g in groupby(merged_data, key=get_key)}
