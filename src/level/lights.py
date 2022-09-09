import random
from operator import itemgetter
from itertools import chain, groupby
from dataclasses import dataclass
from typing import Any

from constants import DIRECTIONS

T_object = Any


@dataclass
class Light_Data:
    surface: str = "LIGHT"
    to_surface: str = "WINDOW"
    font_size: int = 15
    color: tuple = (0, 0, 0)
    special_flags: str = "BLEND_RGB_ADD"
    position: tuple = None


class Lights:
    def __init__(self, grid_size: int) -> None:

        self.grid_size = grid_size
        self.grid_size_2D = (self.grid_size, self.grid_size)

        self.objs = []

    def update(
        self,
        paths: list[tuple[int, int]],
        path_start_position: tuple[int, int],
        path_finish_position: tuple[int, int],
        player_path_position: tuple[int, int],
        lights_state: bool,
        grid_size: int,
        brightness_list: list = [],
    ) -> T_object:

        self.light_positions = dict.fromkeys(paths, (0, 0, 0))

        self.character_light_positions = dict.fromkeys(paths, (0, 0, 0))

        x, brightness_list = self.set_color_value(1)

        self.set_lights_debug(
            lights_state,
            brightness_list,
        )

        source = self.set_light_source(paths)

        # print(f"{source=}")

        light_positions_adjacent_source = self.get_light_positions_adjacent_source(
            source, paths, grid_size
        )

        light_positions_adjacent = self.get_light_positions_adjacent(
            light_positions_adjacent_source, paths, grid_size
        )

        # print(f"{light_positions_adjacent=}")

        sun_light_positions = self.get_positions_sun(
            path_start_position, paths, brightness_list, path_finish_position, grid_size
        )

        character_light_positions = self.update_character_light_positions(
            self.character_light_positions,
            player_path_position,
            paths,
            brightness_list,
            grid_size,
        )

        light_positions = self.update_light_positions(
            self.light_positions,
            sun_light_positions,
            character_light_positions,
        )

        light_objs = [
            Light_Data(position=pos, color=color)
            for pos, color in light_positions.items()
            if color[0] > 0
        ]

        return light_objs

    def get_light_positions_adjacent(
        self,
        light_positions_adjacent: list[tuple[int, int]],
        paths: list[tuple[int, int]],
        grid_size,
    ) -> list[tuple[int, int]]:

        result = []
        for light in light_positions_adjacent:
            pos = (
                light["position"][0] + (light["direction"][0] * grid_size),
                light["position"][1] + (light["direction"][1] * grid_size),
            )
            if pos in paths:
                result.append(
                    {
                        "position": pos,
                        "direction": light["direction"],
                        "adjacent_by": light["adjacent_by"] + 1,
                    }
                )

        if len(result) > 0:
            result = self.get_light_positions_adjacent(result, paths, grid_size)

        light_positions_adjacent += result

        return light_positions_adjacent

    def get_light_positions_adjacent_source(
        self, source: tuple[int, int], path: list[tuple[int, int]], grid_size: int
    ):
        result = []
        for direction in DIRECTIONS:
            pos = (
                source[0] + (direction[0] * grid_size),
                source[1] + (direction[1] * grid_size),
            )
            if pos in path:
                result.append(
                    {
                        "position": pos,
                        "direction": direction,
                        "adjacent_by": 1,
                    }
                )
        return result

    # def get_light_data(self):
    #     pass

    def set_light_source(self, paths: list[tuple[int, int]]) -> tuple[int, int]:
        return random.choice(paths)

    def set_attrs_C_V_Data(
        self, pos: tuple[int, int], positions: list[tuple[int, int]]
    ) -> dict[str, Any]:
        return {
            "surface": "LIGHT",
            "to_surface": "WINDOW",
            "font_size": 15,
            "color": positions[pos],
            "special_flags": "BLEND_RGB_ADD",
            "pos": pos,
        }

    def set_color_value(self, x: int):
        brightness_list = []
        if x < 256:
            res, brightness_list = self.set_color_value((x * 2))
            res = int(res)
            if res >= 255:
                res += -1
            brightness_list.append(tuple([res] * 3))
        return x, brightness_list

    def set_lights_debug(self, lights_state: bool, brightness):
        # todo brightness not getting outside method!
        if lights_state:
            brightness = brightness[1]

    def update_character_light_positions(
        self,
        character_light_positions: list[tuple[int, int]],
        current_position: tuple[int, int],
        paths: list[tuple[int, int]],
        brightness_list,
        grid_size: int,
    ) -> list[tuple[int, int]]:
        mylist = [grid_size, -grid_size]
        for i in mylist:
            posslightposition = current_position
            brightness = 0
            run = True
            while run:
                if posslightposition in paths:
                    character_light_positions[posslightposition] = brightness_list[
                        brightness
                    ]
                    posslightposition = (posslightposition[0] + i, posslightposition[1])
                    if brightness < len(brightness_list) - 1:
                        brightness += 1
                else:
                    run = False
        for i in mylist:
            posslightposition = current_position
            brightness = 0
            run = True
            while run:
                if posslightposition in paths:
                    character_light_positions[posslightposition] = brightness_list[
                        brightness
                    ]
                    posslightposition = (posslightposition[0], posslightposition[1] + i)
                    if brightness < len(brightness_list) - 1:
                        brightness += 1
                else:
                    run = False
        character_light_positions[current_position] = (0, 0, 0)
        return character_light_positions

    def get_positions_sun(
        self,
        path_start_position: tuple[int, int],
        paths: list[tuple[int, int]],
        brightness_list,
        path_finish_position: tuple[int, int],
        grid_size: int,
    ):
        sun_light_positions = dict.fromkeys(paths, (0, 0, 0))

        for light_position in [path_start_position, path_finish_position]:
            brightness = 1

            while True:
                if not light_position in paths:
                    break
                sun_light_positions[light_position] = brightness_list[brightness]
                light_position = (light_position[0], light_position[1] + grid_size)
                if brightness < len(brightness_list) - 1:
                    brightness += 1

        return sun_light_positions

    def update_light_positions(
        self,
        light_positions: list[tuple[int, int]],
        sun_light_positions: list[tuple[int, int]],
        character_light_positions: list[tuple[int, int]],
    ):

        get_key, get_val = itemgetter(0), itemgetter(1)
        merged_data = sorted(
            chain(
                light_positions.items(),
                sun_light_positions.items(),
                character_light_positions.items(),
            ),
            key=get_key,
        )
        return {k: max(map(get_val, g)) for k, g in groupby(merged_data, key=get_key)}
