import random
from re import I
import pygame
import os
import numpy

from PIL import Image, ImageFont, ImageDraw, ImageOps
from operator import itemgetter
from itertools import chain, groupby, product
from collections import defaultdict
from blend_modes import darken_only, lighten_only
from pygame import color
# from dataclasses import dataclass


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


# @dataclass
# class Object:
#     drawable: bool


class object():
    def __init__(self, drawable, position, dimensions, material, navigable):
        self.position = position

        self.drawable = drawable
        self.dimensions = dimensions
        self.material = material

        self.navigable = navigable


class Model():
    def __init__(self):
        # self.draw = draw

        self.list_next_position = []
        self.list_path_return = []
        self.list_wall_break_positions = []
        self.list_past_positions = []
        self.tuple_maze_start_position = (0, 0)
        self.tuple_maze_finish_position = (0, 0)
        self.list_water_list = []
        self.list_climb_positions = []
        self.dict_objects = {}
        self.list_ends = []
        self.dict_path_type = {}
        self.dict_path_directions = {}
        self.list_route = []
        self.list_route_index = 0

        # ! V02
        self.objs = self.set_grid_v02()
        self.current_position_v02 = (random.choice([obj.position for obj in self.objs]))
        self.next_position_v02 = ()
        self.path_return_v02 = []
        self.wall_break_positions_v02 = []
        self.past_positions_v02 = []
        self.maze_start_position_v02 = (0, 0)
        self.maze_finish_position_v02 = (0, 0)

        # from character!!
        self.set_position_keys = ("K_LEFT", "K_RIGHT", "K_UP", "K_DOWN")
        self.previous_position = ()
        self.selected = False
        self.velocity = GRID_SIZE
        self.climb_positions_visited = []
        self.list_water_list = self.list_water_list

        # lights
        self.brightness_list = []
        self.set_brightness(1)

    # BUILD FUNCTION

    def set_maze(self, past_positions, current_position, grid, path_return, wall_break_positions, next_position):

        past_positions.append(current_position)

        poss_positions = self.poss_postions(current_position, past_positions, grid)

        self.list_next_position = self.next_position(current_position, past_positions, path_return, poss_positions)

        wall_break_positions.append(self.set_current_wall_break_position(self.list_next_position, current_position))

        self.tuple_current_position = self.list_next_position

    # TODO MOVE TO BUILD CLASS?

    def set_camp_positions_list(self, maze_start_position):
        return [(i, maze_start_position[1] - GRID_SIZE) for i in range(0, WIDTH, GRID_SIZE)]

    def set_paths(self, past_positions, wall_break_positions, maze_start_position, maze_finish_position):
        return past_positions + wall_break_positions + [maze_start_position, maze_finish_position]

    def set_paths_v02_obj_navigable(self):
        return [obj.position
                for obj in self.objs
                if obj.navigable != False]

    def tile(self, path, x, y):
        return (path[0] + (x * GRID_SIZE), path[1] + (y * GRID_SIZE))

    # TODO may remove this
    def set_dict_path_adjacent(self):
        return {self.tile(path, x, y): "fish"
                for path, x, y in product(self.paths, AROUND, AROUND)
                if self.tile(path, x, y) not in self.paths}

    def set_tileLocations_camp_positions_v02(self, start_pos):
        return [(x, start_pos[1] - GRID_SIZE)
                for x in range(0, WIDTH, GRID_SIZE)]

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

    def set_tileLocations_earth(self):
        return [(x, y)
                for x in range(0, GRID_SIZE*(WIDTH//GRID_SIZE), GRID_SIZE)
                for y in range(GRID_SIZE*(), GRID_SIZE*(TOP_OFFSET+1), GRID_SIZE)]

    def set_dict_tiles(self):
        # dict
        TILES = [(self.rock, 'R'), (self.path_adjacent, 'A'), (self.sky, 'S'), (self.grass, 'G'), (self.paths, 'P')]

        temp_tiles = {}
        for i in TILES:
            temp_tiles.update(dict.fromkeys(*i))
        return temp_tiles

    def set_tiles_v02_obj_textures(self):
        # dict - change in place
        for obj in self.objs:
            if obj.position in self.rock:
                obj.texture = 'R'
            elif obj.position in self.sky:
                obj.texture = 'S'
            elif obj.position in self.grass:
                obj.texture = 'G'
            elif obj.position in self.rock:
                obj.texture = 'P'

    # TODO MOVE TO BUILD CLASS?

    def set_poss_maze_start(self, past_positions):
        return [p
                for p in past_positions
                if p[1] == GRID_SIZE * TOP_OFFSET
                if p[0] < ((WIDTH - GRID_SIZE * 2) * (1/3))]

    def set_maze_start_position(self, poss_maze_start):

        # return tuple with condition
        if len(poss_maze_start) > 0:
            poss_maze_start = random.choice(poss_maze_start)
            return (poss_maze_start[0], poss_maze_start[1] - GRID_SIZE)

            # self.draw.draw(COLOURS["BLACK_VERY_LIGHT"], self.maze_start_position[0], self.maze_start_position[1])
        # else:
        #     self.maze_start = None

    #! V02
    #! def update_maze_start_position_v02_obj(self, past_positions_v02, top_offset):
    #     poss_maze_start = []
    #     for p in past_positions_v02:
    #         if p[1] == GRID_SIZE * top_offset:
    #             if p[0] < ((WIDTH - GRID_SIZE * 2) * (1/3)):
    #                 poss_maze_start.append(p)

    #     if len(poss_maze_start) > 0:
    #         drawable = True
    #         dimensions = GRID_SIZE
    #         material = COLOURS["RED"]
    #         navigable = True
    #         poss_maze_start = random.choice(poss_maze_start)
    #         self.maze_start_position_v02 = (poss_maze_start[0], poss_maze_start[1] - GRID_SIZE)
    #         self.objs.append(object(drawable, self.maze_start_position_v02, dimensions, material, navigable))
    #         # self.draw.draw(COLOURS["BLACK_VERY_LIGHT"], self.maze_start_position[0], self.maze_start_position[1])
    #     # else:
    #     #     self.maze_start = None

    #! def set_maze_finish_position_v02(self):
    #     drawable = True
    #     dimensions = GRID_SIZE
    #     material = COLOURS["RED"]
    #     navigable = True
    #     poss_maze_finish = []
    #     for p in self.past_positions_v02:
    #         if p[0] == WIDTH - (GRID_SIZE * 2):
    #             if p[1] > ((HEIGHT - GRID_SIZE * 2) * (2/3)):
    #                 poss_maze_finish.append(p)

    #     if len(poss_maze_finish) > 0:
    #         poss_maze_finish = random.choice(poss_maze_finish)
    #         self.maze_finish_position_v02 = (poss_maze_finish[0] + GRID_SIZE, poss_maze_finish[1])
    #         self.objs.append(object(drawable, self.maze_start_position_v02, dimensions, material, navigable))
    #         # self.draw.draw(COLOURS["BLUE_VERY_LIGHT"], self.maze_finish_position[0], self.maze_finish_position[1])
    #     else:
    #         self.maze_finish_v02 = None

    def set_poss_maze_finish(self, past_positions):
        return [p
                for p in past_positions
                if p[0] == WIDTH - (GRID_SIZE * 2)
                if p[1] > ((HEIGHT - GRID_SIZE * 2) * (2/3))]

    # TODO MOVE TO BUILD CLASS?

    def set_maze_finish_position(self, poss_maze_finish):
        if len(poss_maze_finish) > 0:
            poss_maze_finish = random.choice(poss_maze_finish)
            return (poss_maze_finish[0] + GRID_SIZE, poss_maze_finish[1])
            # self.draw.draw(COLOURS["BLUE_VERY_LIGHT"], self.maze_finish_position[0], self.maze_finish_position[1])
        # else:
        #     # self.maze_finish = None

    def set_grid_v01(self):
        grid = [(x, y) for x in range(GRID_SIZE, WIDTH, GRID_SIZE * 2) for y in range(GRID_SIZE * TOP_OFFSET, HEIGHT - (GRID_SIZE * 2), GRID_SIZE * 2) if (x, y)]

        for i in range(len(grid) // 3):
            grid.remove(random.choice(grid))
        return grid

    # TODO MOVE TO BUILD CLASS?

    def set_current_wall_break_position(self, next_position, current_position):
        result = ((next_position[0] - current_position[0]) // 2, (next_position[1] - current_position[1]) // 2)
        return (current_position[0] + result[0], current_position[1] + result[1])
        self.list_wall_break_positions.append(result02)

    def check_maze_finish(self, past_positions, current_position):
        if len(past_positions) > 2 and current_position == past_positions[0]:
            return False
        else:
            return True

    def set_climb(self):
        for p in self.paths:
            check_right = (p[0] + GRID_SIZE, p[1])
            check_left = (p[0] - GRID_SIZE, p[1])
            if check_right not in self.paths and check_left not in self.paths:
                self.list_climb_positions.append(p)

    def setWater(self):
        poss_water_list = []
        not_water_list = []
        for p in self.paths:
            possWater = (p[0], p[1] + GRID_SIZE)
            if possWater not in self.paths:
                poss_water_list.append((p[0], p[1]))
            else:
                not_water_list.append((p[0], p[1]))

        run = True
        while run == True:
            i = 1
            start = len(poss_water_list)
            for p in poss_water_list:
                possWaterRight = (p[0] + GRID_SIZE, p[1])
                possWaterLeft = (p[0] - GRID_SIZE, p[1])
                possWater = [possWaterRight, possWaterLeft]
                check = any(item in possWater for item in not_water_list)
                if check is True:
                    not_water_list.append(p)
                    poss_water_list.remove(p)
            end = len(poss_water_list)
            if start == end:
                run = False
            i += 1

        for p in self.paths:
            if p[1] > ((HEIGHT - GRID_SIZE * 2) * (2/3)):
                poss_water_list.append(p)
                self.list_water_list = poss_water_list

    # TODO MOVE TO BUILD CLASS?? 01

    # def set_current_position(self, next_position):
    #     return next_position

    # TODO MOVE TO BUILD CLASS?? 03

    def poss_position(self, current_position, direction):
        return (current_position[0] + (direction[0] * GRID_SIZE * 2), current_position[1] + (direction[1] * GRID_SIZE * 2))

    def poss_postions(self, current_position, past_positions, grid):
        return [self.poss_position(current_position, d)
                for d in random.sample(DIRECTIONS, len(DIRECTIONS))
                if self.poss_position(current_position, d) in grid
                and self.poss_position(current_position, d) not in past_positions]

    def next_position(self, current_position, past_positions, path_return, poss_position):
        if len(poss_position) > 1:
            return random.choices(poss_position, k=1, weights=[100, 100, 1, 1][:len(poss_position)])[0]
        if len(poss_position) == 0:
            if current_position in past_positions:
                res = self.set_path_return(past_positions, current_position)
                path_return.append(res)
                return res
            else:
                return past_positions[-1]
        if len(poss_position) == 1:
            return poss_position[0]

    def set_path_return(self, past_positions, current_position):
        return past_positions[past_positions.index(current_position) - 1]

    #! V02 *************************************************************************************************************

    #! def set_current_position_v02(self, current_position_v02, next_position_v02):
    #     # if len(current_position_v02) == 0:
    #     #     position = random.choice([obj.position for obj in self.objs])
    #     #     return position
    #     # else:
    #     return next_position_v02

    #! def set_next_position_v02(self, current_position_v02, past_positions_v02, path_return_v02):
    #     random.shuffle(DIRECTIONS)
    #     poss_directions = []
    #     poss_position_List = []
    #     for d in DIRECTIONS:
    #         poss_position = (current_position_v02[0] + (
    #             d[0] * GRID_SIZE * 2), current_position_v02[1] + (d[1] * GRID_SIZE * 2))
    #         if poss_position in [obj.position for obj in self.objs]:
    #             if poss_position not in past_positions_v02:
    #                 poss_position_List.append(poss_position)
    #     if len(poss_position_List) > 1:
    #         bias = [100, 100, 1, 1]
    #         randomResult = random.choices(poss_position_List, k=1, weights=bias[:len(poss_position_List)])
    #         result = randomResult[0]
    #     if len(poss_position_List) == 0:
    #         if current_position_v02 in past_positions_v02:
    #             index = past_positions_v02.index(current_position_v02)
    #             result = past_positions_v02[index - 1]
    #             path_return_v02.append(result)
    #         else:
    #             result = past_positions_v02[-1]
    #     if len(poss_position_List) == 1:
    #         result = poss_position_List[0]
    #     return result

    # TODO MOVE TO BUILD CLASS? 02
    # def set_past_positions(self, temp_past_positions, current_position):
    #     temp_past_positions.append(current_position)
    #     return temp_past_positions

    # def set_past_positions_v02(self, temp_past_positions_v02, current_position_v02):
    #     temp_past_positions_v02.append(current_position_v02)
    #     return temp_past_positions_v02

    # NAV STUFF HERE!

    def set_grid_v02(self):
        drawable = True
        temp_objs = []
        dimensions = (GRID_SIZE, GRID_SIZE, GRID_SIZE)
        material = COLOURS["RED"]
        navigable = True
        for x in range(GRID_SIZE, WIDTH, GRID_SIZE * 2):
            for y in range(GRID_SIZE * TOP_OFFSET, HEIGHT - (GRID_SIZE * 2), GRID_SIZE * 2):
                temp_objs.append(object(drawable, (x, y), dimensions, material, navigable))

        for i in range(len(temp_objs) // 3):
            random_item_from_list = random.choice(temp_objs)
            temp_objs.remove(random_item_from_list)

        return temp_objs

        # for obj in self.objs:
        #     print(obj.drawable, obj.position, obj.dimensions, obj.material, obj.navagatable)

    def update_wall_break_positions_v02_obj(self, next_position_v02, current_position_v02):
        drawable = True
        dimensions = (GRID_SIZE, GRID_SIZE, GRID_SIZE)
        material = COLOURS["RED"]
        navigable = True
        result = ((next_position_v02[0] - current_position_v02[0]) // 2, (next_position_v02[1] - current_position_v02[1]) // 2)
        result02 = (current_position_v02[0] + result[0], current_position_v02[1] + result[1])
        self.objs.append(object(drawable, result02, dimensions, material, navigable))

    #! END *************************************************************************************************************

    def set_navigation(self):
        self.dict_path_type = dict.fromkeys(self.paths, "X")
        self.dict_path_type.update(dict.fromkeys(self.camp_positions, "X"))
        self.dict_path_directions = dict.fromkeys(self.paths, [])
        for p in self.dict_path_type.keys():
            path_directions = []
            for d in DIRECTIONS:
                direction = (p[0] + (d[0] * GRID_SIZE),
                             p[1] + (d[1] * GRID_SIZE))
                if direction in self.dict_path_type:
                    path_directions.append(direction)
            if len(path_directions) == 1:
                self.dict_path_type[p] = 1
                self.dict_path_directions[p] = path_directions
            if len(path_directions) == 2:
                self.dict_path_type[p] = "P"
                self.dict_path_directions[p] = path_directions
            if len(path_directions) > 2:
                self.dict_path_type[p] = "J"
                self.dict_path_directions[p] = path_directions
        for p in [k for k, v in self.dict_path_type.items() if v == 1]:
            if self.dict_path_type[self.dict_path_directions[p][0]] == "P":
                self.dict_path_type[self.dict_path_directions[p][0]] = "N"

        run = True
        while run:
            if any([k for k, v in self.dict_path_type.items() if v == "N"]):
                for k in [k for k, v in self.dict_path_type.items() if v == "N"]:
                    for i in self.dict_path_directions[k]:
                        if isinstance(self.dict_path_type[i], int):
                            result = self.dict_path_type[i]
                        if self.dict_path_type[i] == "P":
                            self.dict_path_type[i] = "N"
                    self.dict_path_type[k] = result + 1
            elif any([k for k, v in self.dict_path_type.items() if v == "G"]):
                for k in [k for k, v in self.dict_path_type.items() if v == "G"]:
                    result = 0
                    result_list02 = []
                    for i in self.dict_path_directions[k]:
                        if isinstance(self.dict_path_type[i], int):
                            result_list02.append(self.dict_path_type[i])
                        if isinstance(self.dict_path_type[i], str):
                            self.dict_path_type[i] = "N"
                    self.dict_path_type[k] = sorted(result_list02)[-1] + 1
            elif any([k for k, v in self.dict_path_type.items() if v == "J"]):
                for k, v in self.dict_path_type.items():
                    if v == "J":
                        result_list = []
                        for i in self.dict_path_directions[k]:
                            if isinstance(self.dict_path_type[i], int):
                                result_list.append(i)
                                if len(result_list) == (len(self.dict_path_directions[k]) - 1):
                                    if self.dict_path_type[k] == "J":
                                        self.dict_path_type[k] = "G"
            else:
                run = False

    def set_route(self, start, end, level):
        route_list_A = []
        route_list_B = []
        route_list_A.append(start)
        if end in level.paths or end in level.camp_positions:
            route_list_B.append(end)
        else:
            route_list_B.append(start)
        run = True
        while run:
            if self.dict_path_type[route_list_A[-1]] <= self.dict_path_type[route_list_B[-1]] or len(route_list_A) == 0:
                result = max(self.dict_path_directions[route_list_A[-1]], key=self.dict_path_type.get)
                route_list_A.append(result)
            if self.dict_path_type[route_list_B[-1]] <= self.dict_path_type[route_list_A[-1]] or len(route_list_B) == 0:
                result = max(self.dict_path_directions[route_list_B[-1]], key=self.dict_path_type.get)
                route_list_B.append(result)
            duplicate = [i for i in route_list_A if i in route_list_B]
            if duplicate:
                route_list_A.pop(-1)
                run = False
        route_list_B.reverse()
        route_list_A.extend(route_list_B)
        self.list_route = route_list_A

    # Charater stuff here:

    # def set_previous_position(self):
    #     positionsList = []
    #     if self.tuple_current_position != positionsList[1]:
    #         positionsList.append(self.tuple_current_position)
    #     if len(positionsList) >= 3:
    #         positionsList.pop(0)

    def set_position(self, event):
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

    def set_climb_positions_visited(self, tuple_current_position, list_climb_positions, climb_positions_visited):
        if tuple_current_position in list_climb_positions:
            climb_positions_visited.append(tuple_current_position)


# class Lights():
    # def __init__(self, level):
        # self.brightness_list = []
        # self.set_brightness(1)
        # self.light_positions = dict.fromkeys(level.paths, (0, 0, 0))
        # self.character_light_positions = dict.fromkeys(level.paths, (0, 0, 0))
        # self.sun_light_positions = dict.fromkeys(level.paths, (0, 0, 0))


    def set_brightness(self, x):
        self.brightness_list = []
        if (x < 256):
            res = self.set_brightness((x*2))
            res = int(res)
            if res >= 255:
                res += -1
            self.brightness_list.append(tuple([res] * 3))
        return x

    def set_lights_debug(self, lights_state, brightness_list):
        if lights_state == True:
            brightness = brightness_list[1]

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

    def set_lights_sun(self, tuple_maze_start_position, paths, sun_light_positions, brightness_list, tuple_maze_finish_position):
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
        get_key, get_val = itemgetter(0), itemgetter(1)
        merged_data = sorted(chain(light_positions.items(), sun_light_positions.items(), character_light_positions.items()), key=get_key)
        return {k: max(map(get_val, g))for k, g in groupby(merged_data, key=get_key)}

    def return_array(self, image):
        array = numpy.array(image)
        array = array.astype(float)
        return array

    def return_darken(self, image_float01, image_float02):
        opacity = 1.0
        # blended_img_float = darken_only(image_float01, image_float02, opacity)
        blended_img_float = lighten_only(image_float01, image_float02, opacity)
        blended_img = numpy.uint8(blended_img_float)
        blended_img_raw = Image.fromarray(blended_img)
        return blended_img_raw

    def return_lighting_tile(self, TOP_image, TOPR_image, neighbor):
        if neighbor == "T":
            res = TOP_image.rotate(0)
        if neighbor == "TR":
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
        foreground_image = neighbors01
        background_image = neighbors02
        forground_array = self.return_array(foreground_image)
        background_array = self.return_array(background_image)
        res = self.return_darken(forground_array, background_array)
        return res

# GAME RUN 01
    def set_tileImages(self):
        self.tileImages = {}
        image_types = ["T", "R", "B", "L", "TR", "BR", "BL", "TL"]
        for i in image_types:
            self.tileImages[i + "_image"] = self.return_lighting_tile(T_image, TR_image, i)


# GAME RUN 02


    def set_route_light_positions(self, path_adjacent, light_positions):
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

# GAME RUN 03
    def set_route_light_positions_tiles(self, debug):
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
