import pygame


KEY_NONE = "KEYNONE"
KEY_DOWN = "KEYDOWN"
KEY_UP = "KEYUP"

K_NONE = "K_NONE"
K_DOWN = "K_DOWN"
K_LEFT = "K_LEFT"
K_UP = "K_UP"
K_RIGHT = "K_RIGHT"
K_BACKQUOTE = "K_BACKQUOTE"


PYGAME_KEY_DOWN = pygame.KEYDOWN
PYGAME_KEY_UP = pygame.KEYUP

PYGAME_K_DOWN = pygame.K_DOWN
PYGAME_K_LEFT = pygame.K_LEFT
PYGAME_K_UP = pygame.K_UP
PYGAME_K_RIGHT = pygame.K_RIGHT
PYGAME_K_BACKQUOTE = pygame.K_BACKQUOTE


KEY_POSITIONS: dict[int, str] = {
    PYGAME_KEY_DOWN: KEY_DOWN,
    PYGAME_KEY_UP: KEY_UP,
}


KEYBOARD_KEY = K_NONE

KEYBOARD_EVENT = {
    PYGAME_K_DOWN: K_DOWN,
    PYGAME_K_LEFT: K_LEFT,
    PYGAME_K_UP: K_UP,
    PYGAME_K_RIGHT: K_RIGHT,
    PYGAME_K_BACKQUOTE: K_BACKQUOTE,
}


class Keyboard:
    def __init__(self):
        self.set_position_keys = ("K_LEFT", "K_RIGHT", "K_UP", "K_DOWN")

    def update(self, view):
        self.events = view.window_events

        return self.event_keyboard

    @property
    def event_keyboard(self):
        if self.keydown:
            if self.keydown[1] in self.set_position_keys:
                return self.keydown[1]

    @property
    def event_key(self):
        try:
            res = next(e for e in self.events if e.type in KEY_POSITIONS)
            return res
        except StopIteration:
            return None

    @property
    def keyboard_state(self):
        if not self.event_key:
            return

        res_key_positions = KEY_POSITIONS[self.event_key.type]
        return res_key_positions

    @property
    def keydown(self):
        for e in self.events:
            if e.type == PYGAME_KEY_DOWN:
                return ("KEYDOWN", KEYBOARD_EVENT.get(e.key, False))

    @property
    def keyup(self):
        for e in self.events:
            if e.type == PYGAME_KEY_UP:
                return ("KEYUP", KEYBOARD_EVENT.get(e.key, False))
