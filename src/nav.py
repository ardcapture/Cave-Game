from src.utilities import DIRECTIONS_FOUR
from src.position import Position


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
    def __init__(self, GRID_SIZE: int, combined_positions: list[Position]) -> None:
        print("init Nav")

        self.GRID_SIZE = GRID_SIZE

        value: int = 0
        self.positionInt: PositionInt = dict.fromkeys(combined_positions, value)

        self.positionPositions: PositionPositions = dict.fromkeys(
            combined_positions, []
        )

        self.positionInt, self.positionPositions = self.set_navigation()

    #! variable renaming done:
    def get_adjacent_positions(self, center_position: Position):
        adjacent_positions: list[Position] = []

        for direction in DIRECTIONS_FOUR:
            x_offset, y_offset = (
                direction.x * self.GRID_SIZE,
                direction.y * self.GRID_SIZE,
            )
            adjacent_x, adjacent_y = (
                center_position.x + x_offset,
                center_position.y + y_offset,
            )
            adjacent_position = Position(adjacent_x, adjacent_y)
            adjacent_position = Position(adjacent_x, adjacent_y)

            if adjacent_position in self.positionInt:
                adjacent_positions.append(adjacent_position)

        return adjacent_positions

    def setPathName(self):
        # TODO: not sure where self.path_directions_list is coming from! How it is changing each loop!
        return PATHS_PATHSNAME[len(self.positions)]

    def set_navigation(self):
        for position in self.positionInt.keys():
            self.positions = self.get_adjacent_positions(position)
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
        self, current_positions: list[Position], updated_positions: list[Position]
    ):
        # """For Nav - currently used in controller."""

        run = True
        while run:
            if (
                self.positionInt[current_positions[-1]]
                <= self.positionInt[updated_positions[-1]]
                or not current_positions
            ):
                position_02: Position = max(
                    self.positionPositions[current_positions[-1]],
                    key=self.maxKey,
                )

                current_positions.append(position_02)
            if (
                self.positionInt[updated_positions[-1]]
                <= self.positionInt[current_positions[-1]]
                or not updated_positions
            ):
                position_02: Position = max(
                    self.positionPositions[updated_positions[-1]],
                    key=self.maxKey,
                )

                updated_positions.append(position_02)
            if [i for i in current_positions if i in updated_positions]:
                current_positions.pop(-1)
                run = False
        updated_positions.reverse()
        current_positions.extend(updated_positions)

        return current_positions
