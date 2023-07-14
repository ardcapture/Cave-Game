import copy
import random
from typing import TYPE_CHECKING

from src.gridPositions import GridPositions
from src.utilities import DIRECTIONS_FOUR, Direction, Position

if TYPE_CHECKING:
    from src.level import Level


class Build:
    return_positions: list[Position] = []  #! X2
    list_position_jump: list[Position] = []
    grid_positions: GridPositions = GridPositions()
    build_path_positions: list[Position] = []

    #! tuples
    @property
    def position_break_current(self) -> Position:
        x = self.current_position.x + self.direction_current.x
        y = self.current_position.y + self.direction_current.y
        return Position(x, y)

    #! tuples
    @property
    def direction_current(self) -> Position:
        x = (self.position_next.x - self.current_position.x) // 2
        y = (self.position_next.y - self.current_position.y) // 2
        return Position(x, y)

    def __init__(self, level: "Level"):
        print("init Paths_Build")

        self.set_reduced_positions(level)
        self.current_position: Position = random.choice(self.reduced_positions)

        while self.grid_positions.is_build_finish(self.current_position):
            self.grid_positions.addPosition(self.current_position)

            self.set_position_next(level)

            self.list_position_jump.append(self.position_break_current)

            self.current_position = self.position_next

            self.build_path_positions = (
                self.grid_positions.returnAllPositions() + self.list_position_jump
            )

    #! reduced_positions - list
    def set_reduced_positions(self, level: "Level") -> None:
        res_grid = copy.copy(level.grid_positions)
        res_len = len(res_grid)
        for _ in range(res_len // 3):
            res_grid.remove(random.choice(res_grid))
        self.reduced_positions = res_grid

    # TODO NEW CLASS?

    #! list from functions
    def set_position_next(self, level: "Level") -> None:
        # TODO extract path_return variable??
        #! infante loop if as property!!??

        if len(self.set_get_next_positions(level)) > 1:
            res = self.position_next_random(level)

        elif len(self.set_get_next_positions(level)) == 1:
            res = self.set_get_next_positions(level)[0]

        else:
            res = self.grid_positions.get_all_positions_next(self.current_position)
            while res is None:
                self.set_return_positions()
                res = self.get_return_position_next()

        self.position_next: Position = res

    def res_sample(self):
        return random.sample(DIRECTIONS_FOUR, len(DIRECTIONS_FOUR))

    #! all_positions - list
    #! reduced_positions - list
    #! RETURNS LIST
    def set_get_next_positions(self, level: "Level") -> list[Position]:
        res_list: list[Position] = []
        isNotIn: bool

        for d in self.res_sample():
            resGetPositionPoss: Position = self.get_position_poss(level, d)

            isIn = resGetPositionPoss in self.reduced_positions

            isNotIn = resGetPositionPoss not in self.grid_positions.returnAllPositions()

            if isIn and isNotIn:
                res_list.append(resGetPositionPoss)

        return res_list

    #! LIST FROM FUNCTION
    def position_next_random(self, level: "Level") -> Position:
        population = self.set_get_next_positions(level)
        slice_end = len(self.set_get_next_positions(level))
        weights_slice = slice(slice_end)
        weights = [100, 100, 1, 1][weights_slice]
        return random.choices(population, weights, k=1)[0]

    #! current_position - tuple
    def get_position_poss(self, level: "Level", direction: Direction) -> Position:
        x = self.current_position.x + (direction.x * level.GRID_SIZE * 2)
        y = self.current_position.y + (direction.y * level.GRID_SIZE * 2)
        return Position(x, y)

    #! return_positions - list
    def set_return_positions(self):
        self.return_positions.append(
            self.grid_positions.path_return(self.current_position)
        )

    #! return_position - list
    def get_return_position_next(self):
        return self.return_positions[-1]
