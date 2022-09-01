from typing import Any


def debug_instance_variables(self: Any) -> None:
    print(f"* {self.__class__.__name__}.debug_instance_variables")

    for k in self.__dict__.keys():
        print(f"- {type(self).__name__}: {k}")


def get_distance_in_direction(
    position: tuple[int, int], direction: str, grid_size: int
) -> tuple[int, int]:
    if direction == "RIGHT":
        return (position[0] + grid_size, position[1])
    if direction == "LEFT":
        return (position[0] - grid_size, position[1])
    if direction == "DOWN":
        return (position[0], position[1] + grid_size)
    if direction == "UP":
        return (position[0], position[1] - grid_size)
    else:
        return (position[0], position[1])


def position_to_grid_position(pos: tuple[int, int], grid_size: int) -> tuple[int, int]:
    return tuple(map(lambda x: (x // grid_size) * grid_size, pos))


def get_list_difference(list01: list[Any], list02: list[Any]) -> list[Any]:
    return [x for x in list01 if x not in list02]
