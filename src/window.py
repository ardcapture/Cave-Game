import pygame
from pygame.event import Event

from src.utilities import WindowEvent
from src.position import Position

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

    pos = Position(0, 0)
    key = 0
    state = 0
    m_event = WindowEvent(pos, key, state)

    scale = 1

    def __init__(
        self,
        title: str,
        width: int,
        height: int,
        width_multiplier: int,
        height_multiplier: int,
    ):
        self.window_width = width
        self.window_height = height

        self.size = (
            self.window_width * width_multiplier,
            self.window_height * height_multiplier,
        )

        self.events: list[Event]

        pygame.display.set_caption(title)

        self.window_surface: pygame.surface.Surface = pygame.display.set_mode(
            self.size, 0, 32
        )

    def set_m_event(self):
        self.m_event = self.control_pygame_events()

    def control_pygame_events(self):
        for event in self.pygame_events:
            if event.type == WINDOW_CLOSE:
                pos = Position(0, 0)
                key = 0
                state = event.type
            elif event.type in self.MOUSE_BUTTON_EVENTS:
                x, y = event.pos
                pos = Position(x, y)
                key = event.button
                state = event.type
            elif event.type in self.KEYBOARD_EVENTS:
                pos = Position(0, 0)
                state = event.type
                key = event.key
            elif event.type == MOUSE_MOTION:
                x, y = event.pos
                pos = Position(x, y)
                key = 0
                state = 0
                if any(event.buttons):
                    key = event.buttons.index(1) + 1
                    state = event.type
            else:
                pos = Position(0, 0)
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
            return Position(0, 0)
        position = self.m_event.pos
        return position if self.m_event.state == MOUSE_BUTTON_DOWN else Position(0, 0)

    @staticmethod
    def close_window():
        pygame.quit()
