import pygame
from pygame.event import Event

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.view.view import View


class Window:
    def __init__(self, title: str, view_width: int, view_height: int, grid_size: int):

        self.view_width = view_width
        self.view_height = view_height
        self.scale = 1

        self.window_width = (grid_size * 2) + (grid_size * view_width)
        self.window_height = (grid_size * 2) + (grid_size * view_height)

        self.events: list[Event]

        pygame.display.set_caption(title)

        self.window_surface = self.get_window_surface()
        self.window_quit = False

    def get_window_quit(self, view: "View"):
        for e in view.window_events:
            if e.type == pygame.QUIT:
                return True

    @property
    def win_event(self) -> list[Event]:
        res_get = pygame.event.get()
        return res_get

    #! breaks when used as property!
    def get_window_surface(self):
        size = (self.window_width * 1, self.window_height * 1)
        flags = 0
        depth = 32
        return pygame.display.set_mode(size, flags, depth)

    @property
    def window_size_scaled(self):
        return (self.view_width * self.scale, self.view_height * self.scale)

    @property
    def scaled_window_surface(self):
        res = pygame.transform.scale(self.window_surface, self.window_size_scaled)
        return res

        # draw window

    @staticmethod
    def close_window():
        pygame.quit()
