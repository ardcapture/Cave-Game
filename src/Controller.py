import random
import os
import numpy

import View
import Model

from PIL import Image
from operator import itemgetter
from itertools import chain, groupby, product
from collections import defaultdict

from blend_modes import lighten_only

from event import post_event

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

imagesPath = 'res'

DIRECTIONS = [(0, 1), (-1, 0), (1, 0), (0, -1)]

GRID_SIZE = 32
WIDTH, HEIGHT = (GRID_SIZE*2) + (GRID_SIZE * 35), (GRID_SIZE*2) + (GRID_SIZE * 22)
TOP_OFFSET = 5
AROUND = [-1, 0, 1]


COLOURS = {"BLACK": (0, 0, 0),
           "WHITE": (255, 255, 255),
           "BLACK_VERY_LIGHT": (210, 210, 210),
           "WHITE_4TH_4TH_4TH_4TH": (1, 1, 1),
           "RED": (255, 0, 0),
           "GREEN": (0, 255, 0),
           "BLUE": (0, 0, 255),
           "BLUE_LIGHT": (125, 125, 255),
           "BLUE_VERY_LIGHT": (210, 210, 255)}


rock_lighting_tile = Image.open(os.path.join(imagesPath, 'rock.png')).resize((GRID_SIZE, GRID_SIZE))
BlackSQ = Image.open(os.path.join(imagesPath, 'BlackSQ.png')).resize((GRID_SIZE, GRID_SIZE))


TILE_DIRECTIONS = {"T": (0, -1), "R": (1, 0), "B": (0, 1), "L": (-1, 0),
                   "TR": (1, -1), "BR": (1, 1), "BL": (-1, 1), "TL": (-1, -1)}


T_image = Image.open(os.path.join(imagesPath, 'I_Image_01.png')).resize((GRID_SIZE, GRID_SIZE))
TR_image = Image.open(os.path.join(imagesPath, 'Corner.png')).resize((GRID_SIZE, GRID_SIZE))

# Utilities:


def debug_instance_variables(self):
    print(f"* {self.__class__.__name__}.debug_instance_variables")

    for k in self.__dict__.keys():
        print(f"- {type(self).__name__}: {k}")


def get_distance_in_direction(position, direction):
    if direction == 'RIGHT':
        return (position[0] + GRID_SIZE, position[1])
    if direction == 'LEFT':
        return (position[0] - GRID_SIZE, position[1])
    if direction == 'DOWN':
        return (position[0], position[1] + GRID_SIZE)
    if direction == 'UP':
        return (position[0], position[1] - GRID_SIZE)


def position_to_grid_position(pos: tuple[int, int]):
    return tuple(map(lambda x: (x // GRID_SIZE) * GRID_SIZE, pos))


def get_list_difference(list01, list02):
    return [x for x in list01 if x not in list02]


class Game:
    def __init__(self):

        # Debugs:
        self.run_debug_state = False

        # game state controllers:

        self.keyboard_set_position = None
        self.mouse_event_run = None
        self.level = Level(self)
        # model and views:
        self.view = View.View(self)

        self.view.setup_view_event_handlers()

    # TODO _run/update too?

    def update(self):
        state = "build"

        while True:
            if state == "build":
                self.level.update_build()
                state = "run"
            if state == "run":
                self.level.update_run(
                    self.keyboard_set_position,
                    self.mouse_event_run
                )

                self.keyboard_set_position, self.mouse_event_run = post_event(
                    "update",
                    self.level,
                    self.run_debug_state,
                    self.level.path_obj.player_path_position
                )

    # TODO get state / event
    # TODO update (run object's update)
    # TODO end
    # TODO add object
    # TODO remove object


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

        self.build_path_positions = self.build.update()

        self.path = Paths()

        self.path_obj = self.path.update_build(
            build_path_positions=self.build_path_positions
        )

        if not self.path_obj:
            # self.view.draw_reset()  # TODO MOVE?
            self.reset()
            pass

        self.tile = Tile()
        self.lights = Lights()
        self.water = Water()
        self.surround = Surround()

    def update_build(self):

        self.water_datas = self.water.update(
            paths=self.path_obj.paths
        )

        self.sky = self.set_tileLocations_sky()
        self.rock = self.set_tileLocations_rock()
        self.grass = self.set_tileLocations_grass()

    def update_run(self,
                   set_position,
                   mouse_event_run
                   ):

        print(f"* {self.__class__.__name__}.update_run")

        self.path_climb_positions_visited = self.path.update_run(
            list_climb_positions=self.path_obj.list_climb_positions,
            player_path_position=self.path_obj.player_path_position,
            path_climb_positions_visited=self.path_climb_positions_visited,


        )

        self.light_objs = self.lights.update(
            paths=self.path_obj.paths,
            path_start_position=self.path_obj.path_start_position,
            path_finish_position=self.path_obj.path_finish_position,
            player_path_position=self.path_obj.player_path_position,
            lights_state=self.lights_state
        )

        #!!! two return!!
        self.surround_positions, self.path_adjacent = self.surround.update(
            paths=self.path_obj.paths
        )

        self.route_light_positions_tiles = self.tile.update(
            surround_positions=self.surround_positions
        )

        # debug_instance_variables(self)

        self.tiles = self.set_dict_tiles(self.rock, self.path_adjacent, self.sky, self.grass, self.path_obj.paths)

        if mouse_event_run:
            player_path_position = self.mouse_event_run(
                mouse_event_run,
                self.path_obj.camp_positions,
                self.path_obj.player_path_position,
                self.path_obj.paths,
                self.path_obj.path_type,
                self.path_obj.path_directions
            )

        player_path_position = self.get_player_path_position(
            set_position,
            self.path_obj.paths,
            self.path_obj.camp_positions,
            self.path_obj.player_path_position
        )

        print(f"- {player_path_position=}")

        self.path_obj.player_path_position = player_path_position

    def reset(self):
        print(f"reset")
        self.__init__(self)

    def set_tileLocations_sky(self):
        return [(x, y)
                for x in range(0, GRID_SIZE*(WIDTH//GRID_SIZE), GRID_SIZE)
                for y in range(0, GRID_SIZE*(TOP_OFFSET-1), GRID_SIZE)]

    def set_tileLocations_rock(self):
        return [(x, y)
                for x in range(0, GRID_SIZE*(WIDTH//GRID_SIZE), GRID_SIZE)
                for y in range(0, GRID_SIZE*(HEIGHT//GRID_SIZE), GRID_SIZE)]

    def set_tileLocations_grass(self):
        return [(x, y)
                for x in range(0, GRID_SIZE*(WIDTH//GRID_SIZE), GRID_SIZE)
                for y in range(GRID_SIZE*(TOP_OFFSET-1), GRID_SIZE*(TOP_OFFSET), GRID_SIZE)]

    def set_dict_tiles(self, rock, path_adjacent, sky, grass, paths):
        temp_tiles = {}
        for i in [(rock, 'R'), (path_adjacent, 'A'), (sky, 'S'), (grass, 'G'), (paths, 'P')]:
            temp_tiles.update(dict.fromkeys(*i))
        return temp_tiles

    #!!!! Class navigation?

    def mouse_event_run(self, res: tuple, camp_positions, player_path_position, paths, path_type, path_directions):
        res = position_to_grid_position(res)
        if res not in paths or res not in camp_positions:
            route = self.set_route(player_path_position, res, paths, camp_positions, path_type, path_directions)
            route_index = 0
            index = 1
            for i in route[route_index:]:  # TODO need breaking into steps
                index += 1
                player_path_position = self.get_player_path_position(i, paths, camp_positions, player_path_position)
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
            if path_type[route_list_A[-1]] <= path_type[route_list_B[-1]] or len(route_list_A) == 0:
                result = max(path_directions[route_list_A[-1]], key=path_type.get)
                route_list_A.append(result)
            if path_type[route_list_B[-1]] <= path_type[route_list_A[-1]] or len(route_list_B) == 0:
                result = max(path_directions[route_list_B[-1]], key=path_type.get)
                route_list_B.append(result)
            duplicate = [i for i in route_list_A if i in route_list_B]
            if duplicate:
                route_list_A.pop(-1)
                run = False
        route_list_B.reverse()
        route_list_A.extend(route_list_B)
        return route_list_A

    def get_player_path_position(self, event, paths, camp_positions, player_path_position):
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


class Tile():
    def update(self,
               surround_positions
               ):

        tileImages = self.get_surround_images()

        self.route_light_positions_tiles = self.set_path_surround_tiles(tileImages, surround_positions, debug=False, )

        return self.route_light_positions_tiles

    def get_surround_images(self):
        tileImages = {}
        image_types = ["T", "R", "B", "L", "TR", "BR", "BL", "TL"]
        for i in image_types:
            tileImages[i + "_image"] = self.get_lighting_tile(T_image, TR_image, i)
        return tileImages

    def set_path_surround_tiles(self, tileImages, path_surround_positions, debug) -> dict:
        route_light_positions_tiles = {}
        for k, v in path_surround_positions.items():
            if len(v) == 1:
                res = self.get_lighting_tile(T_image, TR_image, v[-1])
                res = res.convert('L')
                if not debug:
                    res = Image.composite(rock_lighting_tile, BlackSQ, res)
                name = "Tiles\\" + str(k) + ".PNG"
                res.save(name)
                route_light_positions_tiles[k] = name
            elif len(v) == 2:
                res = self.return_blended(tileImages[v[0] + "_image"], tileImages[v[1] + "_image"])
                res = res.convert('L')
                if not debug:
                    res = Image.composite(rock_lighting_tile, BlackSQ, res)
                name = "Tiles\\" + str(k) + ".PNG"
                res.save(name)
                route_light_positions_tiles[k] = name
            elif len(v) == 3:
                image01 = tileImages[v.pop() + "_image"]
                image02 = tileImages[v.pop() + "_image"]
                blend01 = self.return_blended(image01, image02)
                # blend01.show()
                image03 = tileImages[v.pop() + "_image"]
                blend02 = self.return_blended(blend01, image03)
                res = blend02
                res = res.convert('L')
                if not debug:
                    res = Image.composite(rock_lighting_tile, BlackSQ, res)
                name = "Tiles\\" + str(k) + ".PNG"
                res.save(name)
                route_light_positions_tiles[k] = name

        return route_light_positions_tiles

    def get_lighting_tile(self, TOP_image, TOPR_image, neighbor):
        if neighbor == "T":
            res = TOP_image.rotate(0)
        elif neighbor == "TR":
            res = TOPR_image.rotate(0)
        elif neighbor == "L":
            res = TOP_image.rotate(90)
        elif neighbor == "TL":
            res = TOPR_image.rotate(90)
        elif neighbor == "B":
            res = TOP_image.rotate(180)
        elif neighbor == "BL":
            res = TOPR_image.rotate(180)
        elif neighbor == "R":
            res = TOP_image.rotate(270)
        elif neighbor == "BR":
            res = TOPR_image.rotate(270)
        return res

    def return_blended(self, foreground_image, background_image):
        return self.get_darken(
            self.return_array(foreground_image),
            self.return_array(background_image)
        )

    def return_array(self, image):
        array = numpy.array(image)
        array = array.astype(float)
        return array

    def get_darken(self, image_float01, image_float02):
        opacity = 1.0
        # blended_img_float = darken_only(image_float01, image_float02, opacity)
        blended_img_float = lighten_only(image_float01, image_float02, opacity)
        blended_img = numpy.uint8(blended_img_float)
        blended_img_raw = Image.fromarray(blended_img)
        return blended_img_raw


class Surround:
    def update(self, paths):

        print(f"* {self.__class__.__name__}.update")

        path_adjacent = self.set_dict_path_adjacent(paths)  # todo may remove

        print(f"- path_adjacent: {len(path_adjacent)}")

        poss_surround_positions = self.set_poss_path_surround_positions(
            path_adjacent,
            paths,
        )

        surround_positions = self.set_path_surround_positions(
            poss_surround_positions,
        )

        print(f"- surround_positions: {len(surround_positions)}")

        debug_instance_variables(self)

        return surround_positions, path_adjacent

    def set_dict_path_adjacent(self, paths):
        return {self.tile(path, x, y): "fish"
                for path, x, y in product(paths, AROUND, AROUND)
                if self.tile(path, x, y) not in paths}

    def set_path_surround_positions(self, poss_path_surround_positions):
        duplicate_checks = ["TR", "BR", "TL", "BL", ]
        for v, s in product(poss_path_surround_positions.values(), duplicate_checks):
            if s in v and any(i in list(s) for i in v):
                v.remove(s)
        return poss_path_surround_positions

    def set_poss_path_surround_positions(self, path_adjacent, light_positions):
        d = defaultdict(list)
        for i, j, k in product(path_adjacent, AROUND, AROUND):
            tile = (i[0] + (j * GRID_SIZE), i[1] + (k * GRID_SIZE))
            if tile in light_positions:
                res = (list(TILE_DIRECTIONS.keys())[list(TILE_DIRECTIONS.values()).index((j, k))])
                d[i].append((res))
        return d

    def tile(self, path, x, y):
        return (path[0] + (x * GRID_SIZE), path[1] + (y * GRID_SIZE))


class Water:
    def update(self, paths: list = []):

        water_above_rock = self._get_water_above_rock(paths)
        water_collect_positions = self._get_water_collect_positions(paths, water_above_rock)
        water_waterline_positions = self._get_water_waterline_positions(paths)
        water_positions = self._get_water_positions(water_collect_positions, water_waterline_positions)

        debug_instance_variables(self)

        return [Model.Water_Data(position=w) for w in water_positions]

    def _get_water_above_rock(self, paths):
        return [(p[0], p[1])
                for p in paths
                if get_distance_in_direction(p, 'DOWN') not in paths]

    def _get_position_either_side(self, position):
        return [get_distance_in_direction(position, 'RIGHT'), get_distance_in_direction(position, 'LEFT')]

    def _get_water_collect_positions(self, paths, water_above_rock):

        start = len(water_above_rock)
        for index, p in enumerate(water_above_rock):
            if any(item in self._get_position_either_side(p)
                   for item in get_list_difference(paths, water_above_rock)):
                water_above_rock.pop(index)
        end = len(water_above_rock)

        if start != end:
            self._get_water_collect_positions(paths, water_above_rock)

        return water_above_rock

    def _get_water_waterline_positions(self, paths):
        return [p for p in paths if p[1] > ((HEIGHT - GRID_SIZE * 2) * (2/3))]

    def _get_water_positions(self, water_collect_positions, water_waterline_positions):
        return [x for x in water_waterline_positions if x not in water_collect_positions] + water_collect_positions


class Paths:
    def __init__(self):
        pass

        # self.route = []

    def update_build(self,
                     build_path_positions
                     ):

        poss_path_start_position = self.set_poss_path_start(build_path_positions)

        path_start_position = self.set_path_start_position(poss_path_start_position)

        poss_path_finish = self.set_poss_path_finish(build_path_positions)
        path_finish_position = self.set_path_finish_position(poss_path_finish)

        if not path_start_position or not path_finish_position:
            return None

        camp_positions = self.set_camp_positions(path_start_position)  # not required in v02

        paths = self.set_paths(
            build_path_positions,
            path_start_position,
            path_finish_position,
        )

        # FOR NAV
        list_climb_positions = self.set_climb(paths)

        # FOR NAV
        path_type, path_directions = self.set_navigation(paths, camp_positions)

        # FOR NAV
        player_path_position = random.choice(camp_positions)

        path_obj = Model.Path_Data(
            path_start_position=path_start_position,
            path_finish_position=path_start_position,
            list_climb_positions=list_climb_positions,
            paths=paths,
            camp_positions=camp_positions,
            player_path_position=player_path_position,
            path_type=path_type,
            path_directions=path_directions
        )

        return path_obj

    def update_run(self,
                   list_climb_positions,
                   player_path_position,
                   path_climb_positions_visited: list = [],
                   ):

        path_climb_positions_visited = self.update_player_climb_positions_visited(player_path_position, list_climb_positions, path_climb_positions_visited)

        debug_instance_variables(self)

        return path_climb_positions_visited

    def set_poss_path_start(self, past_positions: list):
        """For level."""
        return [p
                for p in past_positions
                if p[1] == GRID_SIZE * TOP_OFFSET
                if p[0] < ((WIDTH - GRID_SIZE * 2) * (1/3))]

    def set_path_start_position(self, poss_maze_start):
        if len(poss_maze_start) > 0:
            poss_maze_start = random.choice(poss_maze_start)
            return (poss_maze_start[0], poss_maze_start[1] - GRID_SIZE)
        else:
            return None

    def set_poss_path_finish(self, past_positions):
        return [p
                for p in past_positions
                if p[0] == WIDTH - (GRID_SIZE * 2)
                if p[1] > ((HEIGHT - GRID_SIZE * 2) * (2/3))]

    def set_path_finish_position(self, poss_maze_finish):
        if len(poss_maze_finish) > 0:
            poss_maze_finish = random.choice(poss_maze_finish)
            return (poss_maze_finish[0] + GRID_SIZE, poss_maze_finish[1])
        else:
            return None
        # TODO check if required
            # self.draw.draw(COLOURS["BLUE_VERY_LIGHT"], self.maze_finish_position[0], self.maze_finish_position[1])
        # else:
        #     # self.maze_finish = None

    def set_camp_positions(self, maze_start_position):
        return [(i, maze_start_position[1] - GRID_SIZE) for i in range(0, WIDTH, GRID_SIZE)]

    def set_paths(self, build_positions: list, maze_start_position: tuple, maze_finish_position: tuple):
        return build_positions + [maze_start_position, maze_finish_position]

    def set_climb(self, paths):
        """For Nav."""
        return [p
                for p in paths
                if get_distance_in_direction(p, 'UP') in paths
                or get_distance_in_direction(p, 'DOWN') in paths]

    def set_navigation(self, paths, camp_positions):
        """For Navigation."""
        path_type = dict.fromkeys(paths, "X")
        path_type.update(dict.fromkeys(camp_positions, "X"))
        path_directions_dict = dict.fromkeys(paths, [])
        for p in path_type.keys():
            path_directions_list = []
            for d in DIRECTIONS:
                direction = (p[0] + (d[0] * GRID_SIZE),
                             p[1] + (d[1] * GRID_SIZE))
                if direction in path_type:
                    path_directions_list.append(direction)
            if len(path_directions_list) == 1:
                path_type[p] = 1
                path_directions_dict[p] = path_directions_list
            elif len(path_directions_list) == 2:
                path_type[p] = "P"
                path_directions_dict[p] = path_directions_list
            elif len(path_directions_list) > 2:
                path_type[p] = "J"
                path_directions_dict[p] = path_directions_list
        for p in [k for k, v in path_type.items() if v == 1]:
            if path_type[path_directions_dict[p][0]] == "P":
                path_type[path_directions_dict[p][0]] = "N"

        run = True
        while run:
            if any([k for k, v in path_type.items() if v == "N"]):
                for k in [k for k, v in path_type.items() if v == "N"]:
                    for i in path_directions_dict[k]:
                        if isinstance(path_type[i], int):
                            result = path_type[i]
                        if path_type[i] == "P":
                            path_type[i] = "N"
                    path_type[k] = result + 1
            elif any([k for k, v in path_type.items() if v == "G"]):
                for k in [k for k, v in path_type.items() if v == "G"]:
                    result = 0
                    result_list02 = []
                    for i in path_directions_dict[k]:
                        if isinstance(path_type[i], int):
                            result_list02.append(path_type[i])
                        if isinstance(path_type[i], str):
                            path_type[i] = "N"
                    path_type[k] = sorted(result_list02)[-1] + 1
            elif any([k for k, v in path_type.items() if v == "J"]):
                for k, v in path_type.items():
                    if v == "J":
                        result_list = []
                        for i in path_directions_dict[k]:
                            if isinstance(path_type[i], int):
                                result_list.append(i)
                                if len(result_list) == (len(path_directions_dict[k]) - 1):
                                    if path_type[k] == "J":
                                        path_type[k] = "G"
            else:
                run = False

        return path_type, path_directions_dict

        """For Nav - currently used in game run."""

    def update_player_climb_positions_visited(self, player_current_position, path_climb_positions, path_climb_positions_visited=[]):
        if player_current_position in path_climb_positions and player_current_position not in path_climb_positions_visited:
            return path_climb_positions_visited + [player_current_position]
        else:
            return path_climb_positions_visited

    # !!! class build


class Build:
    def update(self):

        build_path_positions, build_positions = self.set_build_positions()

        return build_path_positions

    def set_build_positions(self):

        build_grid = self.set_build_grid()
        self.grid = self.build_grid_remove_random(build_grid)

        build_current_position = random.choice(build_grid)

        build_return_positions = []
        build_jump_positions = []
        build_positions = []

        while self.check_build_finish(build_positions, build_current_position):

            build_positions = self.update_build_past_positions(
                build_positions,
                build_current_position,
            )

            self.build_poss_next_positions = self.set_build_poss_next_positions(
                build_current_position,
                build_positions,
                build_grid,
            )

            build_next_position = self.set_build_next_position(
                build_current_position,
                build_positions,
                build_return_positions,
                self.build_poss_next_positions
            )

            build_current_break_direction = self.set_build_current_break_direction(
                build_next_position,
                build_current_position,
            )

            self.build_current_break_position = self.set_build_current_break_position(
                build_current_position,
                build_current_break_direction,
            )

            build_jump_positions = self.update_build_jump_positions(
                build_jump_positions,
                self.build_current_break_position,
            )

            build_current_position = build_next_position

        return build_positions + build_jump_positions, build_positions

    def build_grid_remove_random(self, grid):
        return [grid.remove(random.choice(grid))
                for i in range(len(grid) // 3)]

    def set_build_grid(self):
        return [(x, y)
                for x in range(GRID_SIZE, WIDTH, GRID_SIZE * 2)
                for y in range(GRID_SIZE * TOP_OFFSET, HEIGHT - (GRID_SIZE * 2), GRID_SIZE * 2)
                if (x, y)]

    def update_build_past_positions(self, past_positions: list, current_position: tuple):
        res = past_positions + [current_position]
        return res

    def set_build_poss_next_positions(self, current_position, past_positions, grid):
        return [self.set_poss_position(current_position, d)
                for d in random.sample(DIRECTIONS, len(DIRECTIONS))
                if self.set_poss_position(current_position, d) in grid
                and self.set_poss_position(current_position, d) not in past_positions]

    def update_build_jump_positions(self, path_jump_positions: list, current_wall_break_position: tuple):
        return [*path_jump_positions, current_wall_break_position]

    # TODO remove path_return variable
    def set_build_next_position(self, current_position, past_positions, path_return, poss_position):
        if len(poss_position) > 1:
            res = random.choices(poss_position, k=1, weights=[100, 100, 1, 1][:len(poss_position)])[0]
        elif len(poss_position) == 0:
            if current_position in past_positions:
                res = self.set_path_return(past_positions, current_position)
                path_return.append(res)
            else:
                res = past_positions[-1]
        elif len(poss_position) == 1:
            res = poss_position[0]

        return res

    def set_build_current_break_direction(self, next_position, current_position):
        return ((next_position[0] - current_position[0]) // 2, (next_position[1] - current_position[1]) // 2)

    def set_build_current_break_position(self, current_position, current_wall_break_direction):
        return (current_position[0] + current_wall_break_direction[0], current_position[1] + current_wall_break_direction[1])
        # self.list_wall_break_positions.append(result02)

    def check_build_finish(self, past_positions, current_position):
        """For level - path"""
        if len(past_positions) > 2 and current_position == past_positions[0]:
            return False
        else:
            return True

    def set_poss_position(self, current_position, direction):
        """For level - Paths."""
        return (current_position[0] + (direction[0] * GRID_SIZE * 2), current_position[1] + (direction[1] * GRID_SIZE * 2))

    def set_path_return(self, past_positions, current_position):
        """For level - Paths."""
        return past_positions[past_positions.index(current_position) - 1]

#!!! ********************************


class Lights:
    def __init__(self):

        self.grid_size = GRID_SIZE
        self.grid_size_2D = (self.grid_size, self.grid_size)

        self.objs = []

    def update(self,
               paths,
               path_start_position,
               path_finish_position,
               player_path_position,
               lights_state,
               brightness_list: list = []
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

        light_positions_adjacent_source = self.get_light_positions_adjacent_source(source, paths)

        light_positions_adjacent = self.get_light_positions_adjacent(light_positions_adjacent_source, paths)

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
            Model.Light_Data(
                position=pos,
                color=color)
            for pos, color in light_positions.items()
            if color[0] > 0
        ]

        return light_objs

    def get_light_positions_adjacent(self, light_positions_adjacent, paths):

        result = []
        for light in light_positions_adjacent:
            pos = (
                light["position"][0] + (light["direction"][0] * GRID_SIZE),
                light["position"][1] + (light["direction"][1] * GRID_SIZE)
            )
            if pos in paths:
                result.append({
                    "position": pos,
                    "direction": light["direction"],
                    "adjacent_by": light["adjacent_by"] + 1,
                })

        if len(result) > 0:
            result = self.get_light_positions_adjacent(result, paths)

        light_positions_adjacent += result

        return light_positions_adjacent

    def get_light_positions_adjacent_source(self, source: tuple, path: list):
        result = []
        for direction in DIRECTIONS:
            pos = (source[0] + (direction[0] * GRID_SIZE), source[1] + (direction[1] * GRID_SIZE))
            if pos in path:
                result.append({
                    "position": pos,
                    "direction": direction,
                    "adjacent_by": 1,
                })
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
            res, brightness_list = self.set_color_value((x*2))
            res = int(res)
            if res >= 255:
                res += -1
            brightness_list.append(tuple([res] * 3))
        return x, brightness_list

    def set_lights_debug(self, lights_state, brightness):
        if lights_state:
            brightness = brightness[1]

    def update_character_light_positions(self, character_light_positions, tuple_current_position, paths, brightness_list):
        mylist = [GRID_SIZE, -GRID_SIZE]
        for i in mylist:
            posslightposition = tuple_current_position
            brightness = 0
            run = True
            while run:
                if posslightposition in paths:
                    character_light_positions[posslightposition] = brightness_list[brightness]
                    posslightposition = (
                        posslightposition[0] + i, posslightposition[1])
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
                    character_light_positions[posslightposition] = brightness_list[brightness]
                    posslightposition = (
                        posslightposition[0], posslightposition[1] + i)
                    if brightness < len(brightness_list) - 1:
                        brightness += 1
                else:
                    run = False
        character_light_positions[tuple_current_position] = (0, 0, 0)
        return character_light_positions

    def get_positions_sun(self, path_start_position, paths, brightness_list, path_finish_position):
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

    def update_light_positions(self, light_positions, sun_light_positions, character_light_positions):

        get_key, get_val = itemgetter(0), itemgetter(1)
        merged_data = sorted(chain(light_positions.items(), sun_light_positions.items(), character_light_positions.items()), key=get_key)
        return {k: max(map(get_val, g))for k, g in groupby(merged_data, key=get_key)}


def main():
    game_new = Game()
    game_new.update()


if __name__ == '__main__':
    main()
