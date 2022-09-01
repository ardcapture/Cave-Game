from dataclasses import dataclass


@dataclass
class Light_Data:
    surface: str = "LIGHT"
    to_surface: str = "WINDOW"
    font_size: int = 15
    color: tuple = (0, 0, 0)
    special_flags: str = "BLEND_RGB_ADD"
    position: tuple = None



