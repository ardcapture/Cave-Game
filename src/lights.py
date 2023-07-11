from itertools import chain, groupby
from operator import itemgetter
from src.utilities import Color, Position, Light_Data
from typing import TYPE_CHECKING
import copy
import random

if TYPE_CHECKING:
    from src.level import Level
    from src.nav import Nav

# TODO: Complex type to class
Colors = list[Color]
PositionColor = dict[Position, Color]

# Constants:
BLACK = Color(0, 0, 0)
WHITE_VALUE = 246


class Lights:
    objs = []
    brightness_list: Colors = []
    # sun_light_positions: PositionColor

    def __init__(self, level: "Level") -> None:
        print("init Lights")

        self.grid_size = level.GRID_SIZE
        self.grid_size_2D = (level.GRID_SIZE, level.GRID_SIZE)

        self.brightness_list = self.setColorFromValue(WHITE_VALUE)

    def update(self, level: "Level", path: "Nav"):
        self.light_positions = dict.fromkeys(level.paths, BLACK)
        self.characterLightPositions = dict.fromkeys(level.paths, BLACK)

        # self.set_lights_debug(level)

        self.source = self.set_light_source(level)

        self.sun_light_positions = self.get_positions_sun(level)

        self.characterLightPositions = self.update_character_light_positions(level)

        light_positions = self.update_light_positions()

        self.light_objs = [
            Light_Data(position=pos, color=color)
            for pos, color in light_positions.items()
            if color[0] > 0
        ]

    def set_light_source(self, level: "Level") -> Position:
        seq = level.paths
        return random.choice(seq)

    def setColorFromValue(self, value: int) -> list[Color]:
        while value > 0:
            r, g, b = tuple([value] * 3)
            self.brightness_list.append(Color(r, g, b))
            value //= 2

        return self.brightness_list

    #! uses itself
    def update_character_light_positions(self, level: "Level") -> dict[Position, Color]:
        characterLightPositions = copy.copy(self.characterLightPositions)

        myList = [level.GRID_SIZE, -level.GRID_SIZE]
        for i in myList:
            possLightPosition = level.player_path_position
            brightness = 0
            run = True
            while run:
                if possLightPosition in level.paths:
                    characterLightPositions[possLightPosition] = self.brightness_list[
                        brightness
                    ]
                    possLightPosition = Position(
                        possLightPosition[0] + i, possLightPosition[1]
                    )
                    if brightness < len(self.brightness_list) - 1:
                        brightness += 1
                else:
                    run = False
        for i in myList:
            possLightPosition = level.player_path_position
            brightness = 0
            run = True
            while run:
                if possLightPosition in level.paths:
                    characterLightPositions[possLightPosition] = self.brightness_list[
                        brightness
                    ]
                    possLightPosition = Position(
                        possLightPosition[0], possLightPosition[1] + i
                    )
                    if brightness < len(self.brightness_list) - 1:
                        brightness += 1
                else:
                    run = False
        characterLightPositions[level.player_path_position] = BLACK
        return characterLightPositions

    #! takes itself
    def get_positions_sun(self, level: "Level") -> PositionColor:
        path_paths = level.paths
        path_path_start_position = level.path_start_position
        path_path_finish_position = level.path_finish_position

        sun_light_positions = dict.fromkeys(path_paths, BLACK)

        seq = [path_path_start_position, path_path_finish_position]

        for light_position in seq:
            brightnessIndex = 1

            while True:
                if not light_position in path_paths:
                    break
                sun_light_positions[light_position] = self.brightness_list[
                    brightnessIndex
                ]
                light_position = (light_position[0], light_position[1] + self.grid_size)
                if brightnessIndex < len(self.brightness_list) - 1:
                    brightnessIndex += 1

        return sun_light_positions

    #! takes self
    def update_light_positions(self):
        get_key, get_val = itemgetter(0), itemgetter(1)

        merged_data = sorted(
            chain(
                self.light_positions.items(),
                self.sun_light_positions.items(),
                self.characterLightPositions.items(),
            ),
            key=get_key,
        )
        return {k: max(map(get_val, g)) for k, g in groupby(merged_data, key=get_key)}
