import pygame
import random

# CONSTANTS
DOWN = (0, -1)
RIGHT = (1, 0)
LEFT = (-1, 0)
UP = (0, 1)
DIRECTIONS = [DOWN, LEFT, RIGHT, UP]

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
RED_VERY_LIGHT = (255, 210, 210)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLUE_LIGHT = (125, 125, 255)
BLUE_VERY_LIGHT = (210, 210, 255)


WIDTH = 1020
HEIGHT = 1020

# WINDOW
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
# win = pygame.display.set_mode((display_width, display_height), pygame.FULLSCREEN)
pygame.display.set_caption("First Game")

class Maze():
    def __init__(self, width, height, grid_size,):
        self.width = width
        self.height = height
        self.grid_size = grid_size
        self.path_return = []
        self.grid = []
        self.next_position = ()
        self.paths = []
        self.wall_break_positions = []
        self.past_positions = []
        self.current_poistion = ()


    def MazeBuild(self):
        

    def set_paths(self):
        self.paths = self.past_positions + self.wall_break_positions

    def set_grid(self):
        w = self.width
        h = self.height
        g_s = self.grid_size
        self.grid = [(x, y) for x in range(g_s, w, g_s*2)
                     for y in range(g_s, h, g_s * 2) if (x, y)]

        for i in range(len(self.grid) // 3):
            random_item_from_list = random.choice(self.grid)
            self.grid.remove(random_item_from_list)

    def draw_grid(self):
        for i in self.grid:
            self.draw(WHITE, i[0], i[1])

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
        self.draw(WHITE, result02[0], result02[1])

    def setWater02(self):
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
                if possWaterRight in not_water_list or possWaterLeft in not_water_list:
                    not_water_list.append(p)
                    poss_water_list.remove(p)
            end = len(poss_water_list)
            if start == end:
                run = False
            i += 1

        for p in self.paths:
            if p[1] > (WIDTH // 1.6):
                poss_water_list.append(p)

        # DRAW
        for p in poss_water_list:
            self.draw_transparent(BLUE_LIGHT, p[0], p[1])

    def set_current_position(self):
        if len(self.current_poistion) == 0:
            position = random.choice(self.grid)
            self.current_poistion = position
        else:
            self.current_poistion = self.next_position

            # DRAW
            # for p in self.path_return:
            #     self.draw(RED_VERY_LIGHT, p[0], p[1])

            self.draw(
                RED, self.current_poistion[0], self.current_poistion[1])

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

        # DRAW
        # for d in poss_position_List:
        #     self.draw(BLUE_LIGHT, d[0], d[1])
        # self.draw(BLUE, self.next_position[0], self.next_position[1])

    def set_past_positions(self):
        self.past_positions.append(self.current_poistion)

    # DRAW METHOD
    def draw(self, color, x, y):
        pygame.draw.rect(
            win, color, (x, y, self.grid_size, self.grid_size))

    def draw_transparent(self, color, x, y):
        surface = pygame.Surface((self.grid_size, self.grid_size))
        surface.set_alpha(50)
        pygame.draw.rect(surface, color, surface.get_rect())
        win.blit(surface, (x, y))


maze01 = Maze(width=WIDTH, height=HEIGHT, grid_size=20)

maze01.set_grid()


mazebuild = True
while mazebuild == True:

    pygame.time.delay(10)

    maze01.draw_grid()

    maze01.set_current_position()

    maze01.set_past_positions()
    maze01.set_next_position()
    maze01.set_wall_break_positions()

    if len(maze01.past_positions) > 2 and maze01.current_poistion == maze01.past_positions[0]:

        maze01.draw_grid_hide()
        maze01.set_paths()
        maze01.setWater02()
        mazebuild = False
        print("mazebuild", mazebuild)

    pygame.display.update()


run = True
while run:
    # clock.tick(10)
    # pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


pygame.quit()
