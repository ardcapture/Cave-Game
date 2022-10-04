import copy
import random
from itertools import product
from typing import Any

from src.utilities import DIRECTIONS_FOUR
from src.utilities import Direction, Position

import pprint

# todo type to fix
A = Any


class Paths_Build:
    def __init__(self, grid_size: int, width_GS: int, top_offset: int, height_GS: int):

        self.grid_size = grid_size
        self.top_offset = top_offset
        self.height_GS = height_GS
        self.width_GS = width_GS

        self.list_position_return: list[Position] = []
        self.list_position_jump: list[Position] = []
        self.list_positions: list[Position] = []

        self.list_position_reduced = self.set_list_position_reduced()
        self.position_current = random.choice(self.list_position_reduced)

    def update(self):

        while self.check_build_finish:

            self.list_positions.append(self.position_current)

            self.position_next = self.set_position_next()

            self.list_position_jump.append(self.position_break_current)

            self.position_current = self.position_next

        return self.list_positions + self.list_position_jump

    #! uses random
    def set_list_position_reduced(self) -> list[Position]:
        res_grid = copy.copy(self.list_position_grid)
        res_len = len(res_grid)
        for _ in range(res_len // 3):
            res_grid.remove(random.choice(res_grid))
        return res_grid

    #! takes variable
    def get_position_poss(self, direction: Direction) -> Position:
        res_add_x = direction.x * self.grid_size * 2
        res_add_y = direction.y * self.grid_size * 2
        res = Position(
            self.position_current.x + (res_add_x),
            self.position_current.y + (res_add_y),
        )
        return res

    # TODO extract path_return variable??
    #! infante loop if as property!!??
    def set_position_next(self) -> Position:

        if len(self.list_position_next_random) > 1:
            return self.position_next_random

        elif len(self.list_position_next_random) == 1:
            return self.list_position_next_random[0]

        else:
            return self.check_next

    @property
    def list_position_grid(self) -> list[Position]:
        res_product = product(self.range_x, self.range_y)
        return [Position(x, y) for x, y in res_product]

    @property
    def range_x(self) -> list[int]:
        self.range_x_start = self.grid_size
        self.range_x_stop = self.width_GS
        self.range_x_step = self.grid_size * 2
        res_range = range(self.range_x_start, self.range_x_stop, self.range_x_step)
        return [x for x in res_range]

    @property
    def range_y(self) -> list[int]:
        self.range_y_start = self.grid_size * self.top_offset
        self.range_y_stop = self.height_GS - (self.grid_size * 2)
        self.range_y_step = self.grid_size * 2
        res_range = range(self.range_y_start, self.range_y_stop, self.range_y_step)
        return [y for y in res_range]

    @property
    def list_position_next_random(self) -> list[Position]:
        res_list: list[Position] = []
        res_sample = random.sample(DIRECTIONS_FOUR, len(DIRECTIONS_FOUR))

        for d in res_sample:
            res_get_position_poss = self.get_position_poss(d)
            res_in = res_get_position_poss in self.list_position_reduced
            res_not_in = res_get_position_poss not in self.list_positions

            if res_in and res_not_in:
                res_list.append(res_get_position_poss)

        return res_list

    @property
    def position_next_random(self) -> Position:
        population = self.list_position_next_random
        slice_end = len(self.list_position_next_random)
        weights_slice = slice(slice_end)
        weights = [100, 100, 1, 1][weights_slice]
        return random.choices(population, weights, k=1)[0]

    @property
    def check_next(self):
        if self.position_current in self.list_positions:
            self.list_position_return.append(self.path_return)
            return self.list_position_return[-1]
        else:
            return self.list_positions[-1]

    @property
    def direction_current(self) -> Position:
        x = (self.position_next.x - self.position_current.x) // 2
        y = (self.position_next.y - self.position_current.y) // 2
        return Position(x, y)

    @property
    def position_break_current(self) -> Position:
        x = self.position_current.x + self.direction_current.x
        y = self.position_current.y + self.direction_current.y
        return Position(x, y)

    @property
    def check_build_finish(self) -> bool:
        check_len = len(self.list_positions) > 2

        if check_len and self.position_current == self.list_positions[0]:
            return False
        else:
            return True

    @property
    def path_return(self) -> Position:
        res_index = self.list_positions.index(self.position_current)
        return self.list_positions[res_index - 1]
