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
GRID_SIZE = 20
BUILD_DEBUG = True
RUN_DEBUG = True
LIGHTS = False

# WINDOW
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game")


class Level():
    def __init__(self, draw):
        self.draw = draw

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

    def MazeBuild(self, build_debug):
        self.set_grid()
        mazebuild = True
        while mazebuild == True:
            self.draw_build_grid(build_debug)
            self.set_current_position()
            self.set_past_positions()
            self.set_next_position()
            self.set_wall_break_positions()
            self.draw_build_wall_break_positions(build_debug)
            if len(self.past_positions) > 2 and self.current_poistion == self.past_positions[0]:
                self.set_maze_start_position()
                self.set_maze_finish_position()
                self.set_camp_positions()
                self.set_paths()
                self.setWater()
                self.set_climb()
                self.draw_build_grid_hide(build_debug)
                self.set_world_top()
                mazebuild = False
            pygame.display.update()

    def set_camp_positions(self):
        for i in range(0, WIDTH, 20):
            self.camp_positions.append(
                (i, self.maze_start_position[1] - self.draw.grid_size))

    def set_world_top(self):
        self.world_top_surface = pygame.Surface(
            (self.draw.width, self.draw.grid_size * 3))

    def set_paths(self):
        mylist = self.past_positions + self.wall_break_positions
        mylist.append(self.maze_start_position)
        mylist.append(self.maze_finish_position)
        self.paths = list(dict.fromkeys(mylist))

    def set_maze_start_position(self):
        poss_maze_start = []
        for p in self.past_positions:
            if p[1] == self.draw.grid_size * self.top_ofset:
                if p[0] < ((WIDTH - self.draw.grid_size * 2) * (1/3)):
                    poss_maze_start.append(p)

        if len(poss_maze_start) > 0:
            poss_maze_start = random.choice(poss_maze_start)
            self.maze_start_position = (
                poss_maze_start[0], poss_maze_start[1] - self.draw.grid_size)
            self.draw.draw(
                BLACK_VERY_LIGHT, self.maze_start_position[0], self.maze_start_position[1])
        else:
            self.maze_start = None

    def set_maze_finish_position(self):
        poss_maze_finish = []
        for p in self.past_positions:
            if p[0] == WIDTH - (self.draw.grid_size * 2):
                if p[1] > ((HEIGHT - self.draw.grid_size * 2) * (2/3)):
                    poss_maze_finish.append(p)

        if len(poss_maze_finish) > 0:
            poss_maze_finish = random.choice(poss_maze_finish)
            self.maze_finish_position = (
                poss_maze_finish[0] + self.draw.grid_size, poss_maze_finish[1])
            self.draw.draw(
                BLUE_VERY_LIGHT, self.maze_finish_position[0], self.maze_finish_position[1])
        else:
            self.maze_finish = None

    def set_grid(self):
        self.grid = [(x, y) for x in range(self.draw.grid_size, self.draw.width, self.draw.grid_size * 2)
                     for y in range(self.draw.grid_size * self.top_ofset, self.draw.height - (self.draw.grid_size * 2), self.draw.grid_size * 2) if (x, y)]

        for i in range(len(self.grid) // 3):
            random_item_from_list = random.choice(self.grid)
            self.grid.remove(random_item_from_list)

    def set_wall_break_positions(self):
        result = ((self.next_position[0] - self.current_poistion[0]) //
                  2, (self.next_position[1] - self.current_poistion[1]) // 2)
        result02 = (
            self.current_poistion[0] + result[0], self.current_poistion[1] + result[1])
        self.wall_break_positions.append(result02)

    def set_climb(self):
        for p in self.paths:
            check_right = (p[0] + self.draw.grid_size, p[1])
            check_left = (p[0] - self.draw.grid_size, p[1])
            if check_right not in self.paths and check_left not in self.paths:
                self.climb_positions.append(p)

    def setWater(self):
        poss_water_list = []
        not_water_list = []
        is_water_list = []
        for p in self.paths:
            possWater = (p[0], p[1] + self.draw.grid_size)
            if possWater not in self.paths:
                poss_water_list.append((p[0], p[1]))
            else:
                not_water_list.append((p[0], p[1]))

        run = True
        while run == True:
            i = 1
            start = len(poss_water_list)
            for p in poss_water_list:
                possWaterRight = (p[0] + self.draw.grid_size, p[1])
                possWaterLeft = (p[0] - self.draw.grid_size, p[1])
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
            if p[1] > ((HEIGHT - self.draw.grid_size * 2) * (2/3)):
                poss_water_list.append(p)
                self.water_list = poss_water_list

    def set_current_position(self):
        if len(self.current_poistion) == 0:
            position = random.choice(self.grid)
            self.current_poistion = position
        else:
            self.current_poistion = self.next_position

    def set_next_position(self):
        random.shuffle(DIRECTIONS)
        poss_directions = []
        poss_position_List = []
        for d in DIRECTIONS:
            poss_position = (self.current_poistion[0] + (
                d[0] * self.draw.grid_size * 2), self.current_poistion[1] + (d[1] * self.draw.grid_size * 2))
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

    def draw_world_top_surface(self):
        pygame.draw.rect(self.world_top_surface, WHITE,
                         self.world_top_surface.get_rect())
        win.blit(self.world_top_surface, (0, 0))

    def draw_paths(self):
        for p in self.paths:
            self.draw.draw(BLACK_VERY_LIGHT, p[0], p[1])

    def draw_water(self):
        for p in self.water_list:
            self.draw.draw_transparent(BLUE_LIGHT, p[0], p[1])

    def draw_build_grid(self, build_debug):
        if build_debug == True:
            for i in self.grid:
                self.draw.draw(BLACK_VERY_LIGHT, i[0], i[1])

    def draw_build_grid_hide(self, build_debug):
        if build_debug == True:
            directions_list = []
            for g in self.grid:
                for d in DIRECTIONS:
                    if (g[0] + (d[0] * self.draw.grid_size), g[1] + (d[1] * self.draw.grid_size)) not in self.wall_break_positions:
                        directions_list.append((d[0], d[1]))
                if len(directions_list) == 4:
                    self.draw.draw(BLACK, g[0], g[1])
                directions_list.clear()

    def draw_build_wall_break_positions(self, build_debug):
        if build_debug == True:
            self.draw.draw(
                BLACK_VERY_LIGHT, self.wall_break_positions[-1][0], self.wall_break_positions[-1][1])

    def draw_debug_climb_positions(self, run_debug):
        if run_debug == True:
            for p in self.climb_positions:
                pygame.draw.rect(
                    win, GREEN, (p[0] + self.draw.grid_size * 7/16, p[1], self.draw.grid_size/8, self.draw.grid_size))

    def draw_debug_start_position(self, run_debug):
        if run_debug == True:
            p = self.past_positions[0]
            self.draw.draw_outline(RED, p[0], p[1])


class Character():
    def __init__(self, level, draw):
        self.level = level
        self.draw = draw

        self.selected = False
        self.current_poistion = random.choice(self.level.camp_positions)
        self.paths = self.level.paths
        self.camp_positions = self.level.camp_positions
        self.velocity = 20
        self.climb_positions = self.level.climb_positions
        self.climb_positions_visited = []
        self.water_list = self.level.water_list

    def events(self):
        print("Character event")

    def set_position(self, event):
        x, y = self.current_poistion

        if event == key_left:
            x -= self.velocity
        if event == key_right:
            x += self.velocity
        if event == key_up:
            y -= self.velocity
        if event == key_down:
            y += self.velocity

        if (x, y) in self.paths or (x, y) in self.camp_positions:
            self.current_poistion = (x, y)
            pygame.time.delay(150)

        pygame.time.delay(100)

    def set_climb_positions_visited(self):
        if self.current_poistion in self.climb_positions:
            self.climb_positions_visited.append(self.current_poistion)

    def set_selected(self):
        pass
        # x, y = self.player_controller.select_location

    def draw_climb_positions_visited(self):
        for p in self.climb_positions_visited:
            if p not in self.water_list:
                pygame.draw.rect(
                    win, RED, (p[0] + self.grid_size * 7/16, p[1], self.draw.grid_size/8, self.draw.grid_size))

    def draw_player(self):
        self.draw.draw(RED, self.current_poistion[0], self.current_poistion[1])
        if self.selected:
            self.draw.draw_circle(WHITE, self.current_poistion[0] + (
                self.draw.grid_size/2), self.current_poistion[1] + (self.draw.grid_size/2))


class Player_Controller():
    def __init__(self, draw, level, character):
        self.draw = draw
        self.level = level
        self.character = character

        self.run = True
        self.select_location = (0, 0)

    def events(self):
        x, y = self.character.current_poistion



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(up)
                elif event.key == pygame.K_DOWN:
                    self.turn(down)
                elif event.key == pygame.K_LEFT:
                    self.turn(left)
                elif event.key == pygame.K_RIGHT:
                    self.turn(right)



        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            return "K_LEFT"
        if keys[pygame.K_RIGHT]:
            return "K_RIGHT"
        if keys[pygame.K_UP]:
            return "K_UP"
        if keys[pygame.K_DOWN]:
            return "K_DOWN"

        if (x, y) in self.character.paths or (x, y) in self.character.camp_positions:
            self.character.current_poistion = (x, y)
            pygame.time.delay(150)



        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                x, y = pos
                x_grid = (x // self.draw.grid_size) * self.draw.grid_size
                y_grid = (y // self.draw.grid_size) * self.draw.grid_size
                self.select_location = (x_grid, y_grid)
                print(pos)
                print(self.select_location)

            if event.type == pygame.QUIT:
                self.run = False



class AI_Controller():
    def __init__(self, draw, level, character, player_controller):
        self.draw = draw
        self.level = level
        self.character = character
        self.player_controller = player_controller

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
                direction = (p[0] + (d[0] * self.draw.grid_size),
                             p[1] + (d[1] * self.draw.grid_size))
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
        route_list_A.append(self.character.current_poistion)
        if self.player_controller.select_location in self.level.paths:
            route_list_B.append(self.player_controller.select_location)
        else:
            route_list_B.append(self.character.current_poistion)

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

    def draw_debug_route(self, run_debug):
        if run_debug == True:
            for p in self.route_list:
                self.draw.draw_outline(GREEN, p[0], p[1])

    def draw_debug_ends(self, run_debug):
        if run_debug == True:
            for k, v in dict.items(self.path_type):
                text = self.draw.font.render("{0}".format(v), 1, (0, 0, 0))
                win.blit(text, (k[0] + 1, k[1] + 5))


class Lights():
    def __init__(self, draw, level, character):
        self.draw = draw
        self.level = level
        self.character = character

    def set_dark_positions(self, lights):
        self.dark_positions = dict.fromkeys(self.level.paths, lights)
        self.dark_positions[self.character.current_poistion] = False

        lightList = []
        for x in range(self.character.current_poistion[0] - self.draw.grid_size, self.character.current_poistion[0] + self.draw.grid_size * 2, self.draw.grid_size):
            for y in range(self.character.current_poistion[1] - self.draw.grid_size, self.character.current_poistion[1] + self.draw.grid_size * 2, self.draw.grid_size):
                lightList.append((x, y))
        for i in lightList:
            self.dark_positions[i] = False

        posslightposition = self.level.maze_start_position
        run = True
        while run:
            if posslightposition in self.level.paths:
                self.dark_positions[posslightposition] = False
                posslightposition = (
                    posslightposition[0], posslightposition[1] + self.draw.grid_size)
            else:
                run = False

    def draw_light_positions(self):
        listOfKeys = list()
        listOfItems = self.dark_positions.items()
        for item in listOfItems:
            if item[1] == True:
                listOfKeys.append(item[0])
        for p in listOfKeys:
            self.draw.draw(BLACK, p[0], p[1])


class Draw():
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT
        self.grid_size = GRID_SIZE

        self.font = pygame.font.SysFont("monospace", 10)

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
        pygame.draw.circle(win, color, (x, y), self.grid_size / 4)

    def draw_reset(self):
        win.fill(BLACK)


class Game():
    def __init__(self):
        pass

    def event_player_controller(self):
        pass
        if self.player_controller.events() != False:
            print(self.player_controller.events())
        # if self.player_controller.events() == "Lefty!":
        #     print(self.character.events())
        #     # print("left")

    def set_draw(self):
        self.draw = Draw()

    def set_player_controller(self):
        self.player_controller = Player_Controller(
            self.draw, self.level, self.character)

    def set_ai_controller(self):
        self.ai_controller_01 = AI_Controller(
            self.draw, self.level, self.character, self.player_controller)

    def set_level(self, build_debug):
        build = True
        while build:
            self.level = Level(self.draw)
            self.level.MazeBuild(build_debug)
            if self.level.maze_finish_position == (0, 0) or self.level.maze_start_position == (0, 0):
                self.level.draw.draw_reset()
                del self.level
            else:
                build = False

    def set_character(self):
        self.character = Character(self.level, self.draw)

    def set_lights(self):
        self.lights = Lights(self.draw, self.level, self.character)

    def build(self, build_debug):
        self.set_draw()
        self.set_level(build_debug)
        self.set_character()
        self.set_player_controller()
        self.set_ai_controller()
        self.set_lights()

        self.ai_controller_01.set_navigation()

    def run_level_background(self):
        self.level.draw_paths()
        self.level.draw_world_top_surface()

    def run_character(self):
        self.character.set_climb_positions_visited()
        self.character.draw_player()
        self.character.set_selected()
        # self.character.draw_climb_positions_visited()

    def run_player_controller(self):
        self.player_controller.events()

    def run_ai_controller(self):
        self.ai_controller_01.set_route()

    def run_level_forground(self):
        self.level.draw_water()

    def run_lights(self):
        self.lights.set_dark_positions(LIGHTS)
        self.lights.draw_light_positions()

    def run_debug(self, run_debug):
        self.level.draw_debug_start_position(run_debug)
        self.level.draw_debug_climb_positions(run_debug)
        self.ai_controller_01.draw_debug_ends(run_debug)
        self.ai_controller_01.draw_debug_route(run_debug)

        pygame.display.update()


# BUILD
game = Game()
game.build(build_debug=BUILD_DEBUG)


# RUN
run = True
while run:
    game.event_player_controller()
    game.run_level_background()
    game.run_character()
    game.run_player_controller()
    game.run_ai_controller()
    game.run_level_forground()
    game.run_lights()
    game.run_debug(run_debug=RUN_DEBUG)
    run = game.player_controller.run
pygame.quit()

# clock.tick(10)
# pygame.time.delay(100)

# win.blit(text, (1,45))
