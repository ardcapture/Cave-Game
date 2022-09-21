import pygame
from src.utilities import MouseEvent

TypeEvent = pygame.event.Event

MOUSE_BUTTON_UP = pygame.MOUSEBUTTONUP
MOUSE_BUTTON_DOWN = pygame.MOUSEBUTTONDOWN
MOUSE_MOTION = pygame.MOUSEMOTION


class Mouse:
    def __init__(self):
        self.mouse_button_up: MouseEvent
        self.mouse_button_down: MouseEvent
        self.mouse_motion: MouseEvent

    def update(self, view):
        self.events = view.window_events

    @property
    def mouse_event_run(self):
        if self.mouse_button_up:
            position = self.mouse_button_up.pos
            button = self.mouse_button_up.button
            if button:
                return position

    @property
    def mouse_button_up(self):
        for event in self.events:
            if event.type == MOUSE_BUTTON_UP:
                pos = event.pos
                button = event.button
                return MouseEvent(pos, button)

    @property
    def mouse_button_down(self):
        for event in self.events:
            if event.type == MOUSE_BUTTON_DOWN:
                pos = event.pos
                button = event.button
                return MouseEvent(pos, button)

    @property
    def mouse_motion(self) -> MouseEvent:
        for event in self.events:
            if event.type == MOUSE_MOTION:
                return self.is_mouse_motion(event)
        pos = (0, 0)
        button = False
        return MouseEvent(pos, button)

    def is_mouse_motion(self, event: TypeEvent) -> MouseEvent:
        pos = event.pos
        button = False
        if any(event.buttons):
            button = event.buttons.index(1) + 1

        return MouseEvent(pos, button)
