from typing import TYPE_CHECKING
import pygame
import os


from pygame import Surface

if TYPE_CHECKING:
    from src.level import Level


PATH_IMAGES: str = "res"


def dirt_image(level):
    paths = "dirt.png"
    return get_surface_file(paths, level)


def grass_image(level):
    paths = "grass.png"
    return get_surface_file(paths, level)


def rock_image(level: "Level") -> Surface:
    paths = "rock.png"
    return get_surface_file(paths, level)


# window = self.window.window_surface

# text = (self.get_surface_text,)

# light = (self.get_surface_lights,)


def get_surface_file(paths, level: "Level"):
    path = PATH_IMAGES
    filename = os.path.join(path, paths)
    surface = pygame.image.load(filename)
    size = level.GRID_SIZE_2D
    return pygame.transform.scale(surface, size)
