from . import utilities
from collections import defaultdict
from itertools import product
from src.GridPositions import GridPositions
from src.WaterFactory import WaterFactory
from src.lights import Lights  #! object used 1x
from src.nav import Nav
from src.positions import Positions
from src.utilities import DIRECTIONS_FOUR, Direction, Position, Color
from src.utilities import NoPositionFound, Position, Colors
import copy
import pygame
import random


LevelStates = ["01_Title", "02_Settings", "03_Build", "04_Play"]
game_keys = "K_BACKQUOTE"

BLACK = Color(0, 0, 0)


KEY_DOWN = pygame.K_DOWN
KEY_LEFT = pygame.K_LEFT
KEY_UP = pygame.K_UP
KEY_RIGHT = pygame.K_RIGHT
KEY_BACKQUOTE = pygame.K_BACKQUOTE


class Level:
    _climb_positions_visited = Positions()

    _lights_state: bool = False
    # selected = False
    # reset_02 = False

    top_offset: int = 5

    GRID_SIZE = 32
    GRID_SIZE_2D = (GRID_SIZE, GRID_SIZE)
    WIDTH_GS = (GRID_SIZE * 2) + (GRID_SIZE * 35)
    HEIGHT_GS = (GRID_SIZE * 2) + (GRID_SIZE * 22)

    # previous_position: Position = Position(0, 0)

    route = Positions()

    _return_positions: list[Position] = []  #! X2
    _list_position_jump: list[Position] = []
    _build_path_positions: list[Position] = []

    def __init__(self):
        self._reduced_positions = self._set_reduced_positions()

        self._current_position: Position = random.choice(self._reduced_positions)

        self._grid_positions: GridPositions = GridPositions()

        while self._grid_positions.is_building_complete(self._current_position):
            self._grid_positions.addPosition(self._current_position)

            self._position_next = self._get_position_next()

            self._list_position_jump.append(self._position_break_current)

            self._current_position = self._position_next

            self._build_path_positions = (
                self._grid_positions.returnAllPositions() + self._list_position_jump
            )

        try:
            self._set_start_position()
            self._set_path_finish_position()
        except NoPositionFound:
            print("No Position Found")
            self.__init__()
            return

        # ! PUBLIC
        # self.paths = self._build_path_positions + [
        #     self.path_start_position,
        #     self.path_finish_position,
        # ]

        paths_positions = self._build_path_positions + [
            self.path_start_position,
            self.path_finish_position,
        ]

        self.paths = Positions(paths_positions)

        # ! PUBLIC
        self.camp_positions = self._set_camp_positions()

        # ! PUBLIC
        self.player_path_position: Position = random.choice(self.camp_positions)

        self._combined_positions = self.paths.add_position(self.camp_positions)

        # ! PUBLIC
        self.nav = Nav(self.GRID_SIZE, self._combined_positions)

        # ! PUBLIC
        self.list_climb_positions = self.paths.positions_vertical_in_distance(
            self.GRID_SIZE
        )

        # ! PUBLIC
        self.lights = Lights()

        # ! PUBLIC
        self.water = WaterFactory(self)

    @property
    def _position_break_current(self) -> Position:
        x = self._current_position.x + self._direction_current.x
        y = self._current_position.y + self._direction_current.y
        return Position(x, y)

    @property
    def _direction_current(self) -> Position:
        x = (self._position_next.x - self._current_position.x) // 2
        y = (self._position_next.y - self._current_position.y) // 2
        return Position(x, y)

    @property
    def _isNewClimbPosition(self):
        a = self.player_path_position
        b = self.list_climb_positions
        c = self._climb_positions_visited
        return a in b and a not in c

    def set_character_light_positions(self):
        self.lights.characterLightPositions = defaultdict(lambda: Colors.BLACK.value)

        self.lights.characterLightPositions = self.update_character_light_positions()

    def update_character_light_positions(
        self,
    ) -> dict[Position, Color]:
        characterLightPositions = copy.copy(self.lights.characterLightPositions)

        directions = [self.GRID_SIZE, -self.GRID_SIZE]

        for i in directions:
            possLightPosition = self.player_path_position
            brightness = 0
            run = True
            while run:
                if possLightPosition in self.paths.positions:
                    characterLightPositions[
                        possLightPosition
                    ] = self.lights.brightness_list[brightness]
                    possLightPosition = Position(
                        possLightPosition.x + i, possLightPosition.y
                    )

                    if brightness < len(self.lights.brightness_list) - 1:
                        brightness += 1
                else:
                    run = False
        for i in directions:
            possLightPosition = self.player_path_position
            brightness = 0
            run = True
            while run:
                if possLightPosition in self.paths.positions:
                    characterLightPositions[
                        possLightPosition
                    ] = self.lights.brightness_list[brightness]
                    possLightPosition = Position(
                        possLightPosition.y, possLightPosition.y + i
                    )
                    if brightness < len(self.lights.brightness_list) - 1:
                        brightness += 1
                else:
                    run = False
        characterLightPositions[self.player_path_position] = Colors.BLACK.value
        return characterLightPositions

    # def set_sun_light_positions(self):
    #     positions =

    #     self.lights.sun_light_positions = self.get_sunlight_positions()

    def get_sunlight_positions(self) -> dict[Position, Color]:
        sunlight_positions: defaultdict[Position, Color] = defaultdict(
            lambda: Colors.BLACK.value
        )

        for position in [
            self.path_start_position,
            self.path_finish_position,
        ]:
            brightness_index = 1

            while True:
                if not position in self.paths.positions:
                    break
                sunlight_positions[position] = self.lights.brightness_list[
                    brightness_index
                ]
                position = (
                    position[0],
                    position[1] + self.GRID_SIZE,
                )
                if brightness_index < len(self.lights.brightness_list) - 1:
                    brightness_index += 1

                else:
                    break

        return dict(sunlight_positions)

    def set_visited_climb_positions(self) -> None:
        if self._isNewClimbPosition:
            self._climb_positions_visited.append(self.player_path_position)

    def set_route_positions(
        self,
        new_position: Position,
        other_positions: list[Position],
    ) -> list[Position]:
        if new_position in self.paths.positions or new_position in other_positions:
            updated_positions = [new_position]
        else:
            updated_positions = [self.player_path_position]
        return updated_positions

    # TODO under __init__
    def _set_path_finish_position(self):
        poss_path_finish = self._set_poss_path_finish()

        if len(poss_path_finish) == 0:
            raise NoPositionFound

        poss_maze_finish = random.choice(poss_path_finish)
        self.path_finish_position = Position(
            poss_maze_finish[0] + self.GRID_SIZE, poss_maze_finish[1]
        )

    # TODO under __init__
    def _set_camp_positions(self) -> list[Position]:
        camp_y_position = self.path_start_position.y - self.GRID_SIZE
        grid_start = 0
        grid_end = self.WIDTH_GS
        grid_step = self.GRID_SIZE
        grid_range = range(grid_start, grid_end, grid_step)
        return [Position(x, camp_y_position) for x in grid_range]

    # ! GROUP: _set_reduced_positions
    # TODO under __init__
    def _set_reduced_positions(self) -> list[Position]:
        grid_positions = self._generate_grid_positions()
        num_removals: int = len(grid_positions) // 3

        for _ in range(num_removals):
            random_position: Position = random.choice(grid_positions)
            grid_positions.remove(random_position)
        return grid_positions

    # TODO under _set_reduced_positions
    def _generate_grid_positions(self) -> list[Position]:
        grid_ranges = product(self._range_x(), self._range_y())
        positions = [Position(x, y) for x, y in grid_ranges]
        return positions

    # TODO under _set_grid_positions
    def _range_x(self) -> list[int]:
        start = self.GRID_SIZE
        stop = self.WIDTH_GS
        return self._list_from_range(start, stop)

    # TODO under _set_grid_positions
    def _range_y(self) -> list[int]:
        start = self.GRID_SIZE * self.top_offset
        stop = self.HEIGHT_GS - (self.GRID_SIZE * 2)
        return self._list_from_range(start, stop)

    # TODO under _range_x
    # TODO under _range_y
    def _list_from_range(self, start: int, stop: int):
        range_x_step = self.GRID_SIZE * 2
        res_range = range(start, stop, range_x_step)
        return list(res_range)

    # ! END GROUP: _set_reduced_positions

    # ! GROUP: _set_poss_path_start
    # TODO under __init__
    def _set_poss_path_start(self) -> list[Position]:
        return [
            position
            for position in self._build_path_positions
            if self._is_start_position(position)
        ]

    #  TODO under _set_poss_path_start
    def _is_start_position(self, position: "Position") -> bool:
        return position.y == self.GRID_SIZE * self.top_offset and position.x < (
            (self.WIDTH_GS - self.GRID_SIZE * 2) * (1 / 3)
        )

    # ! END GROUP: _set_poss_path_start

    # TODO under __init__
    def _set_start_position(self):
        poss_path_start_position = self._set_poss_path_start()

        if len(poss_path_start_position) == 0:
            # self.path_start_position = Position(-1, -1)
            raise NoPositionFound

        pos_list = random.choice(poss_path_start_position)
        self.path_start_position = Position(pos_list[0], pos_list[1] - self.GRID_SIZE)

    # ! GROUP: _set_poss_path_finish
    # TODO under __init__
    def _set_poss_path_finish(self) -> list[Position]:
        return [
            position
            for position in self._build_path_positions
            if self._is_finish_position(position)
        ]

    # TODO under _set_poss_path_finish
    def _is_finish_position(self, position: "Position"):
        return position.x == self.WIDTH_GS - (self.GRID_SIZE * 2) and position.y > (
            (self.HEIGHT_GS - self.GRID_SIZE * 2) * (2 / 3)
        )

    # ! END GROUP: _set_poss_path_finish

    # ! GROUP: _get_position_next
    def _get_position_next(self) -> Position:
        # TODO extract path_return variable??
        #! infante loop if as property!!??

        if len(self._set_get_next_positions()) > 1:
            res = self._get_position_next_random()

        elif len(self._set_get_next_positions()) == 1:
            res = self._set_get_next_positions()[0]

        else:
            res = self._grid_positions.get_positions_next_to(self._current_position)
            while res is None:
                self._update_return_positions()
                res = self._get_return_position_next()

        return res

    # TODO under _get_position_next
    def _get_return_position_next(self):
        return self._return_positions[-1]

    # ! END GROUP: _get_position_next

    # TODO under _get_position_next
    def _get_position_next_random(self) -> Position:
        population = self._set_get_next_positions()
        slice_end = len(self._set_get_next_positions())
        weights_slice = slice(slice_end)
        weights = [100, 100, 1, 1][weights_slice]
        return random.choices(population, weights, k=1)[0]

    # TODO under _get_position_next
    def _update_return_positions(self):
        self._return_positions.append(
            self._grid_positions.get_previous_position(self._current_position)
        )

    # TODO rename???
    # TODO under _get_position_next_random
    # TODO under _get_position_next
    def _set_get_next_positions(self) -> list[Position]:
        result_positions: list[Position] = []

        for data in self._get_res_sample():
            position_poss: Position = self._get_position_poss(data)
            is_in_reduced = position_poss in self._reduced_positions
            is_not_in_grid = (
                position_poss not in self._grid_positions.returnAllPositions()
            )

            if is_in_reduced and is_not_in_grid:
                result_positions.append(position_poss)

        return result_positions

    # TODO under _set_get_next_positions
    def _get_res_sample(self):
        return random.sample(DIRECTIONS_FOUR, len(DIRECTIONS_FOUR))

    # TODO under _set_get_next_positions
    def _get_position_poss(self, direction: Direction) -> Position:
        x = self._current_position.x + (direction.x * self.GRID_SIZE * 2)
        y = self._current_position.y + (direction.y * self.GRID_SIZE * 2)
        return Position(x, y)
