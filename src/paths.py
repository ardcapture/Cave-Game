import random
from dataclasses import dataclass, field
from typing import Any
from utilities import debug_instance_variables, get_distance_in_direction
from constants import DIRECTIONS

# todo fix these types:
T_PathObj = Any


@dataclass
class Path_Data:
    path_start_position: tuple[int, int]
    path_finish_position: tuple[int, int]
    climb_positions: list[tuple[int, int]]
    paths: list[tuple[int, int]]
    camp_positions: list[tuple[int, int]]
    player_path_position: tuple[int, int]
    path_type: dict[tuple[int, int], str]
    path_directions: dict[tuple[int, int], str]


class Paths:
    def update_build(
        self,
        build_path_positions: list[tuple[int, int]],
        grid_size: int,
        top_offset: int,
        width: int,
        height: int,
    ) -> T_PathObj:

        poss_path_start_position = self.set_poss_path_start(
            build_path_positions, grid_size, top_offset, width
        )

        path_start_position = self.set_path_start_position(
            poss_path_start_position, grid_size
        )

        poss_path_finish = self.set_poss_path_finish(
            build_path_positions, grid_size, width, height
        )
        path_finish_position = self.set_path_finish_position(
            poss_path_finish, grid_size
        )

        if not path_start_position or not path_finish_position:
            return None

        camp_positions = self.set_camp_positions(path_start_position, grid_size, width)

        paths = self.set_paths(
            build_path_positions,
            path_start_position,
            path_finish_position,
        )

        # FOR NAV
        list_climb_positions = self.set_climb(paths, grid_size)

        # FOR NAV
        path_type, path_directions = self.set_navigation(
            paths, camp_positions, grid_size
        )

        # FOR NAV
        player_path_position = random.choice(camp_positions)

        path_obj = Path_Data(
            path_start_position=path_start_position,
            path_finish_position=path_start_position,
            climb_positions=list_climb_positions,
            paths=paths,
            camp_positions=camp_positions,
            player_path_position=player_path_position,
            path_type=path_type,
            path_directions=path_directions,
        )

        return path_obj

    def update_run(
        self,
        climb_positions: list[tuple[int, int]],
        player_path_position: tuple[int, int],
        path_climb_positions_visited: list[tuple[int, int]] = [],
    ):

        path_climb_positions_visited = self.update_player_climb_positions_visited(
            player_path_position, climb_positions, path_climb_positions_visited
        )

        debug_instance_variables(self)

        return path_climb_positions_visited

    def set_poss_path_start(
        self,
        past_positions: list[tuple[int, int]],
        grid_size: int,
        top_offset: int,
        width: int,
    ) -> list[tuple[int, int]]:
        return [
            p
            for p in past_positions
            if p[1] == grid_size * top_offset
            if p[0] < ((width - grid_size * 2) * (1 / 3))
        ]

    def set_path_start_position(
        self, poss_maze_start: list[tuple[int, int]], grid_size: int
    ) -> tuple[int, int]:
        if len(poss_maze_start) > 0:
            poss_maze_start = random.choice(poss_maze_start)
            return (poss_maze_start[0], poss_maze_start[1] - grid_size)
        else:
            return (-0, -0)

    def set_poss_path_finish(
        self,
        past_positions: list[tuple[int, int]],
        grid_size: int,
        width: int,
        height: int,
    ) -> list[tuple[int, int]]:
        return [
            p
            for p in past_positions
            if p[0] == width - (grid_size * 2)
            if p[1] > ((height - grid_size * 2) * (2 / 3))
        ]

    def set_path_finish_position(
        self, poss_maze_finish: list[tuple[int, int]], grid_size: int
    ) -> tuple[int, int]:
        if len(poss_maze_finish) > 0:
            poss_maze_finish = random.choice(poss_maze_finish)
            return (poss_maze_finish[0] + grid_size, poss_maze_finish[1])
        else:
            return (-0, -0)

        # TODO check if required
        # self.draw.draw(COLOURS["BLUE_VERY_LIGHT"], self.maze_finish_position[0], self.maze_finish_position[1])
        # else:
        #     # self.maze_finish = None

    def set_camp_positions(
        self, maze_start_position: tuple[int, int], grid_size: int, width: int
    ) -> list[tuple[int, int]]:
        return [
            (i, maze_start_position[1] - grid_size) for i in range(0, width, grid_size)
        ]

    def set_paths(
        self,
        build_positions: list[tuple[int, int]],
        maze_start_position: tuple[int, int],
        maze_finish_position: tuple[int, int],
    ) -> list[tuple[int, int]]:
        return build_positions + [maze_start_position, maze_finish_position]

    def set_climb(
        self, paths: list[tuple[int, int]], grid_size: int
    ) -> list[tuple[int, int]]:
        return [
            p
            for p in paths
            if get_distance_in_direction(p, "UP", grid_size) in paths
            or get_distance_in_direction(p, "DOWN", grid_size) in paths
        ]

    def set_navigation(
        self,
        paths: list[tuple[int, int]],
        camp_positions: list[tuple[int, int]],
        grid_size: int,
    ):
        path_type: dict[tuple[int, int], str] = dict.fromkeys(paths, "X")
        path_type.update(dict.fromkeys(camp_positions, "X"))

        path_directions_dict: dict[
            tuple[int, int], list[tuple[int, int]]
        ] = dict.fromkeys(paths, [])
        for p in path_type.keys():
            path_directions_list: list[tuple[int, int]] = []
            for d in DIRECTIONS:
                direction = (p[0] + (d[0] * grid_size), p[1] + (d[1] * grid_size))
                if direction in path_type:
                    path_directions_list.append(direction)
            if len(path_directions_list) == 1:
                path_type[p] = 1
                path_directions_dict[p] = path_directions_list
            elif len(path_directions_list) == 2:
                path_type[p] = "P"
                path_directions_dict[p] = path_directions_list
            elif len(path_directions_list) > 2:
                path_type[p] = "J"
                path_directions_dict[p] = path_directions_list
        for p in [k for k, v in path_type.items() if v == 1]:
            if path_type[path_directions_dict[p][0]] == "P":
                path_type[path_directions_dict[p][0]] = "N"

        run = True
        while run:
            if any([k for k, v in path_type.items() if v == "N"]):
                for k in [k for k, v in path_type.items() if v == "N"]:
                    for i in path_directions_dict[k]:
                        if isinstance(path_type[i], int):
                            result = path_type[i]
                        if path_type[i] == "P":
                            path_type[i] = "N"
                    path_type[k] = result + 1
            elif any([k for k, v in path_type.items() if v == "G"]):
                for k in [k for k, v in path_type.items() if v == "G"]:
                    result = 0
                    result_list02 = []
                    for i in path_directions_dict[k]:
                        if isinstance(path_type[i], int):
                            result_list02.append(path_type[i])
                        if isinstance(path_type[i], str):
                            path_type[i] = "N"
                    path_type[k] = sorted(result_list02)[-1] + 1
            elif any([k for k, v in path_type.items() if v == "J"]):
                for k, v in path_type.items():
                    if v == "J":
                        result_list = []
                        for i in path_directions_dict[k]:
                            if isinstance(path_type[i], int):
                                result_list.append(i)
                                if len(result_list) == (
                                    len(path_directions_dict[k]) - 1
                                ):
                                    if path_type[k] == "J":
                                        path_type[k] = "G"
            else:
                run = False
        # print(f"{path_type=}")
        # print(f"{path_directions_dict=}")


        return path_type, path_directions_dict

        """For Nav - currently used in game run."""

    def update_player_climb_positions_visited(
        self,
        player_current_position: tuple[int, int],
        path_climb_positions: list[tuple[int, int]],
        path_climb_positions_visited: list[tuple[int, int]] = [],
    ) -> list[tuple[int, int]]:
        if (
            player_current_position in path_climb_positions
            and player_current_position not in path_climb_positions_visited
        ):
            return path_climb_positions_visited + [player_current_position]
        else:
            return path_climb_positions_visited
