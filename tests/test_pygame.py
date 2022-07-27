import pygame

pygame.init()

window = pygame.display.set_mode(size=(100, 100), flags=0, depth=32)


while True:
    window.blit(window)