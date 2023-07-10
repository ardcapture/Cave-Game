import random
from itertools import product
from typing import TYPE_CHECKING

import pygame

from src.build import Build
from src.lights import Lights
from src.nav import Nav
from src.utilities import NoPositionFound, Position
from src.WaterFactory import WaterFactory

from . import utilities

if TYPE_CHECKING:
    from window import Window


LevelStates = ["01_Title", "02_Settings", "03_Build", "04_Play"]
game_keys = "K_BACKQUOTE"


KEY_DOWN = pygame.K_DOWN
KEY_LEFT = pygame.K_LEFT
KEY_UP = pygame.K_UP
KEY_RIGHT = pygame.K_RIGHT
KEY_BACKQUOTE = pygame.K_BACKQUOTE


class Level:
    climb_positions_visited: list[Position] = []

    lights_state: bool = False
    selected = False
    reset_02 = False

    top_offset: int = 5

    GRID_SIZE = 32
    GRID_SIZE_2D = (GRID_SIZE, GRID_SIZE)
    WIDTH_GS = (GRID_SIZE * 2) + (GRID_SIZE * 35)
    HEIGHT_GS = (GRID_SIZE * 2) + (GRID_SIZE * 22)

    previous_position: Position = Position(0, 0)

    route: list["Position"] = []

    def __init__(self):
        self._set_grid_positions()

        self.build = Build(self)

        self.set_poss_path_start(self.build)
        self.set_poss_path_finish(self.build)

        try:
            self.set_start_position()
            self.set_path_finish_position()
        except NoPositionFound:
            print("No Position Found")
            self.__init__()
            return

        self.paths = self.build.build_path_positions + [
            self.path_start_position,
            self.path_finish_position,
        ]

        self.set_camp_positions()
        self.player_path_position = random.choice(self.camp_positions)

        self.nav = Nav(self)

        self._set_climb_positions()

        self.lights = Lights(self)
        self.water = WaterFactory(self, self.nav)

    #! self.player_path_position - set
    def update(self, window: "Window"):
        self.lights.update(self, self.nav)

        self.player_path_position = self.mouse_event_run(self.nav, window)

        self.player_path_position = self.get_player_path_position(
            window,
            Position(0, 0),
        )

        # self.path.player_path_position = player_path_position

    #! self.player_path_position - get
    #! self.list_climb_positions - get
    #! self.climb_positions_visited - get
    @property
    def isNewClimbPosition(self):
        a = self.player_path_position
        b = self.list_climb_positions
        c = self.climb_positions_visited
        return a in b and a not in c

    #! -
    @property
    def water_line(self) -> float:
        return (self.HEIGHT_GS - self.GRID_SIZE * 2) * (2 / 3)

    #! self.path_start_position - get
    #! self.camp_positions - set
    def set_camp_positions(self) -> None:
        y = self.path_start_position.y - self.GRID_SIZE
        start = 0
        stop = self.WIDTH_GS
        step = self.GRID_SIZE
        seq = range(start, stop, step)
        self.camp_positions = [Position(x, y) for x in seq]

    #! self.grid_positions - SET
    def _set_grid_positions(self) -> None:
        res_product = product(self._range_x(), self._range_y())
        self.grid_positions = [Position(x, y) for x, y in res_product]

    #! -
    def _range_x(self) -> list[int]:
        start = self.GRID_SIZE
        stop = self.WIDTH_GS
        return self._list_from_range(start, stop)

    #! -
    def _range_y(self) -> list[int]:
        start = self.GRID_SIZE * self.top_offset
        stop = self.HEIGHT_GS - (self.GRID_SIZE * 2)
        return self._list_from_range(start, stop)

    #! -
    def _list_from_range(self, start: int, stop: int):
        range_x_step = self.GRID_SIZE * 2
        res_range = range(start, stop, range_x_step)
        return list(res_range)

    #! self.list_climb_position - SET
    def _set_climb_positions(self) -> None:
        self.list_climb_positions = [
            position for position in self.paths if self._is_climb_position(position)
        ]

    #! self.paths - GET
    def _is_climb_position(self, position: "Position") -> bool:
        return (
            utilities.get_distance_in_direction(position, "UP", self.GRID_SIZE)
            in self.paths
            or utilities.get_distance_in_direction(position, "DOWN", self.GRID_SIZE)
            in self.paths
        )

    #! poss_path_start_position - SET
    def set_poss_path_start(self, build: "Build") -> None:
        self.poss_path_start_position = [
            position
            for position in build.build_path_positions
            if self.is_start_position(position)
        ]

    #! self.poss_path_start_position - GET
    #! self.path_start_position - SET
    def set_start_position(self):
        if len(self.poss_path_start_position) == 0:
            # self.path_start_position = Position(-1, -1)
            raise NoPositionFound

        pos_list = random.choice(self.poss_path_start_position)
        self.path_start_position = Position(pos_list[0], pos_list[1] - self.GRID_SIZE)

    #! -
    def is_start_position(self, position: "Position") -> bool:
        return position.y == self.GRID_SIZE * self.top_offset and position.x < (
            (self.WIDTH_GS - self.GRID_SIZE * 2) * (1 / 3)
        )

    #! self.poss_path_finish - tuple
    def set_poss_path_finish(self, build: "Build") -> None:
        self.poss_path_finish = [
            position
            for position in build.build_path_positions
            if self.is_finish_position(position)
        ]

    #! -
    def is_finish_position(self, position: "Position"):
        return position.x == self.WIDTH_GS - (self.GRID_SIZE * 2) and position.y > (
            (self.HEIGHT_GS - self.GRID_SIZE * 2) * (2 / 3)
        )

    #! self.poss_path_finish
    #! self.path_finish_position
    def set_path_finish_position(self):
        if len(self.poss_path_finish) == 0:
            # self.path_finish_position = Position(-1, -1)
            raise NoPositionFound

        poss_maze_finish = random.choice(self.poss_path_finish)
        self.path_finish_position = Position(
            poss_maze_finish[0] + self.GRID_SIZE, poss_maze_finish[1]
        )

    #! self.is_new_climb_position
    #! self.climb_positions_visited
    #! self.player_path_position - tuple
    def set_visited_climb_positions(self) -> None:
        if not self.isNewClimbPosition:
            return

        self.climb_positions_visited.append(self.player_path_position)

    #! self.paths
    #! self.camp_positions
    #! self.route
    #! self.player_path_position - tuple
    def mouse_event_run(self, nav: "Nav", window: "Window"):
        if not window.mouse_event_run:
            return

        position = window.mouse_event_run
        grid_size = self.GRID_SIZE
        position = utilities.position_to_grid_position(position, grid_size)

        if position not in self.paths or position not in self.camp_positions:
            self.route = nav.set_route(self, position)
            route_index = 0
            for i in self.route[route_index:]:  # TODO need breaking into steps
                self.player_path_position = self.get_player_path_position(window, i)
        return self.player_path_position

    #! self.player_path_position
    #! self.paths
    #! self.camp_positions
    def get_player_path_position(
        self, window: "Window", position: "Position"
    ) -> Position:
        x, y = self.player_path_position

        if position != Position(0, 0):
            x, y = position

        elif window.event_keyboard == KEY_LEFT:
            x -= self.GRID_SIZE
        elif window.event_keyboard == KEY_RIGHT:
            x += self.GRID_SIZE
        elif window.event_keyboard == KEY_UP:
            y -= self.GRID_SIZE
        elif window.event_keyboard == KEY_DOWN:
            y += self.GRID_SIZE

        if Position(x, y) in self.paths or Position(x, y) in self.camp_positions:
            return Position(x, y)

        else:
            return Position(0, 0)
