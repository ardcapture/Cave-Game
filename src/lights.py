import copy
import random
from itertools import chain, groupby
from operator import itemgetter
from typing import TYPE_CHECKING

from src.utilities import Color, Positions, Light_Data

if TYPE_CHECKING:
    from src.Level import Level
    from src.Nav import Nav


class Lights:
    objs = []
    brightness_list: list[Color] = []
    sun_light_positions: dict[Positions, tuple[Color]]

    def __init__(self, level: "Level") -> None:

        print("init Lights")

        self.grid_size = level.GRID_SIZE
        self.grid_size_2D = (level.GRID_SIZE, level.GRID_SIZE)

        self.brightness_list = self.set_color_value(256)

    def update(self, level: "Level", path: "Nav"):

        self.light_positions = dict.fromkeys(level.paths, (0, 0, 0))
        self.character_light_positions = dict.fromkeys(level.paths, (0, 0, 0))

        # self.set_lights_debug(level)

        self.source = self.set_light_source(level)

        self.sun_light_positions = self.get_positions_sun(level)

        self.character_light_positions = self.update_character_light_positions(level)

        light_positions = self.update_light_positions()

        self.light_objs = [
            Light_Data(position=pos, color=color)
            for pos, color in light_positions.items()
            if color[0] > 0
        ]

    def set_light_source(self, level: "Level") -> Positions:
        seq = level.paths
        return random.choice(seq)

    def set_color_value(self, x: int):

        while x > 0:
            r, g, b = tuple([x] * 3)
            self.brightness_list.append(Color(r, g, b))
            x //= 2

        return self.brightness_list

    #! uses itself
    def update_character_light_positions(self, level: "Level") -> list[Positions]:

        character_light_positions_copy = copy.copy(self.character_light_positions)

        mylist = [level.GRID_SIZE, -level.GRID_SIZE]
        for i in mylist:
            poss_light_position = level.player_path_position
            brightness = 0
            run = True
            while run:
                if poss_light_position in level.paths:
                    character_light_positions_copy[
                        poss_light_position
                    ] = self.brightness_list[brightness]
                    poss_light_position = Positions(
                        poss_light_position[0] + i, poss_light_position[1]
                    )
                    if brightness < len(self.brightness_list) - 1:
                        brightness += 1
                else:
                    run = False
        for i in mylist:
            poss_light_position = level.player_path_position
            brightness = 0
            run = True
            while run:
                if poss_light_position in level.paths:
                    character_light_positions_copy[
                        poss_light_position
                    ] = self.brightness_list[brightness]
                    poss_light_position = Positions(
                        poss_light_position[0], poss_light_position[1] + i
                    )
                    if brightness < len(self.brightness_list) - 1:
                        brightness += 1
                else:
                    run = False
        character_light_positions_copy[level.player_path_position] = (0, 0, 0)
        return character_light_positions_copy

    #! takes itself
    def get_positions_sun(self, level: "Level") -> dict[Positions, tuple[int]]:
        path_paths = level.paths
        path_path_start_position = level.path_start_position
        path_path_finish_position = level.path_finish_position

        sun_light_positions = dict.fromkeys(path_paths, (0, 0, 0))

        seq = [path_path_start_position, path_path_finish_position]

        for light_position in seq:
            brightness = 1

            while True:
                if not light_position in path_paths:
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
