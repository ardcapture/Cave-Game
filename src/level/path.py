from dataclasses import dataclass
import random
from typing import TYPE_CHECKING

from src import utilities
from src.utilities import DIRECTIONS_FOUR, Position

if TYPE_CHECKING:
    from src.level import Level


class Path:
    reset = False

    def update_build(self, level: "Level"):

        self.poss_path_start_position = self.set_poss_path_start(level)
        self.path_start_position = self.set_path_start_position(level)
        self.poss_path_finish = self.set_poss_path_finish(level)
        self.path_finish_position = self.set_path_finish_position(level)

        if self.path_start_position == (-1, -1) or self.path_finish_position == (
            -1,
            -1,
        ):
            self.reset = True
            return

        self.camp_positions = self.set_camp_positions(level)
        self.paths = self.set_paths(level)

        # FOR NAV
        self.list_climb_positions = self.set_climb(level)
        self.dict_position_str, self.dict_position_list_position = self.set_navigation(level)
        self.player_path_position = random.choice(self.camp_positions)

    def path_directions_dict_to_class(self, my_dict):

        for key in my_dict:
            setattr(self, key, my_dict[key])

    def update_run(
        self,
        climb_positions: list[Position],
        player_path_position: Position,
        path_climb_positions_visited: list[Position] = [],
    ):

        path_climb_positions_visited = self.update_player_climb_positions_visited(
            player_path_position, climb_positions, path_climb_positions_visited
        )

        return path_climb_positions_visited

    def set_poss_path_start(self, level: "Level") -> list[Position]:

        return [
            p
            for p in level.build_path_positions
            if p.y == level.GRID_SIZE * level.top_offset
            if p.x < ((level.WIDTH_GS - level.GRID_SIZE * 2) * (1 / 3))
        ]

    def set_poss_path_finish(self, level: "Level") -> list[Position]:
        return [
            p
            for p in level.build_path_positions
            if p[0] == level.WIDTH_GS - (level.GRID_SIZE * 2)
            if p[1] > ((level.HEIGHT_GS - level.GRID_SIZE * 2) * (2 / 3))
        ]

    def set_path_start_position(self, level: "Level") -> Position:
        if len(self.poss_path_start_position) > 0:
            pos_list = random.choice(self.poss_path_start_position)
            return Position(pos_list[0], pos_list[1] - level.GRID_SIZE)
        else:
            return Position(-1, -1)

    def set_path_finish_position(self, level: "Level") -> Position:
        if len(self.poss_path_finish) > 0:
            poss_maze_finish = random.choice(self.poss_path_finish)
            return Position(poss_maze_finish[0] + level.GRID_SIZE, poss_maze_finish[1])
        else:
            return Position(-1, -1)

    def set_camp_positions(self, level: "Level") -> list[Position]:
        y = self.path_start_position.y - level.GRID_SIZE
        start = 0
        stop = level.WIDTH_GS
        step = level.GRID_SIZE
        seq = range(start, stop, step)
        return [Position(x, y) for x in seq]

    def set_paths(self, level: "Level") -> list[Position]:
        return level.build_path_positions + [
            self.path_start_position,
            self.path_finish_position,
        ]

    def set_climb(self, level: "Level") -> list[Position]:
        return [
            p
            for p in self.paths
            if utilities.get_distance_in_direction(p, "UP", level.GRID_SIZE)
            in self.paths
            or utilities.get_distance_in_direction(p, "DOWN", level.GRID_SIZE)
            in self.paths
        ]

    def set_navigation(self, level: "Level"):

        iterable = self.paths + self.camp_positions
        value = "X"
        dict_position_str = dict.fromkeys(iterable, value)

        iterable = self.paths + self.camp_positions
        value = []
        dict_position_list_position = dict.fromkeys(iterable, value)

        iterable = self.paths + self.camp_positions
        value = int
        dict_position_int = dict.fromkeys(iterable, value)

        for position in dict_position_str.keys():
            path_directions_list: list[Position] = []

            for direction in DIRECTIONS_FOUR:
                x = position.x + (direction.x * level.GRID_SIZE)
                y = position.y + (direction.y * level.GRID_SIZE)
                direction = Position(x, y)

                if direction in dict_position_str:

                    path_directions_list.append(direction)

            # set path to 1
            if len(path_directions_list) == 1:
                dict_position_str[position] = 1

                dict_position_list_position[position] = path_directions_list

            elif len(path_directions_list) == 2:
                dict_position_str[position] = "P"
                dict_position_list_position[position] = path_directions_list
            elif len(path_directions_list) > 2:
                dict_position_str[position] = "J"

                dict_position_list_position[position] = path_directions_list

        for position in [k for k, v in dict_position_str.items() if v == 1]:
            if dict_position_str[dict_position_list_position[position][0]] == "P":
                dict_position_str[dict_position_list_position[position][0]] = "N"

        run = True
        while run:
            if any([k for k, v in dict_position_str.items() if v == "N"]):
                for k in [k for k, v in dict_position_str.items() if v == "N"]:
                    for i in dict_position_list_position[k]:
                        if isinstance(dict_position_str[i], int):
                            result = dict_position_str[i]
                        if dict_position_str[i] == "P":
                            dict_position_str[i] = "N"
                    dict_position_str[k] = result + 1
            elif any([k for k, v in dict_position_str.items() if v == "G"]):
                for k in [k for k, v in dict_position_str.items() if v == "G"]:
                    result = 0
                    result_list02 = []
                    for i in dict_position_list_position[k]:
                        if isinstance(dict_position_str[i], int):
                            result_list02.append(dict_position_str[i])
                        if isinstance(dict_position_str[i], str):
                            dict_position_str[i] = "N"
                    dict_position_str[k] = sorted(result_list02)[-1] + 1
            elif any([k for k, v in dict_position_str.items() if v == "J"]):
                for k, v in dict_position_str.items():
                    if v == "J":
                        result_list = []
                        for i in dict_position_list_position[k]:
                            if isinstance(dict_position_str[i], int):
                                result_list.append(i)
                                if len(result_list) == (
                                    len(dict_position_list_position[k]) - 1
                                ):
                                    if dict_position_str[k] == "J":
                                        dict_position_str[k] = "G"
            else:
                run = False

        # for key, value in dict_position_list_position.items():
        #     print(f"{key=}  {value=}")

        return dict_position_str, dict_position_list_position

    def update_player_climb_positions_visited(
        self,
        player_current_position: Position,
        path_climb_positions: list[Position],
        path_climb_positions_visited: list[Position] = [],
    ) -> list[Position]:
        if (
            player_current_position in path_climb_positions
            and player_current_position not in path_climb_positions_visited
        ):
            return path_climb_positions_visited + [player_current_position]
        else:
            return path_climb_positions_visited
