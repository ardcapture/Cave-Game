from itertools import chain, groupby
from operator import itemgetter
from src.utilities import Color, Position, Light_Data, Colors
from collections import defaultdict


# Constants:
WHITE_VALUE = 246


class Lights:
    # objs = []
    brightness_list: list[Color] = []

    characterLightPositions: dict[Position, Color]
    sun_light_positions: dict[Position, Color]

    def __init__(self) -> None:
        print("init Lights")

        self.brightness_list = self._update_brightness_list(WHITE_VALUE)

    def set_light_objs(self):
        light_positions = self._update_light_positions()

        self.light_objs = [
            Light_Data(position=pos, color=color)
            for pos, color in light_positions.items()
            if color[0] > 0
        ]

    def _update_brightness_list(self, value: int) -> list[Color]:
        while value > 0:
            r, g, b = tuple([value] * 3)
            self.brightness_list.append(Color(r, g, b))
            value //= 2

        return self.brightness_list

    #! takes self
    def _update_light_positions(self) -> dict[Position, Color]:
        light_positions: defaultdict[Position, Color] = defaultdict(
            lambda: Colors.BLACK.value
        )

        merged_data = sorted(
            chain(
                light_positions.items(),
                self.sun_light_positions.items(),
                self.characterLightPositions.items(),
            ),
            key=itemgetter(0),
        )
        grouped_data = groupby(merged_data, key=itemgetter(0))
        return {k: max(map(itemgetter(1), g)) for k, g in grouped_data}
