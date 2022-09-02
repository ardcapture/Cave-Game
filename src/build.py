import random

from typing import Any
from constants import DIRECTIONS

# todo type to fix
A = Any


class Build:
    def update(self, grid_size: int, width: int, top_offset: int, height: int):

        build_path_positions = self.set_build_positions(
            grid_size, width, top_offset, height
        )

        return build_path_positions

    def set_build_positions(
        self, grid_size: int, width: int, top_offset: int, height: int
    ) -> A:

        build_return_positions = []
        build_jump_positions = []
        build_positions = []

        build_grid = self.set_build_grid(grid_size, width, top_offset, height)
        self.grid = self.build_grid_remove_random(build_grid)

        build_current_position = random.choice(build_grid)

        while self.check_build_finish(build_positions, build_current_position):

            build_positions = self.update_build_past_positions(
                build_positions,
                build_current_position,
            )

            build_poss_next_positions = self.set_build_poss_next_positions(
                build_current_position, build_positions, build_grid, grid_size
            )

            build_next_position = self.set_build_next_position(
                build_current_position,
                build_positions,
                build_return_positions,
                build_poss_next_positions,
            )

            build_current_break_direction = self.set_build_current_break_direction(
                build_next_position,
                build_current_position,
            )

            self.build_current_break_position = self.set_build_current_break_position(
                build_current_position,
                build_current_break_direction,
            )

            build_jump_positions = self.update_build_jump_positions(
                build_jump_positions,
                self.build_current_break_position,
            )

            build_current_position = build_next_position

        return build_positions + build_jump_positions

    def build_grid_remove_random(self, grid: list[tuple[int, int]]):
        res_grid: list[tuple[int, int]] = grid
        for _ in range(len(res_grid) // 3):
            grid.remove(random.choice(res_grid))
        return res_grid

    def set_build_grid(
        self, grid_size: int, width: int, top_offset: int, height: int
    ) -> list[tuple[int, int]]:
        return [
            (x, y)
            for x in range(grid_size, width, grid_size * 2)
            for y in range(
                grid_size * top_offset, height - (grid_size * 2), grid_size * 2
            )
            if (x, y)
        ]

    def update_build_past_positions(
        self, past_positions: list[tuple[int, int]], current_position: tuple[int, int]
    ):
        res = past_positions + [current_position]
        return res

    def set_build_poss_next_positions(
        self,
        current_position: tuple[int, int],
        past_positions: list[tuple[int, int]],
        grid: list[tuple[int, int]],
        grid_size: int,
    ) -> list[tuple[int, int]]:
        return [
            self.set_poss_position(current_position, d, grid_size)
            for d in random.sample(DIRECTIONS, len(DIRECTIONS))
            if self.set_poss_position(current_position, d, grid_size) in grid
            and self.set_poss_position(current_position, d, grid_size)
            not in past_positions
        ]

    def update_build_jump_positions(
        self,
        path_jump_positions: list[tuple[int, int]],
        current_wall_break_position: tuple[int, int],
    ) -> list[tuple[int, int]]:
        return [*path_jump_positions, current_wall_break_position]

    # TODO remove path_return variable
    def set_build_next_position(
        self,
        current_position: tuple[int, int],
        past_positions: list[tuple[int, int]],
        path_return: list[tuple[int, int]],
        poss_position: list[tuple[int, int]],
    ) -> tuple[int, int]:
        if len(poss_position) > 1:
            res = random.choices(
                poss_position, k=1, weights=[100, 100, 1, 1][: len(poss_position)]
            )[0]
        elif len(poss_position) == 0:
            if current_position in past_positions:
                res = self.set_path_return(past_positions, current_position)
                path_return.append(res)
            else:
                res = past_positions[-1]
        elif len(poss_position) == 1:
            res = poss_position[0]

        return res

    def set_build_current_break_direction(
        self, next_position: tuple[int, int], current_position: tuple[int, int]
    ) -> tuple[int, int]:
        return (
            (next_position[0] - current_position[0]) // 2,
            (next_position[1] - current_position[1]) // 2,
        )

    def set_build_current_break_position(
        self,
        current_position: tuple[int, int],
        current_wall_break_direction: tuple[int, int],
    ) -> tuple[int, int]:
        return (
            current_position[0] + current_wall_break_direction[0],
            current_position[1] + current_wall_break_direction[1],
        )
        # self.list_wall_break_positions.append(result02)

    def check_build_finish(
        self, past_positions: list[tuple[int, int]], current_position: tuple[int, int]
    ) -> bool:
        if len(past_positions) > 2 and current_position == past_positions[0]:
            return False
        else:
            return True

    def set_poss_position(
        self,
        current_position: tuple[int, int],
        direction: tuple[int, int],
        grid_size: int,
    ) -> tuple[int, int]:
        return (
            current_position[0] + (direction[0] * grid_size * 2),
            current_position[1] + (direction[1] * grid_size * 2),
        )

    def set_path_return(
        self, past_positions: list[tuple[int, int]], current_position: tuple[int, int]
    ) -> tuple[int, int]:
        return past_positions[past_positions.index(current_position) - 1]
