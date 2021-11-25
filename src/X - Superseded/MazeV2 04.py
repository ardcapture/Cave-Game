import pygame
import random

from pygame.constants import GL_RED_SIZE

# CONSTANTS
DOWN = (0, -1)
RIGHT = (1, 0)
LEFT = (-1, 0)
UP = (0, 1)
DIRECTIONS = [DOWN, LEFT, RIGHT, UP]

BLACK = (0, 0, 0)
BlACK_VERY_LIGHT = (210, 210, 210)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
RED_VERY_LIGHT = (255, 210, 210)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLUE_LIGHT = (125, 125, 255)
BLUE_VERY_LIGHT = (210, 210, 255)


WIDTH = 1020
HEIGHT = 1020


# myfont = pygame.font.SysFont("monospace",16)

# WINDOW
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
# win = pygame.display.set_mode((display_width, display_height), pygame.FULLSCREEN)
pygame.display.set_caption("First Game")


class Level():
    def __init__(self, world):
        self.world = world
        self.ends_list = []

        self.path_type = {}
        self.path_directions = {}

    def set_ends(self):

        paths = self.world.paths

        self.path_type = dict.fromkeys(self.world.paths, "X")
        self.path_directions = dict.fromkeys(self.world.paths, [])

        # set parts!
        for p in self.path_type.keys():
            path_directions = []
            for d in DIRECTIONS:
                direction = (p[0] + (d[0] * self.world.grid_size), p[1] + (d[1] * self.world.grid_size))
                if direction in self.path_type:
                    path_directions.append(direction)
            if len(path_directions) == 1:
                self.path_type[p] = 1
                self.path_directions[p] = path_directions
            if len(path_directions) == 2:
                self.path_type[p] = "P"
                self.path_directions[p] = path_directions
            if len(path_directions) > 2:
                self.path_type[p] = "J"
                self.path_directions[p] = path_directions


        for p in [k for k,v in self.path_type.items() if v == 1]:
            if self.path_type[self.path_directions[p][0]] == "P":
                self.path_type[self.path_directions[p][0]] = "N"


        run = True
        while run:
            if any([k for k,v in self.path_type.items() if v == "N"]):
                for k,v in self.path_type.items():
                        if v == "N":
                            for i in self.path_directions[k]:
                                if isinstance(self.path_type[i], int):
                                    result = self.path_type[i]
                                if self.path_type[i] == "P":
                                    self.path_type[i] = "N"
                            self.path_type[k] = result + 1

            elif any([k for k,v in self.path_type.items() if v == "G"]):
                for k in [k for k,v in self.path_type.items() if v == "G"]:
                    result = 0
                    for i in self.path_directions[k]:
                        if isinstance(self.path_type[i], int):
                            result += self.path_type[i]
                            print("k", k, self.path_type[k], "=", self.path_type[i])
                        if isinstance(self.path_type[i], str):
                            self.path_type[i] = "N"
                    print("result", result)
                    self.path_type[k] = result + 1

            elif any([k for k,v in self.path_type.items() if v == "J"]):
                for k,v in self.path_type.items():
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


    def draw_ends(self):
        for k,v in dict.items(self.path_type):
            text = myfont.render("{0}".format(v), 1, (0, 0, 0))
            win.blit(text, (k[0] + 1, k[1] + 5))



class Player():
    def __init__(self, world):
        self.current_poistion = random.choice(world.camp_positions)
        self.grid_size = world.grid_size
        self.paths = world.paths
        self.camp_positions = world.camp_positions
        self.velocity = 20
        self.climb_positions = world.climb_positions
        self.climb_positions_visited = []
        self.water_list = world.water_list
        self.dark_positions = dict.fromkeys(self.paths, False)

    def set_current_position(self):
        x, y = self.current_poistion
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            x -= self.velocity
        if keys[pygame.K_RIGHT]:
            x += self.velocity
        if keys[pygame.K_UP]:
            y -= self.velocity
        if keys[pygame.K_DOWN]:
            y += self.velocity

        if (x, y) in self.paths or (x, y) in self.camp_positions:
            self.current_poistion = (x, y)

    def set_climb_positions_visited(self):
        if self.current_poistion in self.climb_positions:
            self.climb_positions_visited.append(self.current_poistion)

    def set_dark_positions(self):
        self.dark_positions[self.current_poistion] = False

        lightList = []
        for x in range(self.current_poistion[0] - self.grid_size, self.current_poistion[0] + self.grid_size * 2, self.grid_size):
            for y in range(self.current_poistion[1] - self.grid_size, self.current_poistion[1] + self.grid_size * 2, self.grid_size):
                lightList.append((x, y))
        for i in lightList:
            self.dark_positions[i] = False

        posslightposition = world.maze_start_position
        run = True
        while run:
            if posslightposition in self.paths:
                self.dark_positions[posslightposition] = False
                posslightposition = (
                    posslightposition[0], posslightposition[1] + self.grid_size)
            else:
                run = False

    def draw_light_positions(self):
        listOfKeys = list()
        listOfItems = self.dark_positions.items()
        for item in listOfItems:
            if item[1] == True:
                listOfKeys.append(item[0])
        for p in listOfKeys:
            self.draw(BLACK, p[0], p[1])

    def draw_climb_positions_visited(self):
        for p in self.climb_positions_visited:
            if p not in self.water_list:
                pygame.draw.rect(
                    win, RED, (p[0] + self.grid_size * 7/16, p[1], self.grid_size/8, self.grid_size))

    def draw_player(self):
        self.draw(RED, self.current_poistion[0], self.current_poistion[1])

    # DRAW METHOD

    def draw(self, color, x, y):
        pygame.draw.rect(
            win, color, (x, y, self.grid_size, self.grid_size))

    def draw_transparent(self, color, x, y):
        surface = pygame.Surface((self.grid_size, self.grid_size))
        surface.set_alpha(50)
        pygame.draw.rect(surface, color, surface.get_rect())
        win.blit(surface, (x, y))

    def draw_reset(self):
        win.fill(BLACK)


class World():
    def __init__(self, width, height, grid_size,):
        self.width = width
        self.height = height
        self.grid_size = grid_size
        self.top_ofset = 4

        self.path_return = []
        self.grid = []
        self.paths = []
        self.wall_break_positions = []
        self.past_positions = []
        self.next_position = ()
        self.current_poistion = ()
        self.maze_start_position = (0, 0)
        self.maze_finish_position = (0, 0)
        self.water_list = []
        self.camp_positions = []
        self.climb_positions = []

    def MazeBuild(self):
        self.set_grid()
        mazebuild = True
        while mazebuild == True:
            # pygame.time.delay(10)
            self.draw_grid()
            self.set_current_position()
            self.set_past_positions()
            self.set_next_position()
            self.set_wall_break_positions()
            if len(self.past_positions) > 2 and self.current_poistion == self.past_positions[0]:
                self.set_maze_start_position()
                self.set_maze_finish_position()
                self.set_camp_positions()
                self.set_paths()
                self.setWater()
                self.set_climb()
                self.draw_grid_hide()
                self.set_world_top()
                mazebuild = False

            pygame.display.update()
        pygame.display.update()

    def world_run_before(self):
        self.draw_paths()
        # self.draw_climb_positions()
        self.draw_world_top_surface()

    def world_run_after(self):
        self.draw_water()
        self.draw_startPosition()

    def set_camp_positions(self):
        for i in range(0, WIDTH, 20):
            self.camp_positions.append(
                (i, self.maze_start_position[1] - self.grid_size))

    def set_world_top(self):
        self.world_top_surface = pygame.Surface(
            (self.width, self.grid_size * 3))

    def draw_world_top_surface(self):
        pygame.draw.rect(self.world_top_surface, WHITE,
                         self.world_top_surface.get_rect())
        win.blit(self.world_top_surface, (0, 0))

    def set_paths(self):
        mylist = self.past_positions + self.wall_break_positions
        mylist.append(self.maze_start_position)
        mylist.append(self.maze_finish_position)
        self.paths = list(dict.fromkeys(mylist))

    def draw_paths(self):
        for p in self.paths:
            # print("p[0]", p[0], "p[1]", p[1])
            self.draw(BlACK_VERY_LIGHT, p[0], p[1])

    def set_maze_start_position(self):
        poss_maze_start = []
        for p in self.past_positions:
            if p[1] == self.grid_size * self.top_ofset:
                if p[0] < ((WIDTH - self.grid_size * 2) * (1/3)):
                    poss_maze_start.append(p)

        if len(poss_maze_start) > 0:
            poss_maze_start = random.choice(poss_maze_start)
            self.maze_start_position = (
                poss_maze_start[0], poss_maze_start[1] - self.grid_size)
            self.draw(
                BlACK_VERY_LIGHT, self.maze_start_position[0], self.maze_start_position[1])
        else:
            self.maze_start = None

    def set_maze_finish_position(self):
        poss_maze_finish = []
        for p in self.past_positions:
            if p[0] == WIDTH - (self.grid_size * 2):
                if p[1] > ((HEIGHT - self.grid_size * 2) * (2/3)):
                    poss_maze_finish.append(p)

        if len(poss_maze_finish) > 0:
            poss_maze_finish = random.choice(poss_maze_finish)
            self.maze_finish_position = (
                poss_maze_finish[0] + self.grid_size, poss_maze_finish[1])
            self.draw(
                BLUE_VERY_LIGHT, self.maze_finish_position[0], self.maze_finish_position[1])
        else:
            self.maze_finish = None

    def set_grid(self):
        self.grid = [(x, y) for x in range(self.grid_size, self.width, self.grid_size * 2)
                     for y in range(self.grid_size * self.top_ofset, self.height - (self.grid_size * 2), self.grid_size * 2) if (x, y)]

        for i in range(len(self.grid) // 3):
            random_item_from_list = random.choice(self.grid)
            self.grid.remove(random_item_from_list)

    def draw_grid(self):
        for i in self.grid:
            self.draw(BlACK_VERY_LIGHT, i[0], i[1])

    def draw_grid_hide(self):
        directions_list = []
        for g in self.grid:
            for d in DIRECTIONS:
                if (g[0] + (d[0] * self.grid_size), g[1] + (d[1] * self.grid_size)) not in self.wall_break_positions:
                    directions_list.append((d[0], d[1]))
            if len(directions_list) == 4:
                self.draw(BLACK, g[0], g[1])
            directions_list.clear()

    def set_current_position_paths(self):
        for p in self.paths:
            pygame.time.delay(1000)

            # DRAW
            self.draw(GREEN, p[0], p[1])

    def set_wall_break_positions(self):
        result = ((self.next_position[0] - self.current_poistion[0]) //
                  2, (self.next_position[1] - self.current_poistion[1]) // 2)
        result02 = (
            self.current_poistion[0] + result[0], self.current_poistion[1] + result[1])
        self.wall_break_positions.append(result02)

        # DRAW
        self.draw(BlACK_VERY_LIGHT, result02[0], result02[1])

    def set_climb(self):
        for p in self.paths:
            check_right = (p[0] + self.grid_size, p[1])
            check_left = (p[0] - self.grid_size, p[1])
            if check_right not in self.paths and check_left not in self.paths:
                self.climb_positions.append(p)

    def draw_climb_positions(self):
        for p in self.climb_positions:
            pygame.draw.rect(
                win, GREEN, (p[0] + self.grid_size * 7/16, p[1], self.grid_size/8, self.grid_size))

    def setWater(self):
        poss_water_list = []
        not_water_list = []
        is_water_list = []
        for p in self.paths:
            possWater = (p[0], p[1] + self.grid_size)
            if possWater not in self.paths:
                poss_water_list.append((p[0], p[1]))
            else:
                not_water_list.append((p[0], p[1]))

        run = True
        while run == True:
            i = 1
            start = len(poss_water_list)
            for p in poss_water_list:
                possWaterRight = (p[0] + self.grid_size, p[1])
                possWaterLeft = (p[0] - self.grid_size, p[1])
                possWater = [possWaterRight, possWaterLeft]
                check = any(item in possWater for item in not_water_list)
                if check is True:
                    # if possWaterRight in not_water_list or possWaterLeft in not_water_list:
                    not_water_list.append(p)
                    poss_water_list.remove(p)
            end = len(poss_water_list)
            if start == end:
                run = False
            i += 1

        for p in self.paths:
            if p[1] > ((HEIGHT - self.grid_size * 2) * (2/3)):
                poss_water_list.append(p)
                self.water_list = poss_water_list

    def draw_startPosition(self):
        p = self.past_positions[0]
        self.draw_outline(RED, p[0], p[1])

    def draw_water(self):
        for p in self.water_list:
            self.draw_transparent(BLUE_LIGHT, p[0], p[1])

    def set_current_position(self):
        if len(self.current_poistion) == 0:
            position = random.choice(self.grid)
            self.current_poistion = position
        else:
            self.current_poistion = self.next_position

            # self.draw(
            #     RED, self.current_poistion[0], self.current_poistion[1])

    def set_next_position(self):
        random.shuffle(DIRECTIONS)
        poss_directions = []
        poss_position_List = []
        for d in DIRECTIONS:
            poss_position = (self.current_poistion[0] + (
                d[0] * self.grid_size * 2), self.current_poistion[1] + (d[1] * self.grid_size * 2))
            if poss_position in self.grid:
                if poss_position not in self.past_positions:
                    poss_position_List.append(poss_position)

        if len(poss_position_List) > 1:
            bias = [100, 100, 1, 1]
            randomResult = random.choices(
                poss_position_List, k=1, weights=bias[:len(poss_position_List)])
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

    def set_past_positions(self):
        self.past_positions.append(self.current_poistion)

    # DRAW METHOD
    def draw(self, color, x, y):
        pygame.draw.rect(
            win, color, (x, y, self.grid_size, self.grid_size))

    def draw_outline(self, color, x, y):
        pygame.draw.rect(
            win, color, (x, y, self.grid_size, self.grid_size), 2)

    def draw_transparent(self, color, x, y):
        surface = pygame.Surface((self.grid_size, self.grid_size))
        surface.set_alpha(75)
        pygame.draw.rect(surface, color, surface.get_rect())
        win.blit(surface, (x, y))

    def draw_reset(self):
        win.fill(BLACK)


# BUILD
build = True
while build:
    world = World(width=WIDTH, height=HEIGHT, grid_size=20)
    world.MazeBuild()
    if world.maze_finish_position == (0, 0) or world.maze_start_position == (0, 0):
        world.draw_reset()
        del world
    else:
        build = False


player = Player(world)
level = Level(world)

myfont = pygame.font.SysFont("monospace", 10)
level.set_ends()


# RUN
run = True
while run:
    # clock.tick(10)
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    world.world_run_before()
    player.set_current_position()
    player.set_climb_positions_visited()
    player.draw_player()
    # player.draw_climb_positions_visited()
    world.world_run_after()
    player.set_dark_positions()
    player.draw_light_positions()
    level.draw_ends()

    # win.blit(text, (1,45))

    pygame.display.update()

pygame.quit()
