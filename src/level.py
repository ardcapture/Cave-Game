import random
import os
import numpy


from operator import itemgetter
from itertools import chain, groupby, product
from collections import defaultdict

from surround import Surround
from water import Water
from paths import Paths
from build import Build
from constants import DIRECTIONS

import view
import Model


from utilities import (
    debug_instance_variables,
    get_distance_in_direction,
    get_list_difference,
)


LevelStates = ["01_Title", "02_Settings", "03_Build", "04_Play"]
game_keys = "K_BACKQUOTE"


# build_debug = True


# TODO may not get used!
state = {
    # "title": title,
    # "level_build": build,
    # "level_run": level_run,
    # "level_pause": level_pause
}


GRID_SIZE = 32
WIDTH, HEIGHT = (GRID_SIZE * 2) + (GRID_SIZE * 35), (GRID_SIZE * 2) + (GRID_SIZE * 22)
TOP_OFFSET = 5


COLOURS = {
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "BLACK_VERY_LIGHT": (210, 210, 210),
    "WHITE_4TH_4TH_4TH_4TH": (1, 1, 1),
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "BLUE_LIGHT": (125, 125, 255),
    "BLUE_VERY_LIGHT": (210, 210, 255),
}


class Level:
    def __init__(self, controller):

        self.objs = []

        # Debugs:

        self.path_climb_positions_visited = []
        self.lights_state = False

        self.parent = controller

        # from character!!
        self.set_position_keys = ("K_LEFT", "K_RIGHT", "K_UP", "K_DOWN")
        self.previous_position = ()
        self.selected = False
        self.velocity = GRID_SIZE

        self.build = Build()

        self.build_path_positions = self.build.update(GRID_SIZE, WIDTH, TOP_OFFSET, HEIGHT)

        self.path = Paths()

        self.path_obj = self.path.update_build(
            build_path_positions=self.build_path_positions,
            grid_size=GRID_SIZE,
            top_offset=TOP_OFFSET,
            width=WIDTH,
            height=HEIGHT,
        )

        if not self.path_obj:
            # self.view.draw_reset()  # TODO MOVE?
            self.reset()
            pass

        self.tile = view.Tile()
        self.lights = Lights()
        self.water = Water()
        self.surround = Surround()

    def update_build(self):

        self.water_datas = self.water.update(
            GRID_SIZE, HEIGHT, paths=self.path_obj.paths
        )

        self.sky = self.set_tileLocations_sky()
        self.rock = self.set_tileLocations_rock()
        self.grass = self.set_tileLocations_grass()

    def update_run(self, set_position, mouse_event_run):

        print(f"* {self.__class__.__name__}.update_run")

        self.path_climb_positions_visited = self.path.update_run(
            climb_positions=self.path_obj.climb_positions,
            player_path_position=self.path_obj.player_path_position,
            path_climb_positions_visited=self.path_climb_positions_visited,
        )

        self.light_objs = self.lights.update(
            paths=self.path_obj.paths,
            path_start_position=self.path_obj.path_start_position,
            path_finish_position=self.path_obj.path_finish_position,
            player_path_position=self.path_obj.player_path_position,
            lights_state=self.lights_state,
        )

        #!!! two return!!
        self.surround_positions, self.path_adjacent = self.surround.update(
            paths=self.path_obj.paths, grid_size=GRID_SIZE
        )

        self.route_light_positions_tiles = self.tile.update(
            surround_positions=self.surround_positions
        )

        # debug_instance_variables(self)

        self.tiles = self.set_dict_tiles(
            self.rock, self.path_adjacent, self.sky, self.grass, self.path_obj.paths
        )

        if mouse_event_run:
            player_path_position = self.mouse_event_run(
                mouse_event_run,
                self.path_obj.camp_positions,
                self.path_obj.player_path_position,
                self.path_obj.paths,
                self.path_obj.path_type,
                self.path_obj.path_directions,
            )

        player_path_position = self.get_player_path_position(
            set_position,
            self.path_obj.paths,
            self.path_obj.camp_positions,
            self.path_obj.player_path_position,
        )

        print(f"- {player_path_position=}")

        self.path_obj.player_path_position = player_path_position

    def reset(self):
        print(f"reset")
        self.__init__(self)

    def set_tileLocations_sky(self):
        return [
            (x, y)
            for x in range(0, GRID_SIZE * (WIDTH // GRID_SIZE), GRID_SIZE)
            for y in range(0, GRID_SIZE * (TOP_OFFSET - 1), GRID_SIZE)
        ]

    def set_tileLocations_rock(self):
        return [
            (x, y)
            for x in range(0, GRID_SIZE * (WIDTH // GRID_SIZE), GRID_SIZE)
            for y in range(0, GRID_SIZE * (HEIGHT // GRID_SIZE), GRID_SIZE)
        ]

    def set_tileLocations_grass(self):
        return [
            (x, y)
            for x in range(0, GRID_SIZE * (WIDTH // GRID_SIZE), GRID_SIZE)
            for y in range(
                GRID_SIZE * (TOP_OFFSET - 1), GRID_SIZE * (TOP_OFFSET), GRID_SIZE
            )
        ]

    def set_dict_tiles(self, rock, path_adjacent, sky, grass, paths):
        temp_tiles = {}
        for i in [
            (rock, "R"),
            (path_adjacent, "A"),
            (sky, "S"),
            (grass, "G"),
            (paths, "P"),
        ]:
            temp_tiles.update(dict.fromkeys(*i))
        return temp_tiles

    #!!!! Class navigation?

    def mouse_event_run(
        self,
        res: tuple,
        camp_positions,
        player_path_position,
        paths,
        path_type,
        path_directions,
    ):
        res = position_to_grid_position(res)
        if res not in paths or res not in camp_positions:
            route = self.set_route(
                player_path_position,
                res,
                paths,
                camp_positions,
                path_type,
                path_directions,
            )
            route_index = 0
            index = 1
            for i in route[route_index:]:  # TODO need breaking into steps
                index += 1
                player_path_position = self.get_player_path_position(
                    i, paths, camp_positions, player_path_position
                )
                print("walk", index, player_path_position)
        return player_path_position

    def set_route(self, start, end, paths, camp_positions, path_type, path_directions):
        """For Nav - currently used in controller."""
        route_list_A = [start]
        if end in paths or end in camp_positions:
            route_list_B = [end]
        else:
            route_list_B = [start]
        run = True
        while run:
            if (
                path_type[route_list_A[-1]] <= path_type[route_list_B[-1]]
                or len(route_list_A) == 0
            ):
                result = max(path_directions[route_list_A[-1]], key=path_type.get)
                route_list_A.append(result)
            if (
                path_type[route_list_B[-1]] <= path_type[route_list_A[-1]]
                or len(route_list_B) == 0
            ):
                result = max(path_directions[route_list_B[-1]], key=path_type.get)
                route_list_B.append(result)
            duplicate = [i for i in route_list_A if i in route_list_B]
            if duplicate:
                route_list_A.pop(-1)
                run = False
        route_list_B.reverse()
        route_list_A.extend(route_list_B)
        return route_list_A

    def get_player_path_position(
        self, event, paths, camp_positions, player_path_position
    ):
        x, y = player_path_position
        if event == "K_LEFT":
            x -= self.velocity
        elif event == "K_RIGHT":
            x += self.velocity
        elif event == "K_UP":
            y -= self.velocity
        elif event == "K_DOWN":
            y += self.velocity
        elif isinstance(event, tuple):
            x, y = event
        if (x, y) in paths or (x, y) in camp_positions:
            return (x, y)

    #!!!! *******************************************


class Lights:
    def __init__(self):

        self.grid_size = GRID_SIZE
        self.grid_size_2D = (self.grid_size, self.grid_size)

        self.objs = []

    def update(
        self,
        paths,
        path_start_position,
        path_finish_position,
        player_path_position,
        lights_state,
        brightness_list: list = [],
    ):

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
            source, paths
        )

        light_positions_adjacent = self.get_light_positions_adjacent(
            light_positions_adjacent_source, paths
        )

        # print(f"{light_positions_adjacent=}")

        sun_light_positions = self.get_positions_sun(
            path_start_position,
            paths,
            brightness_list,
            path_finish_position,
        )

        character_light_positions = self.update_character_light_positions(
            self.character_light_positions,
            player_path_position,
            paths,
            brightness_list,
        )

        light_positions = self.update_light_positions(
            self.light_positions,
            sun_light_positions,
            character_light_positions,
        )

        light_objs = [
            Model.Light_Data(position=pos, color=color)
            for pos, color in light_positions.items()
            if color[0] > 0
        ]

        return light_objs

    def get_light_positions_adjacent(self, light_positions_adjacent, paths):

        result = []
        for light in light_positions_adjacent:
            pos = (
                light["position"][0] + (light["direction"][0] * GRID_SIZE),
                light["position"][1] + (light["direction"][1] * GRID_SIZE),
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
            result = self.get_light_positions_adjacent(result, paths)

        light_positions_adjacent += result

        return light_positions_adjacent

    def get_light_positions_adjacent_source(self, source: tuple, path: list):
        result = []
        for direction in DIRECTIONS:
            pos = (
                source[0] + (direction[0] * GRID_SIZE),
                source[1] + (direction[1] * GRID_SIZE),
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

    def get_light_data(self):
        pass

    def set_light_source(self, paths):
        return random.choice(paths)

    def set_attrs_C_V_Data(self, pos, positions):
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

    def set_lights_debug(self, lights_state, brightness):
        if lights_state:
            brightness = brightness[1]

    def update_character_light_positions(
        self, character_light_positions, tuple_current_position, paths, brightness_list
    ):
        mylist = [GRID_SIZE, -GRID_SIZE]
        for i in mylist:
            posslightposition = tuple_current_position
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
            posslightposition = tuple_current_position
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
        character_light_positions[tuple_current_position] = (0, 0, 0)
        return character_light_positions

    def get_positions_sun(
        self, path_start_position, paths, brightness_list, path_finish_position
    ):
        sun_light_positions = dict.fromkeys(paths, (0, 0, 0))

        for light_position in [path_start_position, path_finish_position]:
            brightness = 1

            while True:
                if not light_position in paths:
                    break
                sun_light_positions[light_position] = brightness_list[brightness]
                light_position = (light_position[0], light_position[1] + GRID_SIZE)
                if brightness < len(brightness_list) - 1:
                    brightness += 1

        return sun_light_positions

    def update_light_positions(
        self, light_positions, sun_light_positions, character_light_positions
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
