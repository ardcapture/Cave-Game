from typing import TYPE_CHECKING

from src.utilities import DIRECTIONS_FOUR, NavData, Position

if TYPE_CHECKING:
    from src.level import Level

# TODO: types to classes
PositionInt = dict[Position, int]
PositionPositions = dict[Position, list[Position]]

# Constants:
PATH = -2
PATH_02 = -22
T_JUNCTION = -3
X_JUNCTION = -4


class Nav:
    def __init__(self, level: "Level") -> None:
        print("init Nav")

        iterable = level.paths + level.camp_positions
        value = 0
        self.positionInt: PositionInt = dict.fromkeys(iterable, value)

        iterable = level.paths + level.camp_positions
        value = []
        self.positionPositions: PositionPositions = dict.fromkeys(iterable, value)

        self.positionInt, self.positionPositions = self.set_navigation(level)

    def set_path_directions_list(self, level: "Level", position: Position):
        path_directions_list: list[Position] = []
        for direction in DIRECTIONS_FOUR:
            x = position.x + (direction.x * level.GRID_SIZE)
            y = position.y + (direction.y * level.GRID_SIZE)
            direction = Position(x, y)

            if direction in self.positionInt:
                path_directions_list.append(direction)

        self.path_directions_list = path_directions_list

    # def setPathsPathname(self, position: Position):
    #     PathsPathname = {
    #         1: 1,
    #         2: PATH,
    #         3: T_JUNCTION,
    #         4: X_JUNCTION,
    #     }

    #     if len(self.path_directions_list) == 1:
    #         self.positionInt[position] = PathsPathname[len(self.path_directions_list)]

    def set_navigation(self, level: "Level"):
        for position in self.positionInt.keys():
            self.set_path_directions_list(level, position)

            #! set self.dict_position_str based on path directions_list
            if len(self.path_directions_list) == 1:
                self.positionInt[position] = 1
                self.positionPositions[position] = self.path_directions_list

            elif len(self.path_directions_list) == 2:
                self.positionInt[position] = PATH
                self.positionPositions[position] = self.path_directions_list

            elif len(self.path_directions_list) == 3:
                self.positionInt[position] = T_JUNCTION
                self.positionPositions[position] = self.path_directions_list

            elif len(self.path_directions_list) == 4:
                self.positionInt[position] = X_JUNCTION
                self.positionPositions[position] = self.path_directions_list

        #! for "1" items -  set the item next to them ready for increment (if "-2" item")
        seq = [k for k, v in self.positionInt.items() if v == 1]
        for position in seq:
            if self.positionInt[self.positionPositions[position][0]] == PATH:
                self.positionInt[self.positionPositions[position][0]] = PATH_02

        run = True
        while run:
            #! if "for number" increment from previous number
            #! set the item next to them ready for increment (if "PATH" item")
            if any(k for k, v in self.positionInt.items() if v == PATH_02):
                for k in [k for k, v in self.positionInt.items() if v == PATH_02]:
                    for i in self.positionPositions[k]:
                        if self.positionInt[i] >= 1:
                            result = self.positionInt[i]

                        if self.positionInt[i] == PATH:
                            self.positionInt[i] = PATH_02

                    self.positionInt[k] = result + 1

            elif any(k for k, v in self.positionInt.items() if v == -5):
                # TODO: not sure if result is used!!:
                result = 0
                for k in [k for k, v in self.positionInt.items() if v == -5]:
                    positionInts: list[int] = []
                    for i in self.positionPositions[k]:
                        if self.positionInt[i] >= 1:
                            positionInts.append(self.positionInt[i])
                        if self.positionInt[i] <= -1:
                            self.positionInt[i] = PATH_02
                    self.positionInt[k] = sorted(positionInts)[-1] + 1

            elif any(
                k for k, v in self.positionInt.items() if v in {T_JUNCTION, X_JUNCTION}
            ):
                for k, v in self.positionInt.items():
                    if v in {T_JUNCTION, X_JUNCTION}:
                        positions: list[Position] = []
                        for i in self.positionPositions[k]:
                            if self.positionInt[i] >= 1:
                                positions.append(i)
                                if len(positions) == (
                                    len(self.positionPositions[k]) - 1
                                ) and self.positionInt[k] in {
                                    T_JUNCTION,
                                    X_JUNCTION,
                                }:
                                    self.positionInt[k] = -5
            else:
                run = False

        return self.positionInt, self.positionPositions

    def set_route(
        self,
        level: "Level",
        position_01: "Position",
    ):
        """For Nav - currently used in controller."""

        routeListA = [level.player_path_position]
        if position_01 in level.paths or position_01 in level.camp_positions:
            routeListB = [position_01]
        else:
            routeListB = [level.player_path_position]

        run = True
        while run:
            if (
                self.positionInt[routeListA[-1]] <= self.positionInt[routeListB[-1]]
                or not routeListA
            ):
                print(f"{self.positionPositions[routeListA[-1]]=}")
                position_02: Position = max(
                    self.positionPositions[routeListA[-1]],
                    # TODO: key might need turning back on -not sure what it is doing!
                    key=self.positionInt.get,
                )
                routeListA.append(position_02)
            if (
                self.positionInt[routeListB[-1]] <= self.positionInt[routeListA[-1]]
                or not routeListB
            ):
                position_02: Position = max(
                    self.positionPositions[routeListB[-1]],
                    # TODO: key might need turning back on -not sure what it is doing!
                    key=self.positionInt.get,
                )
                routeListB.append(position_02)
            if [i for i in routeListA if i in routeListB]:
                routeListA.pop(-1)
                run = False
        routeListB.reverse()
        routeListA.extend(routeListB)

        return routeListA
