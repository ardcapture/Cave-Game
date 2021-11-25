import pygame
import os



pygame.init()
screen = pygame.display.set_mode((200, 50))

GRID_SIZE = 64

imagesPath = 'PyGame'

def return_image(image, path, scale):
    res = pygame.image.load(os.path.join(path, image))
    res = pygame.transform.scale(res, scale)
    return res

image = return_image('grass.png', imagesPath, (GRID_SIZE, GRID_SIZE))
shadow = return_image('dirt.png', imagesPath, (GRID_SIZE, GRID_SIZE))


# screen.blits()


# image = pygame.image.load("grass.png")
# shadow = pygame.image.load("dirt.png")

merged = image.copy()
merged.blit(shadow, (0, 0))

while True:  
    screen.fill(pygame.color.Color('white'))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise

    # screen.blits((image, (0,  0)), (shadow, (50, 0)))            
    # screen.blit
    screen.blit(image, (100, 0))
    screen.blit(shadow, (100, 0))
    screen.blit(merged, (150, 0))
    pygame.display.flip()



# 3D Matrix

[[[255   0   0]
  [255   0   0]
  [255   0   0]
  ...
  [  0   0   0]
  [  0   0   0]
  [  0   0   0]]

 [[255   0   0]
  [255   0   0]
  [255   0   0]
  ...
  [  0   0   0]
  [  0   0   0]
  [  0   0   0]]

 [[255   0   0]
  [255   0   0]
  [255   0   0]
  ...
  [  0   0   0]
  [  0   0   0]
  [  0   0   0]]

 ...

 [[255 255 255]
  [255 255 255]
  [255 255 255]
  ...
  [  0   0   0]
  [  0   0   0]
  [  0   0   0]]

 [[255 255 255]
  [255 255 255]
  [255 255 255]
  ...
  [  0   0   0]
  [  0   0   0]
  [  0   0   0]]

 [[255 255 255]
  [255 255 255]
  [255 255 255]
  ...
  [  0   0   0]
  [  0   0   0]
  [  0   0   0]]]