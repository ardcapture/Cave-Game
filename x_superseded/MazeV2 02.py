import pygame
import random
pygame.init()



display_width = 500
display_height = 500



win = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("First Game")

x = 50
y = 50
width = 40
height = 60
vel = 5


# drawGrid01(win)




class Maze():
    def __init__(self):
        self.grid_size = 20
        self.grid = []
        self.current_poistion = (60, 60)
        self.next_position = (0, 0)
        self.past_positions = [(100,20), (100, 60), (100, 100)]

    def set_grid(self):
        for x in range(self.grid_size, display_width, self.grid_size*2):
            for y in range(self.grid_size, display_height, self.grid_size*2):
                if (x, y) not in self.grid:
                    self.grid.append((x, y))
        # print("self.grid", self.grid)
        for i in self.grid:
            pygame.draw.rect(win, (255,255,255), (i[0], i[1], self.grid_size , self.grid_size))

    def set_current_position(self):
        print("self.current_poistion", self.current_poistion)
        pygame.draw.rect(win, (255,0,0), (self.current_poistion[0], self.current_poistion[1], self.grid_size , self.grid_size))
        self.current_poistion = self.next_position

    def set_next_position(self):
        directions  = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        poss_directions = []
        poss_position_List = []
        for d in directions:
            poss_position = (self.current_poistion[0] + (d[0] * self.grid_size * 2), self.current_poistion[1] + (d[1] * self.grid_size * 2))
            print("poss_position", poss_position)
            if poss_position in self.grid:
                if poss_position not in self.past_positions:
                    poss_position_List.append(poss_position)

        if len(poss_position_List) > 1:
            result = random.choice(poss_position_List)
        if len(poss_position_List) == 0:
            if self.current_poistion in self.past_positions:
                index = self.past_positions.index(self.current_poistion)
                result = self.past_positions[index - 1]
            else:
                result = self.past_positions[-1]
        if len(poss_position_List) == 1:
            result = poss_position_List[0]

        self.next_position = result

        #PRINT            
        print("poss_position_List", poss_position_List)


        #DRAW
        for d in poss_position_List:
                pygame.draw.rect(win, (125,125,255), (d[0], d[1], self.grid_size , self.grid_size))
        
        pygame.draw.rect(win, (0,0,255), (poss_position[0], poss_position[1], self.grid_size , self.grid_size))
        

    def set_past_positions(self):

        self.past_positions.append(self.current_poistion)


        #DRAW
        for p in self.past_positions:
            pygame.draw.rect(win, (255,125,125), (p[0], p[1], self.grid_size , self.grid_size))



maze01 = Maze()



run = True
while run:
    # clock.tick(10)
    pygame.time.delay(1000)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    maze01.set_grid()
    maze01.set_past_positions()

    maze01.set_next_position()
    maze01.set_current_position()


    pygame.display.update()

pygame.quit()
