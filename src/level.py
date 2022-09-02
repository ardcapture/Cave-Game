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
from lights import Lights
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

        self.build_path_positions = self.build.update(
            GRID_SIZE, WIDTH, TOP_OFFSET, HEIGHT
        )

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
        self.lights = Lights(GRID_SIZE)
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
            grid_size=GRID_SIZE,
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
