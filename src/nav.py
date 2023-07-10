from typing import TYPE_CHECKING

from src.utilities import DIRECTIONS_FOUR, NavData, Position

if TYPE_CHECKING:
    from src.level import Level


class Nav:
    def __init__(self, level: "Level") -> None:
        print("init Nav")

        iterable = level.paths + level.camp_positions
        value = "X"
        self.d_position_str: dict[Position, str] = dict.fromkeys(iterable, value)

        iterable = level.paths + level.camp_positions
        value = []
        self.d_position_list_position: dict[Position, list[Position]] = dict.fromkeys(
            iterable, value
        )

        self.d_position_str, self.d_position_list_position = self.set_navigation(level)

    def set_path_directions_list(self, level: "Level", position: Position):
        path_directions_list: list[Position] = []
        for direction in DIRECTIONS_FOUR:
            x = position.x + (direction.x * level.GRID_SIZE)
            y = position.y + (direction.y * level.GRID_SIZE)
            direction = Position(x, y)

            if direction in self.d_position_str:
                path_directions_list.append(direction)

        self.path_directions_list = path_directions_list

    def set_navigation(self, level: "Level"):
        # TODO needs fixing

        dict_position_NavData: dict[Position, NavData]
        iterable = level.paths + level.camp_positions
        value = NavData("X")
        dict_position_NavData = dict.fromkeys(iterable, value)

        # pprint(dict_position_NavData)

        #! ****************************

        iterable = level.paths + level.camp_positions
        value = int
        dict_position_int = dict.fromkeys(iterable, value)

        for position in self.d_position_str.keys():
            self.set_path_directions_list(level, position)

            #! set self.dict_position_str based on path directions_list
            if len(self.path_directions_list) == 1:
                self.d_position_str[position] = 1
                self.d_position_list_position[position] = self.path_directions_list

            elif len(self.path_directions_list) == 2:
                self.d_position_str[position] = "2"
                self.d_position_list_position[position] = self.path_directions_list
            elif len(self.path_directions_list) > 2:
                self.d_position_str[position] = "3 or 4"
                self.d_position_list_position[position] = self.path_directions_list

        #! for "1" items -  set the item next to them ready for increment (if "2" item")
        seq = [k for k, v in self.d_position_str.items() if v == 1]
        for position in seq:
            if self.d_position_str[self.d_position_list_position[position][0]] == "2":
                self.d_position_str[self.d_position_list_position[position][0]] = "#"

        run = True
        while run:
            #! if "for number" increment from previous number
            #! set the item next to them ready for increment (if "2" item")
            if any(k for k, v in self.d_position_str.items() if v == "#"):
                for k in [k for k, v in self.d_position_str.items() if v == "#"]:
                    for i in self.d_position_list_position[k]:
                        if isinstance(self.d_position_str[i], int):
                            result = self.d_position_str[i]
                        if self.d_position_str[i] == "2":
                            self.d_position_str[i] = "#"
                    self.d_position_str[k] = result + 1

            elif any(k for k, v in self.d_position_str.items() if v == "G"):
                result = 0
                for k in [k for k, v in self.d_position_str.items() if v == "G"]:
                    result_list02 = []
                    for i in self.d_position_list_position[k]:
                        if isinstance(self.d_position_str[i], int):
                            result_list02.append(self.d_position_str[i])
                        if isinstance(self.d_position_str[i], str):
                            self.d_position_str[i] = "#"
                    self.d_position_str[k] = sorted(result_list02)[-1] + 1

            elif any(k for k, v in self.d_position_str.items() if v == "3 or 4"):
                for k, v in self.d_position_str.items():
                    if v == "3 or 4":
                        result_list = []
                        for i in self.d_position_list_position[k]:
                            if isinstance(self.d_position_str[i], int):
                                result_list.append(i)
                                # print(f"{result_list=}")
                                if (
                                    len(result_list)
                                    == (len(self.d_position_list_position[k]) - 1)
                                    and self.d_position_str[k] == "3 or 4"
                                ):
                                    self.d_position_str[k] = "G"
            else:
                run = False

        # for key, value in dict_position_list_position.items():
        #     print(f"{key=}  {value=}")

        return self.d_position_str, self.d_position_list_position

    def set_route(
        self,
        level: "Level",
        position_01: "Position",
    ):
        """For Nav - currently used in controller."""

        position_02: Position

        route_list_A = [level.player_path_position]
        if position_01 in level.paths or position_01 in level.camp_positions:
            route_list_B = [position_01]
        else:
            route_list_B = [level.player_path_position]
        run = True
        while run:
            if (
                self.d_position_str[route_list_A[-1]]
                <= self.d_position_str[route_list_B[-1]]
                or not route_list_A
            ):
                position_02 = max(
                    self.d_position_list_position[route_list_A[-1]],
                    key=self.d_position_str.get,
                )
                route_list_A.append(position_02)
            if (
                self.d_position_str[route_list_B[-1]]
                <= self.d_position_str[route_list_A[-1]]
                or not route_list_B
            ):
                position_02 = max(
                    self.d_position_list_position[route_list_B[-1]],
                    key=self.d_position_str.get,
                )
                route_list_B.append(position_02)
            if [i for i in route_list_A if i in route_list_B]:
                route_list_A.pop(-1)
                run = False
        route_list_B.reverse()
        route_list_A.extend(route_list_B)
        return route_list_A
