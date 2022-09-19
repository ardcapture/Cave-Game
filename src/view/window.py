from collections import defaultdict

import pygame

EventType = pygame.event.Event


KEYNONE = "KEYNONE"
KEYDOWN = "KEYDOWN"
KEYUP = "KEYUP"

K_NONE = "K_NONE"
K_DOWN = "K_DOWN"
K_LEFT = "K_LEFT"
K_UP = "K_UP"
K_RIGHT = "K_RIGHT"
K_BACKQUOTE = "K_BACKQUOTE"


# Pygame:
PYGAME_KEYDOWN = pygame.KEYDOWN
PYGAME_KEYUP = pygame.KEYUP

PYGAME_K_DOWN = pygame.K_DOWN
PYGAME_K_LEFT = pygame.K_LEFT
PYGAME_K_UP = pygame.K_UP
PYGAME_K_RIGHT = pygame.K_RIGHT
PYGAME_K_BACKQUOTE = pygame.K_BACKQUOTE


KEY_POSITIONS: dict[int, str] = {
    PYGAME_KEYDOWN: KEYDOWN,
    PYGAME_KEYUP: KEYUP,
}


class Window:
    def __init__(self, title: str, width: int, height: int, grid_size: int):

        self.width, self.height = list(
            map(lambda x: (grid_size * 2) + (grid_size * x), [width, height])
        )

        self.window_size_scaled = self.get_window_scale(
            self.width, self.height, scale=1
        )

        pygame.display.set_caption(title)
        self.window_surface = pygame.display.set_mode(
            size=(self.width * 1, self.height * 1), flags=0, depth=32
        )

        self.events = self.get_events()

    def update(self, parent):
        events = parent.events

        self.events = self.get_events()
        self.window_quit = self.get_window_quit(events)

        return self

    def get_window_scale(self, width, height, scale: int):
        return (width * scale, height * scale)

    def get_scaled_window_surface(self):
        res = pygame.transform.scale(self.window_surface, self.window_size_scaled)
        return res

        # draw window

    def set_window(self, surface):
        self.window_surface.blit(surface, (0, 0))

    def get_window_quit(self, events):
        for e in events:
            if e.type == pygame.QUIT:
                return True

    def get_events(self) -> list[EventType]:
        res_get = pygame.event.get()
        return res_get

    @staticmethod
    def close_window():
        pygame.quit()


class Keyboard:
    def __init__(self):

        self.keyboard_state = KEYNONE
        self.keyboard_key = K_NONE

        self.keyboard_events = {
            PYGAME_K_DOWN: K_DOWN,
            PYGAME_K_LEFT: K_LEFT,
            PYGAME_K_UP: K_UP,
            PYGAME_K_RIGHT: K_RIGHT,
            PYGAME_K_BACKQUOTE: K_BACKQUOTE,
        }

    def update(self, parent):
        self.events: list[EventType] = parent.events

        self.event_key = self.get_events_key(self.events)

        self.keyboard_state = self.key_position(self.event_key)

        self.keydown = self._get_keydown(self.events)
        self.keyup = self._get_keyup(self.events)

        return self

    def get_events_key(self, events: list[EventType]):
        # res_events = [e for e in events if e.type in KEY_POSITIONS]
        # res_iter = iter(res_events)
        try:
            res = next(e for e in events if e.type in KEY_POSITIONS)
            return res
        except StopIteration:
            return None

    # def get_event_key(self):

    def key_position(self, event):
        if not event:
            return

        res_key_positions = KEY_POSITIONS[event.type]
        # print(f"*******{res_key_positions=}")
        return res_key_positions

    def _get_keydown(self, events: list[EventType]):
        for e in events:
            if e.type == PYGAME_KEYDOWN:
                return ("KEYDOWN", self.keyboard_events.get(e.key, False))

    def _get_keyup(self, events: list[EventType]):
        for event in events:
            if event.type == PYGAME_KEYUP:
                return ("KEYUP", self.keyboard_events.get(event.key, False))
