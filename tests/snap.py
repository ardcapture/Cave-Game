import pygame
pygame.init()

screen = pygame.display.set_mode((200, 200))
clock = pygame.time.Clock()

def drawgrid(w, rows, surface):
    sizebtwn = w // rows
    for i in range(0, w, sizebtwn):
        x, y = i, i
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))

class Cube:
    def update(self, sizebtwn):
        x, y = pygame.mouse.get_pos()
        ix = x // sizebtwn
        iy = y // sizebtwn
        self.cx, self.cy = ix * sizebtwn, iy * sizebtwn
        self.square = pygame.Rect(self.cx, self.cy, sizebtwn, sizebtwn)
    def draw(self, surface):
        click = pygame.mouse.get_pressed()
        if click[0]:
            pygame.draw.rect(surface, (255, 255, 255), self.square)

cube = Cube()

run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    cube.update(screen.get_width() // 10)

    screen.fill(0)
    drawgrid(screen.get_width(), 10, screen)
    cube.draw(screen)
    pygame.display.flip()