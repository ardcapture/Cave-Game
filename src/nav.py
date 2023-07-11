from typing import TYPE_CHECKING

from src.utilities import DIRECTIONS_FOUR, NavData, Position

if TYPE_CHECKING:
    from src.level import Level


class Nav:
    def __init__(self, level: "Level") -> None:
        print("init Nav")

        iterable = level.paths + level.camp_positions
        value = "0"
        self.d_position_str: dict[Position, str] = dict.fromkeys(iterable, value)

        iterable = level.paths + level.camp_positions
        value = []
        self.Position_ListPosition: dict[Position, list[Position]] = dict.fromkeys(
            iterable, value
        )

        self.d_position_str, self.Position_ListPosition = self.set_navigation(level)

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

        # dict_position_NavData: dict[Position, NavData]
        # iterable = level.paths + level.camp_positions
        # value = NavData("X")
        # dict_position_NavData = dict.fromkeys(iterable, value)

        # pprint(dict_position_NavData)

        # ****************************

        # iterable = level.paths + level.camp_positions
        # value = int
        # dict_position_int = dict.fromkeys(iterable, value)

        # print(f"{self.d_position_str.values()=}")
        for position in self.d_position_str.keys():
            self.set_path_directions_list(level, position)

            #! set self.dict_position_str based on path directions_list
            if len(self.path_directions_list) == 1:
                self.d_position_str[position] = 1
                self.Position_ListPosition[position] = self.path_directions_list

            elif len(self.path_directions_list) == 2:
                self.d_position_str[position] = "-2"
                self.Position_ListPosition[position] = self.path_directions_list

            elif len(self.path_directions_list) == 3:
                self.d_position_str[position] = "-3"
                self.Position_ListPosition[position] = self.path_directions_list

            elif len(self.path_directions_list) == 4:
                self.d_position_str[position] = "-4"
                self.Position_ListPosition[position] = self.path_directions_list

        #! for "1" items -  set the item next to them ready for increment (if "-2" item")
        seq = [k for k, v in self.d_position_str.items() if v == 1]
        for position in seq:
            if self.d_position_str[self.Position_ListPosition[position][0]] == "-2":
                self.d_position_str[self.Position_ListPosition[position][0]] = "-22"

        run = True
        while run:
            #! if "for number" increment from previous number
            #! set the item next to them ready for increment (if "-2" item")
            if any(k for k, v in self.d_position_str.items() if v == "-22"):
                for k in [k for k, v in self.d_position_str.items() if v == "-22"]:
                    for i in self.Position_ListPosition[k]:
                        print(f"{self.d_position_str[i]=}")
                        if isinstance(int(self.d_position_str[i]), int):
                            if int(self.d_position_str[i]) >= 1:
                                result = self.d_position_str[i]
                        if self.d_position_str[i] == "-2":
                            self.d_position_str[i] = "-22"
                    self.d_position_str[k] = result + 1

            elif any(k for k, v in self.d_position_str.items() if v == "-5"):
                result = 0
                for k in [k for k, v in self.d_position_str.items() if v == "-5"]:
                    result_list02 = []
                    # print(f"{self.d_position_str=}")
                    for i in self.Position_ListPosition[k]:
                        # what are these numbers?!
                        # print(f"{self.d_position_str[i]=}")
                        if isinstance(int(self.d_position_str[i]), int):
                            # TODO TO REMOVE ABOVE CHECK WITH BELOW5
                            if int(int(self.d_position_str[i])) >= 1:
                                result_list02.append(self.d_position_str[i])
                        if isinstance(int(self.d_position_str[i]), int):
                            if int(self.d_position_str[i]) <= -1:
                                self.d_position_str[i] = "-22"
                    self.d_position_str[k] = sorted(result_list02)[-1] + 1

            elif any(k for k, v in self.d_position_str.items() if v in {"-3", "4"}):
                for k, v in self.d_position_str.items():
                    if v in {"-3", "4"}:
                        result_list = []
                        for i in self.Position_ListPosition[k]:
                            if isinstance(int(self.d_position_str[i]), int):
                                if int(self.d_position_str[i]) >= 1:
                                    result_list.append(i)
                                    if len(result_list) == (
                                        len(self.Position_ListPosition[k]) - 1
                                    ) and self.d_position_str[k] in {"-3", "4"}:
                                        self.d_position_str[k] = "-5"
            else:
                run = False

        # for key, value in dict_position_list_position.items():
        #     print(f"{key=}  {value=}")

        return self.d_position_str, self.Position_ListPosition

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
                    self.Position_ListPosition[route_list_A[-1]],
                    key=self.d_position_str.get,
                )
                route_list_A.append(position_02)
            if (
                self.d_position_str[route_list_B[-1]]
                <= self.d_position_str[route_list_A[-1]]
                or not route_list_B
            ):
                position_02 = max(
                    self.Position_ListPosition[route_list_B[-1]],
                    key=self.d_position_str.get,
                )
                route_list_B.append(position_02)
            if [i for i in route_list_A if i in route_list_B]:
                route_list_A.pop(-1)
                run = False
        route_list_B.reverse()
        route_list_A.extend(route_list_B)
        return route_list_A
