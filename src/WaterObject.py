import pygame

from src.LevelObject import LevelObject


class WaterObject(LevelObject):
    value: int = 75  # for set_alpha

    def surface(self):
        surface = pygame.Surface(self.rect)
        surface.set_alpha(self.value)
        return surface
