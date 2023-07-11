from src.utilities import Position


class GridPositions:
    nonePosition: Position = Position(-1, -1)

    def __init__(self, items: list[Position] = []):
        self.value = 0
        self._items: list[Position] = items

    #! self._items - GET
    def __len__(self):
        return len(self._items)

    #! self._items - GET
    def __getitem__(self, slice: slice) -> list[Position]:
        return self._items[slice]

    #! self - SET
    def __setitem__(self, position: int, item: Position, itemType: str = "Nope"):
        self._items[position] = item
        print(f"{itemType=}")

    # TODO - test before removing
    # def __add__(self, other: Position):
    #     res = list(self._items) + list(other)
    #     return GridPositions(res)

    def addPosition(self, position: Position):
        self._items.append(position)

    def returnAllPositions(self):
        return self._items

    #! self._items - GET
    def path_return(self, position: Position) -> Position:
        i = self._items.index(position)
        return self._items[i - 1]

    #! self._items - GET
    def is_build_finish(self, level_item: Position) -> bool:
        check_len = len(self._items) > 2
        return not check_len or level_item != self._items[0]

    #! self._items - GET
    def get_all_positions_next(self, position: Position):
        if position not in self._items:
            return self._items[-1]
