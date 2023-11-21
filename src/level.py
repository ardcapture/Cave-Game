import random
import copy

from itertools import product
from typing import TYPE_CHECKING

import pygame

from src.lights import Lights  #! object used 1x
from src.nav import Nav
from src.utilities import NoPositionFound, Position
from src.WaterFactory import WaterFactory
from src.GridPositions import GridPositions

from . import utilities

from src.utilities import DIRECTIONS_FOUR, Direction, Position, Color

if TYPE_CHECKING:
    from window import Window


LevelStates = ["01_Title", "02_Settings", "03_Build", "04_Play"]
game_keys = "K_BACKQUOTE"

BLACK = Color(0, 0, 0)


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

    return_positions: list[Position] = []  #! X2
    list_position_jump: list[Position] = []
    build_path_positions: list[Position] = []

    def __init__(self):
        self._set_grid_positions()

        self.reduced_positions = utilities.set_reduced_positions(self.grid_positions)

        self.current_position: Position = random.choice(self.reduced_positions)

        self.grid_positions: GridPositions = GridPositions()

        while self.grid_positions.is_building_complete(self.current_position):
            self.grid_positions.addPosition(self.current_position)

            self.set_position_next()

            self.list_position_jump.append(self.position_break_current)

            self.current_position = self.position_next

            self.build_path_positions = (
                self.grid_positions.returnAllPositions() + self.list_position_jump
            )

        self.set_poss_path_start()
        self.set_poss_path_finish()

        try:
            self.set_start_position()
            self.set_path_finish_position()
        except NoPositionFound:
            print("No Position Found")
            self.__init__()
            return

        self.paths = self.build_path_positions + [
            self.path_start_position,
            self.path_finish_position,
        ]

        self.set_camp_positions()
        self.player_path_position: Position = random.choice(self.camp_positions)
        self.combined_positions = self.paths + self.camp_positions

        self.nav = Nav(self.GRID_SIZE, self.combined_positions)

        self._set_climb_positions()

        self.lights = Lights(self.GRID_SIZE)
        self.water = WaterFactory(self, self.nav)

    #! tuples
    @property
    def position_break_current(self) -> Position:
        x = self.current_position.x + self.direction_current.x
        y = self.current_position.y + self.direction_current.y
        return Position(x, y)

    @property
    def direction_current(self) -> Position:
        x = (self.position_next.x - self.current_position.x) // 2
        y = (self.position_next.y - self.current_position.y) // 2
        return Position(x, y)

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
        grid_height = self.HEIGHT_GS - self.GRID_SIZE * 2
        water_level = grid_height * (2 / 3)
        return water_level

    #! list from functions
    def set_position_next(self) -> None:
        # TODO extract path_return variable??
        #! infante loop if as property!!??

        if len(self.set_get_next_positions()) > 1:
            res = self.position_next_random()

        elif len(self.set_get_next_positions()) == 1:
            res = self.set_get_next_positions()[0]

        else:
            res = self.grid_positions.get_positions_next_to(self.current_position)
            while res is None:
                self.set_return_positions()
                res = self.get_return_position_next()

        self.position_next: Position = res

    #! return_position - list
    def get_return_position_next(self):
        return self.return_positions[-1]

    #! all_positions - list
    #! reduced_positions - list
    #! RETURNS LIST
    def set_get_next_positions(self) -> list[Position]:
        result_positions: list[Position] = []

        for data in self.res_sample():
            position_poss: Position = self.get_position_poss(data)
            is_in_reduced = position_poss in self.reduced_positions
            is_not_in_grid = (
                position_poss not in self.grid_positions.returnAllPositions()
            )

            if is_in_reduced and is_not_in_grid:
                result_positions.append(position_poss)

        return result_positions

    def res_sample(self):
        return random.sample(DIRECTIONS_FOUR, len(DIRECTIONS_FOUR))

    #! current_position - tuple
    def get_position_poss(self, direction: Direction) -> Position:
        x = self.current_position.x + (direction.x * self.GRID_SIZE * 2)
        y = self.current_position.y + (direction.y * self.GRID_SIZE * 2)
        return Position(x, y)

    # Helper function
    def position_next_random(self) -> Position:
        population = self.set_get_next_positions()
        slice_end = len(self.set_get_next_positions())
        weights_slice = slice(slice_end)
        weights = [100, 100, 1, 1][weights_slice]
        return random.choices(population, weights, k=1)[0]

    # Helper function
    def set_return_positions(self):
        self.return_positions.append(
            self.grid_positions.get_previous_position(self.current_position)
        )

    def set_player_path_position(self, window: "Window") -> None:
        self.player_path_position = self.mouse_event_run(self.nav, window)
        self.player_path_position = self.get_player_path_position(
            window,
            Position(0, 0),
        )

    def set_character_light_positions(self):
        self.lights.characterLightPositions = dict.fromkeys(self.paths, BLACK)

        directions = [self.GRID_SIZE, -self.GRID_SIZE]
        self.lights.characterLightPositions = (
            self.lights.update_character_light_positions(
                self,
                directions,
            )
        )

    def set_sun_light_positions(self):
        start_finish_positions = [
            self.path_start_position,
            self.path_finish_position,
        ]

        self.lights.sun_light_positions = self.lights.get_positions_sun(
            self,
            start_finish_positions,
            self.paths,
        )

    def set_light_positions(self):
        self.lights.light_positions = dict.fromkeys(self.paths, BLACK)

    #! self.path_start_position - get
    #! self.camp_positions - set
    def set_camp_positions(self) -> None:
        camp_y_position = self.path_start_position.y - self.GRID_SIZE
        grid_start = 0
        grid_end = self.WIDTH_GS
        grid_step = self.GRID_SIZE
        grid_range = range(grid_start, grid_end, grid_step)
        self.camp_positions = [Position(x, camp_y_position) for x in grid_range]

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
    def set_poss_path_start(self) -> None:
        self.poss_path_start_position = [
            position
            for position in self.build_path_positions
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

    # Helper function
    def is_start_position(self, position: "Position") -> bool:
        return position.y == self.GRID_SIZE * self.top_offset and position.x < (
            (self.WIDTH_GS - self.GRID_SIZE * 2) * (1 / 3)
        )

    #! self.poss_path_finish - tuple
    def set_poss_path_finish(self) -> None:
        self.poss_path_finish = [
            position
            for position in self.build_path_positions
            if self.is_finish_position(position)
        ]

    # Helper function
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

    def set_route_positions(self, new_position: Position) -> list[Position]:
        if new_position in self.paths or new_position in self.camp_positions:
            updated_positions = [new_position]
        else:
            updated_positions = [self.player_path_position]
        return updated_positions

    #! self.paths
    #! self.camp_positions
    #! self.route
    #! self.player_path_position - tuple
    def mouse_event_run(self, nav: "Nav", window: "Window") -> Position:
        if not window.mouse_event_run:
            return Position(-1, -1)

        position = window.mouse_event_run
        position = utilities.position_to_grid_position(position, self.GRID_SIZE)

        if position not in self.paths or position not in self.camp_positions:
            current_positions = [self.player_path_position]
            updated_positions = self.set_route_positions(position)
            self.route = nav.set_route(current_positions, updated_positions)
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
