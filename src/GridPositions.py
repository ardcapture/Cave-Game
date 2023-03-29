from src.utilities import Positions


class GridPositions:
    def __init__(self, items: Positions = None):
        self.value = 0
        self._items: list[Positions] = [] if items is None else items

    #! self._items - GET
    def __len__(self):
        return len(self._items)

    #! self._items - GET
    def __getitem__(self, slice: slice):
        return self._items[slice]

    #! self - SET
    def __setitem__(self, position: int, item: Positions, itemType: str = "Nope"):
        self._items[position] = item
        print(f"{itemType=}")

    #! self - SET
    def __add__(self, other):
        return GridPositions((list(self._items) + list(other)))

    #! self._items - GET
    def path_return(self, position: Positions) -> Positions:
        i = self._items.index(position)
        return self._items[i - 1]

    #! self._items - GET
    def is_build_finish(self, level_item: Positions) -> bool:
        check_len = len(self._items) > 2
        return not check_len or level_item != self._items[0]

    #! self._items - GET
    def get_all_positions_next(self, position: Positions):
        if position not in self._items:
            return self._items[-1]
