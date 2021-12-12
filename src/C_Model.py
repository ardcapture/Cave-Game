import random
import pygame
import os
import numpy

from PIL import Image, ImageFont, ImageDraw, ImageOps
from operator import itemgetter
from itertools import chain, groupby
from collections import defaultdict
from blend_modes import darken_only, lighten_only


imagesPath = 'res'


DIRECTIONS = [(0, 1), (-1, 0), (1, 0), (0, -1)]

GRID_SIZE = 32
WIDTH, HEIGHT = (GRID_SIZE*2) + (GRID_SIZE *
                                 35), (GRID_SIZE*2) + (GRID_SIZE * 22)


win = pygame.Surface((WIDTH, HEIGHT))


COLOURS = {"BLACK": (0, 0, 0),
           "WHITE": (255, 255, 255),
           "BLACK_VERY_LIGHT": (210, 210, 210),
           "WHITE_4TH_4TH_4TH_4TH": (1, 1, 1),
           "RED": (255, 0, 0),
           "GREEN": (0, 255, 0),
           "BLUE_LIGHT": (125, 125, 255),
           "BLUE_VERY_LIGHT": (210, 210, 255)}


rock_lighting_tile = Image.open(os.path.join(imagesPath, 'rock.png')).resize((GRID_SIZE, GRID_SIZE))
BlackSQ = Image.open(os.path.join(imagesPath, 'BlackSQ.png')).resize((GRID_SIZE, GRID_SIZE))


TILE_DIRECTIONS = {"T": (0, -1), "R": (1, 0), "B": (0, 1), "L": (-1, 0),
                   "TR": (1, -1), "BR": (1, 1), "BL": (-1, 1), "TL": (-1, -1)}

T_image = Image.open(os.path.join(imagesPath, 'I_Image_01.png')).resize((GRID_SIZE, GRID_SIZE))
TR_image = Image.open(os.path.join(imagesPath, 'Corner.png')).resize((GRID_SIZE, GRID_SIZE))


class Level():
    def __init__(self):
        # self.draw = draw
        self.top_ofset = 5
        self.path_return = []
        self.wall_break_positions = []
        self.past_positions = []
        self.next_position = ()
        self.current_poistion = ()
        self.maze_start_position = (0, 0)
        self.maze_finish_position = (0, 0)
        self.water_list = []
        self.camp_positions = []
        self.climb_positions = []

    # TODO MOVE TO BUILD CLASS?
    def set_camp_positions(self):
        for i in range(0, WIDTH, GRID_SIZE):
            self.camp_positions.append(
                (i, self.maze_start_position[1] - GRID_SIZE))

    def set_paths(self):
        mylist = self.past_positions + self.wall_break_positions
        mylist.append(self.maze_start_position)
        mylist.append(self.maze_finish_position)
        self.paths = list(dict.fromkeys(mylist))

    def set_path_adjacent(self):
        self.path_adjacent = {}
        AROUND = [-1, 0, 1]
        for i in self.paths:
            for j in AROUND:
                for k in AROUND:
                    tile = (i[0] + (j * GRID_SIZE), i[1] + (k * GRID_SIZE))
                    if tile not in self.paths:
                        self.path_adjacent[tile] = "fish"

    def set_tileLocations(self):
        self.sky = [(x, y) for x in range(0, GRID_SIZE*(WIDTH//GRID_SIZE), GRID_SIZE)
                    for y in range(0, GRID_SIZE*(self.top_ofset-1), GRID_SIZE)]

        self.rock = [(x, y) for x in range(0, GRID_SIZE*(WIDTH//GRID_SIZE), GRID_SIZE)
                     for y in range(0, GRID_SIZE*(HEIGHT//GRID_SIZE), GRID_SIZE)]

        self.grass = [(x, y) for x in range(0, GRID_SIZE*(WIDTH//GRID_SIZE), GRID_SIZE)
                      for y in range(GRID_SIZE*(self.top_ofset-1), GRID_SIZE*(self.top_ofset), GRID_SIZE)]

        self.earth = [(x, y) for x in range(0, GRID_SIZE*(WIDTH//GRID_SIZE), GRID_SIZE)
                      for y in range(GRID_SIZE*(self.top_ofset), GRID_SIZE*(self.top_ofset+1), GRID_SIZE)]

    def set_tiles(self):
        self.tiles = dict.fromkeys(self.rock, 'R')
        self.tiles.update(dict.fromkeys(self.path_adjacent, 'A'))
        self.tiles.update(dict.fromkeys(self.sky, 'S'))
        self.tiles.update(dict.fromkeys(self.grass, 'G'))
        self.tiles.update(dict.fromkeys(self.paths, 'P'))

    # TODO MOVE TO BUILD CLASS?
    def set_maze_start_position(self):
        poss_maze_start = []
        for p in self.past_positions:
            if p[1] == GRID_SIZE * self.top_ofset:
                if p[0] < ((WIDTH - GRID_SIZE * 2) * (1/3)):
                    poss_maze_start.append(p)

        if len(poss_maze_start) > 0:
            poss_maze_start = random.choice(poss_maze_start)
            self.maze_start_position = (poss_maze_start[0], poss_maze_start[1] - GRID_SIZE)
            # self.draw.draw(COLOURS["BLACK_VERY_LIGHT"], self.maze_start_position[0], self.maze_start_position[1])
        else:
            self.maze_start = None

    # TODO MOVE TO BUILD CLASS?
    def set_maze_finish_position(self):
        poss_maze_finish = []
        for p in self.past_positions:
            if p[0] == WIDTH - (GRID_SIZE * 2):
                if p[1] > ((HEIGHT - GRID_SIZE * 2) * (2/3)):
                    poss_maze_finish.append(p)

        if len(poss_maze_finish) > 0:
            poss_maze_finish = random.choice(poss_maze_finish)
            self.maze_finish_position = (poss_maze_finish[0] + GRID_SIZE, poss_maze_finish[1])
            # self.draw.draw(COLOURS["BLUE_VERY_LIGHT"], self.maze_finish_position[0], self.maze_finish_position[1])
        else:
            self.maze_finish = None

    def set_grid(self):
        self.grid = [(x, y) for x in range(GRID_SIZE, WIDTH, GRID_SIZE * 2)
                     for y in range(GRID_SIZE * self.top_ofset, HEIGHT - (GRID_SIZE * 2), GRID_SIZE * 2) if (x, y)]

        for i in range(len(self.grid) // 3):
            random_item_from_list = random.choice(self.grid)
            self.grid.remove(random_item_from_list)

    # TODO MOVE TO BUILD CLASS?
    def set_wall_break_positions(self):
        result = ((self.next_position[0] - self.current_poistion[0]) //
                  2, (self.next_position[1] - self.current_poistion[1]) // 2)
        result02 = (self.current_poistion[0] + result[0], self.current_poistion[1] + result[1])
        self.wall_break_positions.append(result02)

    def set_climb(self):
        for p in self.paths:
            check_right = (p[0] + GRID_SIZE, p[1])
            check_left = (p[0] - GRID_SIZE, p[1])
            if check_right not in self.paths and check_left not in self.paths:
                self.climb_positions.append(p)

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
                self.water_list = poss_water_list

    # TODO MOVE TO BUILD CLASS?? 01

    def set_current_position(self):
        if len(self.current_poistion) == 0:
            position = random.choice(self.grid)
            self.current_poistion = position
        else:
            self.current_poistion = self.next_position

    # TODO MOVE TO BUILD CLASS?? 03
    def set_next_position(self):
        random.shuffle(DIRECTIONS)
        poss_directions = []
        poss_position_List = []
        for d in DIRECTIONS:
            poss_position = (self.current_poistion[0] + (
                d[0] * GRID_SIZE * 2), self.current_poistion[1] + (d[1] * GRID_SIZE * 2))
            if poss_position in self.grid:
                if poss_position not in self.past_positions:
                    poss_position_List.append(poss_position)

        if len(poss_position_List) > 1:
            bias = [100, 100, 1, 1]
            randomResult = random.choices(poss_position_List, k=1, weights=bias[:len(poss_position_List)])
            result = randomResult[0]
        if len(poss_position_List) == 0:
            if self.current_poistion in self.past_positions:
                index = self.past_positions.index(self.current_poistion)
                result = self.past_positions[index - 1]
                self.path_return.append(result)
            else:
                result = self.past_positions[-1]
        if len(poss_position_List) == 1:
            result = poss_position_List[0]
        self.next_position = result

    # TODO MOVBE TO BUID CLASS? 02
    def set_past_positions(self):
        self.past_positions.append(self.current_poistion)


class Character():
    def __init__(self, level):
        self.level = level
        self.set_position_keys = ("K_LEFT", "K_RIGHT", "K_UP", "K_DOWN")
        self.previous_position = ()
        self.selected = False
        self.current_poistion = random.choice(self.level.camp_positions)
        self.paths = self.level.paths
        self.camp_positions = self.level.camp_positions
        self.velocity = GRID_SIZE
        self.climb_positions = self.level.climb_positions
        self.climb_positions_visited = []
        self.water_list = self.level.water_list

    def events(self):
        print("Character event")

    def set_previous_position(self):
        positionsList = []
        if self.current_poistion != positionsList[1]:
            positionsList.append(self.current_poistion)
        if len(positionsList) >= 3:
            positionsList.pop(0)

    def set_position(self, event):
        x, y = self.current_poistion
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
            self.current_poistion = (x, y)
            pygame.time.delay(150)

    def set_climb_positions_visited(self):
        if self.current_poistion in self.climb_positions:
            self.climb_positions_visited.append(self.current_poistion)

    def set_selected(self):
        pass


class Lights():
    def __init__(self, level, character):
        self.level = level
        self.character = character
        self.brightness_list = []
        self.set_brightness(1)
        self.light_positions = dict.fromkeys(self.level.paths, (0, 0, 0))
        self.character_light_positions = dict.fromkeys(self.level.paths, (0, 0, 0))
        self.sun_light_positions = dict.fromkeys(self.level.paths, (0, 0, 0))

    def set_brightness(self, x):
        self.brightness_list = []
        if (x < 256):
            res = self.set_brightness((x*2))
            res = int(res)
            if res >= 255:
                res += -1
            self.brightness_list.append(tuple([res] * 3))
        return x

    def set_lights(self, lights_state):
        self.set_lights_debug(lights_state)
        self.set_lights_sun()
        self.set_lights_character()
        self.set_light_positions()

    def set_lights_debug(self, lights_state):
        if lights_state == True:
            brightness = self.brightness_list[1]

    def set_lights_character(self):
        mylist = [GRID_SIZE, -GRID_SIZE]
        for i in mylist:
            posslightposition = self.character.current_poistion
            brightness = 0
            run = True
            while run:
                if posslightposition in self.level.paths:
                    self.character_light_positions[posslightposition] = self.brightness_list[brightness]
                    posslightposition = (
                        posslightposition[0] + i, posslightposition[1])
                    if brightness < len(self.brightness_list) - 1:
                        brightness += 1
                else:
                    run = False
        for i in mylist:
            posslightposition = self.character.current_poistion
            brightness = 0
            run = True
            while run:
                if posslightposition in self.level.paths:
                    self.character_light_positions[posslightposition] = self.brightness_list[brightness]
                    posslightposition = (
                        posslightposition[0], posslightposition[1] + i)
                    if brightness < len(self.brightness_list) - 1:
                        brightness += 1
                else:
                    run = False

        self.character_light_positions[self.character.current_poistion] = (0, 0, 0)

    def set_lights_sun(self):
        posslightposition = self.level.maze_start_position
        brightness = 1
        run = True
        while run:
            if posslightposition in self.level.paths:
                self.sun_light_positions[posslightposition] = self.brightness_list[brightness]
                posslightposition = (
                    posslightposition[0], posslightposition[1] + GRID_SIZE)
                if brightness < len(self.brightness_list) - 1:
                    brightness += 1
            else:
                run = False
        posslightposition = self.level.maze_finish_position
        brightness = 1
        run = True
        while run:
            if posslightposition in self.level.paths:
                self.sun_light_positions[posslightposition] = self.brightness_list[brightness]
                posslightposition = (posslightposition[0] - GRID_SIZE, posslightposition[1])
                if brightness < len(self.brightness_list) - 1:
                    brightness += 1
            else:
                run = False

    def set_light_positions(self):
        get_key, get_val = itemgetter(0), itemgetter(1)
        merged_data = sorted(chain(self.light_positions.items(), self.sun_light_positions.items(), self.character_light_positions.items()), key=get_key)

        self.light_positions = {k: max(map(get_val, g))
                                for k, g in groupby(merged_data, key=get_key)}

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

    def return_lighting_tile(self, TOP_image, TOPR_image, neighbour):
        if neighbour == "T":
            res = TOP_image.rotate(0)
        if neighbour == "TR":
            res = TOPR_image.rotate(0)
        elif neighbour == "L":
            res = TOP_image.rotate(90)
        elif neighbour == "TL":
            res = TOPR_image.rotate(90)
        elif neighbour == "B":
            res = TOP_image.rotate(180)
        elif neighbour == "BL":
            res = TOPR_image.rotate(180)
        elif neighbour == "R":
            res = TOP_image.rotate(270)
        elif neighbour == "BR":
            res = TOPR_image.rotate(270)
        return res

    def return_blended(self, neighbours01, neighbours02):
        forgound_image = neighbours01
        background_image = neighbours02
        forground_array = self.return_array(forgound_image)
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


    def set_route_light_positions(self, path_adjacent):
        d = defaultdict(list)
        for i in path_adjacent:
            AROUND = [-1, 0, 1]
            for j in AROUND:
                for k in AROUND:
                    tile = (i[0] + (j * GRID_SIZE), i[1] + (k * GRID_SIZE))
                    if tile in self.light_positions:
                        res = (list(TILE_DIRECTIONS.keys())[list(TILE_DIRECTIONS.values()).index((j, k))])
                        d[i].append((res))
        self.route_light_positions = d
        for k, v in self.route_light_positions.items():
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

# GAME RUN 03
    def set_route_light_positions_tiles(self, dict, debug):
        self.route_light_positions_tiles = {}
        for k, v in dict.items():
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
