import pygame
import random

from pygame.constants import MOUSEBUTTONUP

# clock = pygame.time.Clock()

# CONSTANTS
DOWN = (0, -1)
RIGHT = (1, 0)
LEFT = (-1, 0)
UP = (0, 1)
DIRECTIONS = [DOWN, LEFT, RIGHT, UP]

BLACK = (0, 0, 0)
BLACK_VERY_LIGHT = (210, 210, 210)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
RED_VERY_LIGHT = (255, 210, 210)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLUE_LIGHT = (125, 125, 255)
BLUE_VERY_LIGHT = (210, 210, 255)


WIDTH = 1020
HEIGHT = 800

# WINDOW
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game")





class Player_Controller():
    def __init__(self, player):
        self.player = player

        self.run = True
        self.select_location = (0, 0)

    # def set_current_position(self):
    #     x, y = self.player.current_poistion

    #     keys = pygame.key.get_pressed()
    #     if keys[pygame.K_LEFT]:
    #         x -= self.player.velocity
    #     if keys[pygame.K_RIGHT]:
    #         x += self.player.velocity
    #     if keys[pygame.K_UP]:
    #         y -= self.player.velocity
    #     if keys[pygame.K_DOWN]:
    #         y += self.player.velocity

    #     if (x, y) in self.player.paths or (x, y) in self.player.camp_positions:
    #         self.player.current_poistion = (x, y)

        pygame.time.delay(100)

    def set_mouse_position(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                self.select_location = pos
                print(pos)

            if event.type == pygame.QUIT:
                self.run = False


class AI_Controller():
    def __init__(self, draw, level, player):
        self.draw = draw
        self.level = level
        self.player = player

        self.ends_list = []
        self.path_type = {}
        self.path_directions = {}
        self.route_list = []

    def set_navigation(self):
        self.path_type = dict.fromkeys(self.level.paths, "X")
        self.path_type.update(dict.fromkeys(self.level.camp_positions, "X"))
        self.path_directions = dict.fromkeys(self.level.paths, [])

        for p in self.path_type.keys():
            path_directions = []
            for d in DIRECTIONS:
                direction = (p[0] + (d[0] * draw.grid_size),
                             p[1] + (d[1] * draw.grid_size))
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

    def set_route(self):
        route_list_A = []
        route_list_B = []
        route_list_A.append(self.player.current_poistion)
        route_list_B.append(self.level.maze_finish_position)

        run = True
        while run:
            if self.path_type[route_list_A[-1]] <= self.path_type[route_list_B[-1]] or len(route_list_A) == 0:
                result = max(
                    self.path_directions[route_list_A[-1]], key=self.path_type.get)
                route_list_A.append(result)

            if self.path_type[route_list_B[-1]] <= self.path_type[route_list_A[-1]] or len(route_list_B) == 0:
                result = max(
                    self.path_directions[route_list_B[-1]], key=self.path_type.get)
                route_list_B.append(result)

            duplicte = [i for i in route_list_A if i in route_list_B]
            if duplicte:
                route_list_A.pop(-1)
                run = False

        route_list_B.reverse()
        route_list_A.extend(route_list_B)
        self.route_list = route_list_A

    # DRAW

    def draw_route(self):
        for p in self.route_list:
            self.draw.draw_outline(GREEN, p[0], p[1])

    def draw_ends(self):
        for k, v in dict.items(self.path_type):
            text = myfont.render("{0}".format(v), 1, (0, 0, 0))
            win.blit(text, (k[0] + 1, k[1] + 5))


class Player():
    def __init__(self, level, draw):
        self.level = level
        self.draw = draw

        self.selected = False
        self.current_poistion = random.choice(self.level.camp_positions)
        self.grid_size = self.level.grid_size
        self.paths = self.level.paths
        self.camp_positions = self.level.camp_positions
        self.velocity = 20
        self.climb_positions = self.level.climb_positions
        self.climb_positions_visited = []
        self.water_list = self.level.water_list
        self.dark_positions = dict.fromkeys(self.paths, False)

    # SET

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

        posslightposition = self.level.maze_start_position
        run = True
        while run:
            if posslightposition in self.paths:
                self.dark_positions[posslightposition] = False
                posslightposition = (
                    posslightposition[0], posslightposition[1] + self.grid_size)
            else:
                run = False

    def set_selected(self):
        pass
        # x, y = self.player_controller.select_location

    # DRAW
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
        self.draw.draw(RED, self.current_poistion[0], self.current_poistion[1])
        # self.draw.draw(GREEN, self.current_poistion[0], self.current_poistion[1])
        if self.selected:
            self.draw.draw_circle(WHITE, self.current_poistion[0] + (self.level.grid_size/2), self.current_poistion[1] + (self.level.grid_size/2))


class Level():
    def __init__(self, width, height, grid_size, draw):
        self.draw = draw

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
            self.draw.draw(BLACK_VERY_LIGHT, p[0], p[1])

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
            self.draw.draw(
                BLACK_VERY_LIGHT, self.maze_start_position[0], self.maze_start_position[1])
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
            self.draw.draw(
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
            self.draw.draw(BLACK_VERY_LIGHT, i[0], i[1])

    def draw_grid_hide(self):
        directions_list = []
        for g in self.grid:
            for d in DIRECTIONS:
                if (g[0] + (d[0] * self.grid_size), g[1] + (d[1] * self.grid_size)) not in self.wall_break_positions:
                    directions_list.append((d[0], d[1]))
            if len(directions_list) == 4:
                self.draw.draw(BLACK, g[0], g[1])
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
        self.draw.draw(BLACK_VERY_LIGHT, result02[0], result02[1])

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
        self.draw.draw_outline(RED, p[0], p[1])

    def draw_water(self):
        for p in self.water_list:
            self.draw.draw_transparent(BLUE_LIGHT, p[0], p[1])

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


class Draw():
    def __init__(self):
        self.grid_size = 20

    def draw_outline(self, color, x, y):
        pygame.draw.rect(
            win, color, (x, y, self.grid_size, self.grid_size), 2)

    def draw(self, color, x, y):
        pygame.draw.rect(win, color, (x, y, self.grid_size, self.grid_size))

    def draw_transparent(self, color, x, y):
        surface = pygame.Surface((self.grid_size, self.grid_size))
        surface.set_alpha(75)
        pygame.draw.rect(surface, color, surface.get_rect())
        win.blit(surface, (x, y))

    def draw_circle(self, color, x, y):
        surface = pygame.Surface((self.grid_size, self.grid_size))
        pygame.draw.circle(win, color, (x, y), self.grid_size/ 4)
        # win.blit(surface, (x, y))


    def draw_reset(self):
        win.fill(BLACK)


class Game():
    def __init__(self, draw):
        pass

    def run(self):
        pass

    # SET


draw = Draw()
game = Game(draw)


# BUILD
build = True
while build:
    level = Level(width=WIDTH, height=HEIGHT, grid_size=20, draw=draw)
    level.MazeBuild()
    if level.maze_finish_position == (0, 0) or level.maze_start_position == (0, 0):
        level.draw.draw_reset()
        del level
    else:
        build = False



player = Player(level, draw)
player_controller = Player_Controller(player)

ai_controller_01 = AI_Controller(draw, level, player)


myfont = pygame.font.SysFont("monospace", 10)
ai_controller_01.set_navigation()
ai_controller_01.set_route()


# RUN
run = True
while run:
    # clock.tick(10)
    # pygame.time.delay(100)

    level.world_run_before()
    # player_controller.set_current_position()
    player_controller.set_mouse_position()

    player.set_climb_positions_visited()
    player.draw_player()
    # player.draw_climb_positions_visited()

    level.world_run_after()
    player.set_dark_positions()
    player.draw_light_positions()
    player.set_selected()
    ai_controller_01.draw_ends()
    ai_controller_01.draw_route()

    # win.blit(text, (1,45))

    pygame.display.update()

    run = player_controller.run

pygame.quit()
