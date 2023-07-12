from typing import TYPE_CHECKING

from src.utilities import DIRECTIONS_FOUR, Position

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

PATHS_PATHSNAME = {
    1: 1,
    2: PATH,
    3: T_JUNCTION,
    4: X_JUNCTION,
}


class Nav:
    def __init__(self, level: "Level") -> None:
        print("init Nav")

        iterable = level.paths + level.camp_positions
        value: int = 0
        self.positionInt: PositionInt = dict.fromkeys(iterable, value)

        iterable = level.paths + level.camp_positions
        self.positionPositions: PositionPositions = dict.fromkeys(iterable, [])

        self.positionInt, self.positionPositions = self.set_navigation(level)

    def set_path_directions_list(self, level: "Level", position: Position):
        path_directions_list: list[Position] = []
        for direction in DIRECTIONS_FOUR:
            x = position.x + (direction.x * level.GRID_SIZE)
            y = position.y + (direction.y * level.GRID_SIZE)
            direction = Position(x, y)

            if direction in self.positionInt:
                path_directions_list.append(direction)

        return path_directions_list

    def setPathName(self):
        # TODO: not sure where self.path_directions_list is coming from! How it is changing each loop!
        return PATHS_PATHSNAME[len(self.positions)]

    def set_navigation(self, level: "Level"):
        for position in self.positionInt.keys():
            self.positions = self.set_path_directions_list(level, position)
            self.positionInt[position] = self.setPathName()
            self.positionPositions[position] = self.positions

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
                result = 0
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

    def maxKey(self, x: Position) -> int:
        return self.positionInt.get(x, 0)

    def set_route(
        self,
        level: "Level",
        position_01: "Position",
    ):
        """For Nav - currently used in controller."""

        positionsA = [level.player_path_position]
        if position_01 in level.paths or position_01 in level.camp_positions:
            positionsB = [position_01]
        else:
            positionsB = [level.player_path_position]

        run = True
        while run:
            if (
                self.positionInt[positionsA[-1]] <= self.positionInt[positionsB[-1]]
                or not positionsA
            ):
                position_02: Position = max(
                    self.positionPositions[positionsA[-1]],
                    key=self.maxKey,
                )

                positionsA.append(position_02)
            if (
                self.positionInt[positionsB[-1]] <= self.positionInt[positionsA[-1]]
                or not positionsB
            ):
                position_02: Position = max(
                    self.positionPositions[positionsB[-1]],
                    key=self.maxKey,
                )

                positionsB.append(position_02)
            if [i for i in positionsA if i in positionsB]:
                positionsA.pop(-1)
                run = False
        positionsB.reverse()
        positionsA.extend(positionsB)

        return positionsA
