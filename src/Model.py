from dataclasses import dataclass


@dataclass
class Water_Data:
    position: tuple


@dataclass
class Light_Data:
    surface: str = "LIGHT"
    to_surface: str = "WINDOW"
    font_size: int = 15
    color: tuple = (0, 0, 0)
    special_flags: str = "BLEND_RGB_ADD"
    position: tuple = None


@dataclass
class Path_Data:
    path_start_position: tuple
    path_finish_position: tuple
    list_climb_positions: list
    paths: list
    camp_positions: list
    player_path_position: tuple
    path_type: dict
    path_directions: dict
