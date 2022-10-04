from typing import TYPE_CHECKING, NamedTuple

import pygame
from pygame.event import Event

from src.utilities import Position

if TYPE_CHECKING:
    from src.view.view import View


K_DOWN = pygame.K_DOWN
K_LEFT = pygame.K_LEFT
K_UP = pygame.K_UP
K_RIGHT = pygame.K_RIGHT
K_BACKQUOTE = pygame.K_BACKQUOTE


KEY_DOWN = pygame.KEYDOWN
KEY_UP = pygame.KEYUP

KEY_POSITIONS: dict[int, str] = {
    KEY_DOWN: "KEY_DOWN",
    KEY_UP: "KEY_UP",
}


KEYBOARD_EVENT: dict[int, str] = {
    K_DOWN: "K_DOWN",
    K_LEFT: "K_LEFT",
    K_UP: "K_UP",
    K_RIGHT: "K_RIGHT",
    K_BACKQUOTE: "K_BACKQUOTE",
}


class KeyboardEvent(NamedTuple):
    state: int
    key: str


class WindowEvent(NamedTuple):
    pos: Position
    key: int
    state: int


class Mouse:

    MOUSE_BUTTON_UP = pygame.MOUSEBUTTONUP
    MOUSE_BUTTON_DOWN = pygame.MOUSEBUTTONDOWN
    MOUSE_MOTION = pygame.MOUSEMOTION

    pos = Position(0, 0)
    key = 0
    state = 0
    m_event = WindowEvent(pos, key, state)

    def update(self, view: "View"):
        self.m_event = self.update_control(view)

    # TODO this wants improving!:
    def update_control(self, view: "View"):
        for event in view.window_events:

            if event.type in [self.MOUSE_BUTTON_UP, self.MOUSE_BUTTON_DOWN]:
                pos = event.pos
                key = event.button
                state = event.type
                return WindowEvent(pos, key, state)

            elif event.type == self.MOUSE_MOTION:
                pos = event.pos
                key = 0
                state = 0
                if any(event.buttons):
                    key = event.buttons.index(1) + 1
                    state = event.type
                return WindowEvent(pos, key, state)

            else:
                pos = Position(0, 0)
                key = 0
                state = 0
                return WindowEvent(pos, key, state)

    @property
    def mouse_event_run(self):
        if self.m_event:
            position = self.m_event.pos
            state = self.m_event.state
            if state == self.MOUSE_BUTTON_DOWN:
                return position


class Keyboard:

    state = 0
    key = "None"

    KeyboardEvent_default = KeyboardEvent(state, key)

    def __init__(self):

        self.set_position_keys = ("K_LEFT", "K_RIGHT", "K_UP", "K_DOWN")

        self.k_event = self.KeyboardEvent_default

    #  TODO need clean up
    def update(self, view: "View"):
        self.get_keyboard_event(view)

    def get_keyboard_event(self, view: "View"):
        if len(view.window_events) == 0:
            self.k_event = self.KeyboardEvent_default

        for event in view.window_events:
            if event.type in [KEY_DOWN, KEY_UP]:
                state = event.type
                key = KEYBOARD_EVENT.get(event.key, "False")
                self.k_event = KeyboardEvent(state, key)

            else:
                self.k_event = self.KeyboardEvent_default

    @property
    def event_keyboard(self):
        if self.k_event:
            if self.k_event.key in self.set_position_keys:
                return self.k_event.key

    @property
    def keyboard_state(self):
        if not self.event_key:
            return

        res_key_positions = KEY_POSITIONS[self.event_key.type]
        return res_key_positions
