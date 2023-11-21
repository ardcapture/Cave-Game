from itertools import chain, groupby
from operator import itemgetter
from src.utilities import Color, Position, Light_Data
from typing import TYPE_CHECKING
import copy
import random

if TYPE_CHECKING:
    from src.level import Level

# TODO: Complex type to class
Colors = list[Color]
PositionColor = dict[Position, Color]

# Constants:
BLACK = Color(0, 0, 0)
WHITE_VALUE = 246


class Lights:
    objs = []
    brightness_list: Colors = []

    light_positions: dict[Position, Color]
    characterLightPositions: dict[Position, Color]
    sun_light_positions: PositionColor

    def __init__(self, GRID_SIZE: int) -> None:
        print("init Lights")

        self.GRID_SIZE = GRID_SIZE
        self.brightness_list = self.setColorFromValue(WHITE_VALUE)

    def update(self):
        light_positions = self.update_light_positions()

        self.light_objs = [
            Light_Data(position=pos, color=color)
            for pos, color in light_positions.items()
            if color[0] > 0
        ]

    def setColorFromValue(self, value: int) -> list[Color]:
        while value > 0:
            r, g, b = tuple([value] * 3)
            self.brightness_list.append(Color(r, g, b))
            value //= 2

        return self.brightness_list

    def update_character_light_positions(
        self,
        level: "Level",
        directions: list[int],
    ) -> dict[Position, Color]:
        characterLightPositions = copy.copy(self.characterLightPositions)

        for i in directions:
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
        for i in directions:
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
    def get_positions_sun(
        self,
        level: "Level",
        start_finish_positions: list[Position],
        path_paths: list[Position],
    ) -> PositionColor:
        sun_light_positions = dict.fromkeys(path_paths, BLACK)

        for light_position in start_finish_positions:
            brightnessIndex = 1

            while True:
                if not light_position in path_paths:
                    break
                sun_light_positions[light_position] = self.brightness_list[
                    brightnessIndex
                ]
                light_position = (
                    light_position[0],
                    light_position[1] + level.GRID_SIZE,
                )
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
