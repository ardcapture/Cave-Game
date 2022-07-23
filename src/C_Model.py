import logging
import random
import pygame
import os
import numpy

from PIL import Image
from operator import itemgetter
from itertools import chain, groupby, product
from collections import defaultdict
from blend_modes import lighten_only

# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logging.disable()

imagesPath = 'res'

DIRECTIONS = [(0, 1), (-1, 0), (1, 0), (0, -1)]

GRID_SIZE = 32
WIDTH, HEIGHT = (GRID_SIZE*2) + (GRID_SIZE * 35), (GRID_SIZE*2) + (GRID_SIZE * 22)
TOP_OFFSET = 5
AROUND = [-1, 0, 1]


win = pygame.Surface((WIDTH, HEIGHT))


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


# class object():
#     def __init__(self, drawable, position, dimensions, material, navigable):
#         self.position = position

#         self.drawable = drawable
#         self.dimensions = dimensions
#         self.material = material

#         self.navigable = navigable


class Game_OLD:
    def __init__(self):
        logging.debug("game old init")
        # self.draw = draw

        # TODO MAP

        # TODO MAP - PATH
        self.list_path_return = []
        self.path_jump_positions = []
        # self.path_return_positions = []
        self.path_past_positions = []

        self.path_start_position = (0, 0)
        self.path_finish_position = (0, 0)
        self.path_type = {}

        # self.dict_objects = {}
        # self.list_ends = []

        # TODO NAV
        self.path_directions = {}
        self.route = []

        # from character!!
        self.set_position_keys = ("K_LEFT", "K_RIGHT", "K_UP", "K_DOWN")
        self.previous_position = ()
        self.selected = False
        self.velocity = GRID_SIZE
        self.climb_positions_visited = []
        # self.list_water_list = self.list_water_list

        # lights
        self.brightness_list = []
        self.set_brightness(1)

        self.map_initialize()
        self.lights_initialize()

    # TODO CLASS MAP ****************************

    def map_initialize(self):

        self.list_grid = self.set_grid_v01()
        self.grid = self.grid_remove_random(self.list_grid)
        self.tuple_current_position = random.choice(self.list_grid)

        # LOOP
        self.build_paths()

        self.poss_maze_start = self.set_poss_maze_start(self.path_past_positions)
        self.path_start_position = self.set_maze_start_position(self.poss_maze_start)
        self.poss_maze_finish = self.set_poss_maze_finish(self.path_past_positions)
        self.path_finish_position = self.set_maze_finish_position(self.poss_maze_finish)

        if self.path_finish_position == (0, 0) or self.path_start_position == (0, 0):
            # self.view.draw_reset()  # TODO MOVE?
            self.reset()
            pass

        self.camp_positions = self.set_camp_positions_list(self.path_start_position)  # not required in v02
        self.sky = self.set_tileLocations_sky()
        self.rock = self.set_tileLocations_rock()
        self.grass = self.set_tileLocations_grass()
        # level.earth = level.set_tileLocations_earth(level.top_offset) #used in v02 too

        self.paths = self.set_paths(
            self.path_past_positions,
            self.path_jump_positions,
            self.path_start_position,
            self.path_finish_position,
        )

        self.path_adjacent = self.set_dict_path_adjacent()  # todo may remove
        self.tiles = self.set_dict_tiles(self.rock, self.path_adjacent, self.sky, self.grass, self.paths)
        self.list_water_list = self.setWater(self.paths, self.set_above_rock(self.paths))  # todo turn back on in a bit

        # FOR MAP
        self.set_tileImages()

        # FOR NAV
        self.list_climb_positions = self.set_climb(self.paths)

        # FOR NAV
        self.set_navigation()

        # FOR NAV
        self.tuple_current_position = random.choice(self.camp_positions)

    def lights_initialize(self):
        """For lights."""
        self.light_positions = dict.fromkeys(self.paths, (0, 0, 0))
        self.character_light_positions = dict.fromkeys(self.paths, (0, 0, 0))
        self.sun_light_positions = dict.fromkeys(self.paths, (0, 0, 0))

        self.route_light_positions = self.set_path_surround_positions(self.path_adjacent, self.light_positions)

        # self.set_path_surround_tiles(debug='FALSE')

    def reset(self):
        """For map."""
        self.__init__()

    def update_past_positions(self, past_positions: list, current_position: tuple):
        """For map."""
        self.path_past_positions =  past_positions + [current_position]

    def set_camp_positions_list(self, maze_start_position):
        """For map."""
        return [(i, maze_start_position[1] - GRID_SIZE) for i in range(0, WIDTH, GRID_SIZE)]

    def set_paths(self, past_positions: list, wall_break_positions: list, maze_start_position: tuple, maze_finish_position: tuple):
        """For map."""
        return past_positions + wall_break_positions + [maze_start_position, maze_finish_position]

    # VARIOUS

    def tile(self, path, x, y):
        return (path[0] + (x * GRID_SIZE), path[1] + (y * GRID_SIZE))

    # TODO may remove this

    def set_dict_path_adjacent(self):
        """For map."""
        return {self.tile(path, x, y): "fish"
                for path, x, y in product(self.paths, AROUND, AROUND)
                if self.tile(path, x, y) not in self.paths}

    def set_tileLocations_sky(self):
        """For map."""
        return [(x, y)
                for x in range(0, GRID_SIZE*(WIDTH//GRID_SIZE), GRID_SIZE)
                for y in range(0, GRID_SIZE*(TOP_OFFSET-1), GRID_SIZE)]

    def set_tileLocations_rock(self):
        """For map."""
        return [(x, y)
                for x in range(0, GRID_SIZE*(WIDTH//GRID_SIZE), GRID_SIZE)
                for y in range(0, GRID_SIZE*(HEIGHT//GRID_SIZE), GRID_SIZE)]

    def set_tileLocations_grass(self):
        """For map."""
        return [(x, y)
                for x in range(0, GRID_SIZE*(WIDTH//GRID_SIZE), GRID_SIZE)
                for y in range(GRID_SIZE*(TOP_OFFSET-1), GRID_SIZE*(TOP_OFFSET), GRID_SIZE)]

    def set_dict_tiles(self, rock, path_adjacent, sky, grass, paths):
        """For map."""
        # dict
        temp_tiles = {}
        for i in [(rock, 'R'), (path_adjacent, 'A'), (sky, 'S'), (grass, 'G'), (paths, 'P')]:
            temp_tiles.update(dict.fromkeys(*i))
        return temp_tiles

    # TODO MOVE TO BUILD CLASS?

    def set_poss_maze_start(self, past_positions: list):
        """For map."""
        return [p
                for p in past_positions
                if p[1] == GRID_SIZE * TOP_OFFSET
                if p[0] < ((WIDTH - GRID_SIZE * 2) * (1/3))]

    def set_maze_start_position(self, poss_maze_start):
        """For map."""
        # return tuple
        if len(poss_maze_start) > 0:
            poss_maze_start = random.choice(poss_maze_start)
            return (poss_maze_start[0], poss_maze_start[1] - GRID_SIZE)
        else:
            return (0, 0)

    def set_poss_maze_finish(self, past_positions):
        """For map."""
        return [p
                for p in past_positions
                if p[0] == WIDTH - (GRID_SIZE * 2)
                if p[1] > ((HEIGHT - GRID_SIZE * 2) * (2/3))]

    def set_maze_finish_position(self, poss_maze_finish):
        """For map."""
        if len(poss_maze_finish) > 0:
            poss_maze_finish = random.choice(poss_maze_finish)
            return (poss_maze_finish[0] + GRID_SIZE, poss_maze_finish[1])
        else:
            return (0, 0)
        # TODO check if required
            # self.draw.draw(COLOURS["BLUE_VERY_LIGHT"], self.maze_finish_position[0], self.maze_finish_position[1])
        # else:
        #     # self.maze_finish = None

    def grid_remove_random(self, grid):
        """For map."""
        return [grid.remove(random.choice(grid))
                for i in range(len(grid) // 3)]

    def set_grid_v01(self):
        """For map."""
        return [(x, y)
                for x in range(GRID_SIZE, WIDTH, GRID_SIZE * 2)
                for y in range(GRID_SIZE * TOP_OFFSET, HEIGHT - (GRID_SIZE * 2), GRID_SIZE * 2)
                if (x, y)]

    def set_current_wall_break_direction(self, next_position, current_position):
        """For map - path"""
        self.current_wall_break_direction = ((next_position[0] - current_position[0]) // 2, (next_position[1] - current_position[1]) // 2)

    def set_current_wall_break_position(self, current_position, current_wall_break_direction):
        """For map - path"""
        self.current_wall_break_position = (current_position[0] + current_wall_break_direction[0], current_position[1] + current_wall_break_direction[1])
        # self.list_wall_break_positions.append(result02)

    def check_maze_finish(self, past_positions, current_position):
        """For map - path"""
        if len(past_positions) > 2 and current_position == past_positions[0]:
            return False
        else:
            return True

    # VARIOUS
    def get_distance_in_direction(self, position, direction):
        if direction == 'RIGHT':
            return (position[0] + GRID_SIZE, position[1])
        if direction == 'LEFT':
            return (position[0] - GRID_SIZE, position[1])
        if direction == 'DOWN':
            return (position[0], position[1] + GRID_SIZE)
        if direction == 'UP':
            return (position[0], position[1] - GRID_SIZE)

    def set_above_rock(self, paths):
        """For map."""
        return [(p[0], p[1])
                for p in paths
                if self.get_distance_in_direction(p, 'DOWN') not in paths]

    def setWater(self, paths, poss_water_list):
        """For map."""
        # REMOVE HORIZONTAL INTO HOLE
        not_water_list = []
        run = True
        while run:
            start = len(poss_water_list)

            for p in poss_water_list:
                if any(item in [self.get_distance_in_direction(p, 'RIGHT'), self.get_distance_in_direction(p, 'LEFT')] for item in [x for x in paths if x not in poss_water_list]):
                    not_water_list.append(p)
                    poss_water_list.remove(p)
            end = len(poss_water_list)
            if start == end:
                run = False

        # return [p for p in paths if p[1] > ((HEIGHT - GRID_SIZE * 2) * (2/3))]

        for p in paths:
            if p[1] > ((HEIGHT - GRID_SIZE * 2) * (2/3)):
                poss_water_list.append(p)

        return poss_water_list

    def set_climb(self, paths):
        """For Nav."""
        return [p
                for p in paths
                if self.get_distance_in_direction(p, 'UP') in paths
                or self.get_distance_in_direction(p, 'DOWN') in paths]

    def build_paths(self):
        """For Map."""

        while self.check_maze_finish(self.path_past_positions,
                                     self.tuple_current_position):

            # ! V01

            logging.debug("build paths")
            # print('self.path_past_positions: ', self.path_past_positions, '\n',
            # 'self.tuple_current_position: ', self.tuple_current_position)

            self.update_past_positions(self.path_past_positions, self.tuple_current_position)

            self.set_poss_postions(self.tuple_current_position, self.path_past_positions, self.list_grid)

            self.set_next_position(self.tuple_current_position,
                                   self.path_past_positions,
                                   self.list_path_return,
                                   self.poss_position)

            self.set_current_wall_break_direction(self.list_next_position, self.tuple_current_position)

            self.set_current_wall_break_position(self.tuple_current_position, self.current_wall_break_direction)

            self.update_path_jump_positions(self.path_jump_positions, self.current_wall_break_position)

            self.tuple_current_position=self.list_next_position

    def set_poss_position(self, current_position, direction):
        """For Map - Paths."""
        return (current_position[0] + (direction[0] * GRID_SIZE * 2), current_position[1] + (direction[1] * GRID_SIZE * 2))

    def set_poss_postions(self, current_position, past_positions, grid):
        """For Map - Paths."""
        self.poss_position=[self.set_poss_position(current_position, d)
                              for d in random.sample(DIRECTIONS, len(DIRECTIONS))
                              if self.set_poss_position(current_position, d) in grid
                              and self.set_poss_position(current_position, d) not in past_positions]

    def update_path_jump_positions(self, path_jump_positions: list, current_wall_break_position: tuple):
        """For Map - Paths."""
        self.path_jump_positions = [*path_jump_positions, current_wall_break_position]

    def set_next_position(self, current_position, past_positions, path_return, poss_position):
        """For Map - Paths."""
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

        self.list_next_position = res

    def set_path_return(self, past_positions, current_position):
        """For Map - Paths."""
        return past_positions[past_positions.index(current_position) - 1]

    def set_navigation(self):
        """For Navigation."""
        self.path_type = dict.fromkeys(self.paths, "X")
        self.path_type.update(dict.fromkeys(self.camp_positions, "X"))
        self.path_directions = dict.fromkeys(self.paths, [])
        for p in self.path_type.keys():
            path_directions = []
            for d in DIRECTIONS:
                direction = (p[0] + (d[0] * GRID_SIZE),
                             p[1] + (d[1] * GRID_SIZE))
                if direction in self.path_type:
                    path_directions.append(direction)
            if len(path_directions) == 1:
                self.path_type[p] = 1
                self.path_directions[p] = path_directions
            elif len(path_directions) == 2:
                self.path_type[p] = "P"
                self.path_directions[p] = path_directions
            elif len(path_directions) > 2:
                self.path_type[p] = "J"
                self.path_directions[p] = path_directions
        for p in [k for k, v in self.path_type.items() if v == 1]:
            if self.path_type[self.path_directions[p][0]] == "P":
                self.path_type[self.path_directions[p][0]] = "N"

        run = True
        while run:
            if any([k for k, v in self.path_type.items() if v == "N"]):
                for k in [k for k, v in self.path_type.items() if v == "N"]:
                    for i in self.path_directions[k]:
                        if isinstance(self.path_type[i], int):
                            result = self.path_type[i]
                        if self.path_type[i] == "P":
                            self.path_type[i] = "N"
                    self.path_type[k] = result + 1
            elif any([k for k, v in self.path_type.items() if v == "G"]):
                for k in [k for k, v in self.path_type.items() if v == "G"]:
                    result = 0
                    result_list02 = []
                    for i in self.path_directions[k]:
                        if isinstance(self.path_type[i], int):
                            result_list02.append(self.path_type[i])
                        if isinstance(self.path_type[i], str):
                            self.path_type[i] = "N"
                    self.path_type[k] = sorted(result_list02)[-1] + 1
            elif any([k for k, v in self.path_type.items() if v == "J"]):
                for k, v in self.path_type.items():
                    if v == "J":
                        result_list = []
                        for i in self.path_directions[k]:
                            if isinstance(self.path_type[i], int):
                                result_list.append(i)
                                if len(result_list) == (len(self.path_directions[k]) - 1):
                                    if self.path_type[k] == "J":
                                        self.path_type[k] = "G"
            else:
                run = False

    def set_route(self, start, end, level):
        """For Nav - currently used in controller."""
        route_list_A = [start]
        if end in level.paths or end in level.camp_positions:
            route_list_B = [end]
        else:
            route_list_B = [start]
        run = True
        while run:
            if self.path_type[route_list_A[-1]] <= self.path_type[route_list_B[-1]] or len(route_list_A) == 0:
                result = max(self.path_directions[route_list_A[-1]], key=self.path_type.get)
                route_list_A.append(result)
            if self.path_type[route_list_B[-1]] <= self.path_type[route_list_A[-1]] or len(route_list_B) == 0:
                result = max(self.path_directions[route_list_B[-1]], key=self.path_type.get)
                route_list_B.append(result)
            duplicate = [i for i in route_list_A if i in route_list_B]
            if duplicate:
                route_list_A.pop(-1)
                run = False
        route_list_B.reverse()
        route_list_A.extend(route_list_B)
        self.route = route_list_A

    def set_position(self, event):
        """For Nav - currently used in controller."""
        x, y = self.tuple_current_position
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
        if (x, y) in self.paths or (x, y) in self.camp_positions:
            self.tuple_current_position = (x, y)
            pygame.time.delay(150)

        """For Nav - currently used in game run."""

    def set_climb_positions_visited(self, tuple_current_position, list_climb_positions, climb_positions_visited):
        if tuple_current_position in list_climb_positions:
            climb_positions_visited.append(tuple_current_position)

    def set_brightness(self, x: int):
        """For lights."""
        self.brightness_list = []
        if x < 256:
            res = self.set_brightness((x*2))
            res = int(res)
            if res >= 255:
                res += -1
            self.brightness_list.append(tuple([res] * 3))
        return x

    def set_lights_debug(self, lights_state, brightness):
        """For lights."""
        if lights_state:
            brightness = brightness[1]

    def update_character_light_positions(self, character_light_positions, tuple_current_position, paths, brightness_list):
        """For lights."""
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

    def set_lights_sun(self, tuple_maze_start_position, paths, sun_light_positions, brightness_list, tuple_maze_finish_position):
        """For lights."""
        posslightposition = tuple_maze_start_position
        brightness = 1
        run = True
        while run:
            if posslightposition in paths:
                sun_light_positions[posslightposition] = brightness_list[brightness]
                posslightposition = (posslightposition[0], posslightposition[1] + GRID_SIZE)
                if brightness < len(brightness_list) - 1:
                    brightness += 1
            else:
                run = False
        posslightposition = tuple_maze_finish_position
        brightness = 1
        run = True
        while run:
            if posslightposition in paths:
                sun_light_positions[posslightposition] = brightness_list[brightness]
                posslightposition = (posslightposition[0] - GRID_SIZE, posslightposition[1])
                if brightness < len(self.brightness_list) - 1:
                    brightness += 1
            else:
                run = False

    def update_light_positions(self, paths, sun_light_positions, character_light_positions, light_positions):
        """For lights"""
        get_key, get_val = itemgetter(0), itemgetter(1)
        merged_data = sorted(chain(light_positions.items(), sun_light_positions.items(), character_light_positions.items()), key=get_key)
        return {k: max(map(get_val, g))for k, g in groupby(merged_data, key=get_key)}

    def return_array(self, image):
        """For map - path surround tiles."""
        array = numpy.array(image)
        array = array.astype(float)
        return array

    def return_darken(self, image_float01, image_float02):
        """For map - path surround tiles."""
        opacity = 1.0
        # blended_img_float = darken_only(image_float01, image_float02, opacity)
        blended_img_float = lighten_only(image_float01, image_float02, opacity)
        blended_img = numpy.uint8(blended_img_float)
        blended_img_raw = Image.fromarray(blended_img)
        return blended_img_raw

    def return_lighting_tile(self, TOP_image, TOPR_image, neighbor):
        """For map - path surround tiles."""
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

    def return_blended(self, neighbors01, neighbors02):
        """For map - path surround tiles."""
        foreground_image = neighbors01
        background_image = neighbors02
        forground_array = self.return_array(foreground_image)
        background_array = self.return_array(background_image)
        res = self.return_darken(forground_array, background_array)
        return res

    # FOR MAP
    def set_tileImages(self):
        """For map - path surround tiles."""
        self.tileImages = {}
        image_types = ["T", "R", "B", "L", "TR", "BR", "BL", "TL"]
        for i in image_types:
            self.tileImages[i + "_image"] = self.return_lighting_tile(T_image, TR_image, i)

    def set_path_surround_positions(self, path_adjacent, light_positions):
        """For map - path surround tiles."""
        d = defaultdict(list)
        for i in path_adjacent:
            AROUND = [-1, 0, 1]
            for j in AROUND:
                for k in AROUND:
                    tile = (i[0] + (j * GRID_SIZE), i[1] + (k * GRID_SIZE))
                    if tile in light_positions:
                        res = (list(TILE_DIRECTIONS.keys())[list(TILE_DIRECTIONS.values()).index((j, k))])
                        d[i].append((res))
        temp_route_light_positions = d
        for k, v in temp_route_light_positions.items():
            if "TR" in v:
                if "T" in v or "R" in v:
                    v.remove("TR")
            if "BR" in v:
                if "B" in v or "R" in v:
                    v.remove("BR")

            if "TL" in v:
                if "T" in v or "L" in v:
                    v.remove("TL")
            if "BL" in v:
                if "B" in v or "L" in v:
                    v.remove("BL")
        return temp_route_light_positions

    def set_path_surround_tiles(self, debug):
        """For map - path surround tiles."""
        self.route_light_positions_tiles = {}
        for k, v in self.route_light_positions.items():
            if len(v) == 1:
                res = self.return_lighting_tile(T_image, TR_image, v[-1])
                res = res.convert('L')
                if debug == 'FALSE':
                    res = Image.composite(rock_lighting_tile, BlackSQ, res)
                name = "Tiles\\" + str(k) + ".PNG"
                res.save(name)
                self.route_light_positions_tiles[k] = name
            elif len(v) == 2:
                res = self.return_blended(self.tileImages[v[0] + "_image"], self.tileImages[v[1] + "_image"])
                res = res.convert('L')
                if debug == 'FALSE':
                    res = Image.composite(rock_lighting_tile, BlackSQ, res)
                name = "Tiles\\" + str(k) + ".PNG"
                res.save(name)
                self.route_light_positions_tiles[k] = name
            elif len(v) == 3:
                image01 = self.tileImages[v.pop() + "_image"]
                image02 = self.tileImages[v.pop() + "_image"]
                blend01 = self.return_blended(image01, image02)
                # blend01.show()
                image03 = self.tileImages[v.pop() + "_image"]
                blend02 = self.return_blended(blend01, image03)
                res = blend02
                res = res.convert('L')
                if debug == 'FALSE':
                    res = Image.composite(rock_lighting_tile, BlackSQ, res)
                name = "Tiles\\" + str(k) + ".PNG"
                res.save(name)
                self.route_light_positions_tiles[k] = name
