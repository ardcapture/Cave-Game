from typing import TYPE_CHECKING

import pygame
from pygame.event import Event

from src.utilities import Positions, WindowEvent

if TYPE_CHECKING:
    from src.level import Level
    from src.view import View

KEY_DOWN = pygame.KEYDOWN
KEY_UP = pygame.KEYUP
K_BACKQUOTE = pygame.K_BACKQUOTE
K_DOWN = pygame.K_DOWN
K_LEFT = pygame.K_LEFT
K_RIGHT = pygame.K_RIGHT
K_UP = pygame.K_UP
MOUSE_BUTTON_DOWN = pygame.MOUSEBUTTONDOWN
MOUSE_BUTTON_UP = pygame.MOUSEBUTTONUP
MOUSE_MOTION = pygame.MOUSEMOTION
WINDOW_CLOSE = pygame.WINDOWCLOSE  # used to be WINDOW_QUIT = pygame.QUIT


class Window:
    pygame_events: list[Event] = []

    KEYBOARD_EVENTS = [KEY_DOWN, KEY_UP]
    KEYBOARD_KEYS = [K_BACKQUOTE, K_DOWN, K_LEFT, K_RIGHT, K_UP]
    MOUSE_BUTTON_EVENTS = [MOUSE_BUTTON_UP, MOUSE_BUTTON_DOWN]

    pos = Positions(0, 0)
    key = 0
    state = 0
    m_event = WindowEvent(pos, key, state)

    scale = 1

    def __init__(self, view: "View", level: "Level"):
        self.view_width = view.width
        self.view_height = view.height

        self.window_width = (level.GRID_SIZE * 2) + (level.GRID_SIZE * view.width)
        self.window_height = (level.GRID_SIZE * 2) + (level.GRID_SIZE * view.height)

        self.events: list[Event]

        pygame.display.set_caption(view.title)

        self.window_surface = self.get_window_surface()

    def update(self):
        self.pygame_events = pygame.event.get()
        self.m_event = self.control_pygame_events()

    def control_pygame_events(self):
        for event in self.pygame_events:
            if event.type == WINDOW_CLOSE:
                pos = Positions(0, 0)
                key = 0
                state = event.type
            elif event.type in self.MOUSE_BUTTON_EVENTS:
                x, y = event.pos
                pos = Positions(x, y)
                key = event.button
                state = event.type
            elif event.type in self.KEYBOARD_EVENTS:
                pos = Positions(0, 0)
                state = event.type
                key = event.key
            elif event.type == MOUSE_MOTION:
                x, y = event.pos
                pos = Positions(x, y)
                key = 0
                state = 0
                if any(event.buttons):
                    key = event.buttons.index(1) + 1
                    state = event.type
            else:
                pos = Positions(0, 0)
                key = 0
                state = 0

            return WindowEvent(pos, key, state)

    @property
    def event_keyboard(self):
        if self.m_event and self.m_event.key in self.KEYBOARD_KEYS:
            return self.m_event.key

    @property
    def mouse_event_run(self):
        if not self.m_event:
            return Positions(0, 0)
        position = self.m_event.pos
        return position if self.m_event.state == MOUSE_BUTTON_DOWN else Positions(0, 0)

    #! breaks when used as property!
    def get_window_surface(self):
        size = (self.window_width * 1, self.window_height * 1)
        flags = 0
        depth = 32
        return pygame.display.set_mode(size, flags, depth)

    @staticmethod
    def close_window():
        pygame.quit()
