import pygame
import random
pygame.init()



display_width = 500
display_height = 500
grid_size = 20


win = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("First Game")

x = 50
y = 50
width = 40
height = 60
vel = 5


def drawGrid01(surface):
    for y in range(grid_size, display_height):
        for x in range(grid_size, display_width):
            if (x+y) % 2 == 0:
                r = pygame.Rect((x*grid_size, y*grid_size),
                                (grid_size, grid_size))
                pygame.draw.rect(surface, (93, 216, 228), r)
            else:
                rr = pygame.Rect((x*grid_size, y*grid_size),
                                 (grid_size, grid_size))
                pygame.draw.rect(surface, (84, 194, 205), rr)


# drawGrid01(win)

grid = []


def drawGrid(surface, grid):
    for x in range(grid_size, display_width, grid_size*2):
        for y in range(grid_size, display_height, grid_size*2):
            if (x, y) not in grid:
                grid.append((x, y))
    for i in grid:
        r = pygame.Rect((i[0], i[1]), (grid_size, grid_size))
        pygame.draw.rect(surface, (255, 255, 255), r)





class gridVisiter():
    def __init__(self, grid):
        self.grid = grid
        self.gridVisiting = (20, 20)
        self.gridVisited = [self.gridVisiting,]
        self.gridWallsVisited = []


    def gridVisit(self, surface):
        print("len(self.grid)", len(self.grid))
        if self.gridVisited == (len(self.grid) - 1):
            print("stop!!!!!!!!!!!!")
        else:
            self.gridVisiting += 1
            print("self.gridVisiting", self.gridVisiting)
            self.gridVisited += 1
            print("self.gridVisited", self.gridVisited)


    def setGetVisitingSurroundingClear(self):
        result = []
        directions = [(1, 0), (-1, 0), (0, 1),(0, -1),]
        for d in directions:
            poss_visit = ((self.gridVisiting[0] + (d[0] * (grid_size * 2))), (self.gridVisiting[1] + (d[1] * (grid_size * 2))))
            if poss_visit in self.grid:
                result.append(poss_visit)
        print("getVisitingSurroundingClear", result)
        self.getVisitingSurroundingClear = result
            



    def getNextGridVisit(self):
        if self.getVisitingSurroundingClear:
            next_visit = random.choice(self.getVisitingSurroundingClear)
            print("next_visit", next_visit)
            self.gridVisiting = next_visit
            self.gridVisited.append(next_visit)
            print("let's go")
        else:
            print("noooooo")




        # poss_visits = []
        # directionOptions = [(1, 0), (-1, 0), (0, 1),(0, -1),]
        # while len(poss_visits) < 4:
        #     print("loop")
        #     direction = random.choice(directionOptions)
        #     poss_visit = ((self.gridVisiting[0] + (direction[0] * (grid_size * 2))), (self.gridVisiting[1] + (direction[1] * (grid_size * 2))))
        #     print("poss_visit", poss_visit)
        #     if poss_visit in self.grid:
        #         print("yes in grid!")
        #         if poss_visit not in self.gridVisited and poss_visits:
        #             self.gridVisiting = poss_visit
        #             print("self.gridVisiting", self.gridVisiting)
        #             self.gridVisited.append(poss_visit)
        #             print("self.gridVisited", self.gridVisited)
        #             break
        #     else:
        #         poss_visits.append(poss_visit)
        #         print("poss_visits", poss_visits)




    def drawGridVisiting(self):
        print("self.gridVisiting", self.gridVisiting)
        r = pygame.Rect(self.gridVisiting, (grid_size, grid_size))
        pygame.draw.rect(win, (255, 0, 0), r)

    def drawGetVisitingSurroundingClear(self):
        for c in self.getVisitingSurroundingClear:

            pygame.draw.rect(win, (0,0,255), (c[0], c[1], grid_size /2 , grid_size /2))
            
            # r = pygame.Rect(c, (grid_size, grid_size))
            # pygame.draw.rect(win, (0, 0, 255), r)
        pygame.time.delay(100)

    def drawGridVisited(self):
        print("self.gridVisited", self.gridVisited)
        for g in self.gridVisited:

 

            r = pygame.Rect(g, (grid_size, grid_size))
            pygame.draw.rect(win, (255, 174, 175), r)

        

gridVisiter01 = gridVisiter(grid)


run = True
while run:
    # clock.tick(10)
    pygame.time.delay(1000)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    drawGrid(win, grid)

    gridVisiter01.setGetVisitingSurroundingClear()

    gridVisiter01.getNextGridVisit()

    
    gridVisiter01.drawGridVisited()

    gridVisiter01.drawGridVisiting()
 
    gridVisiter01.drawGetVisitingSurroundingClear()
    


    # gridVisiter01.getNextGridVisit()

    
    # gridVisiter01.gridVisiting(win)

    # gridVisiter01.gridVisitRandom(win)
  

    # win.fill((0,0,0))  # Fills the screen with black
    # pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))
    pygame.display.update()

pygame.quit()
