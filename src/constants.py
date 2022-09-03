DIRECTIONS: list[tuple[int, int]] = [(0, 1), (-1, 0), (1, 0), (0, -1)]

TILE_DIRECTIONS: dict[str, tuple[int, int]] = {
    "T": (0, -1),
    "R": (1, 0),
    "B": (0, 1),
    "L": (-1, 0),
    "TR": (1, -1),
    "BR": (1, 1),
    "BL": (-1, 1),
    "TL": (-1, -1),
}

AROUND: list[int] = [-1, 0, 1]

DUPLICATE_CHECKS: list[str] = [
    "TR",
    "BR",
    "TL",
    "BL",
]


COLORS: dict[str, tuple[int, int, int]] = {
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "BLACK_VERY_LIGHT": (210, 210, 210),
    "WHITE_4TH_4TH_4TH_4TH": (1, 1, 1),
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "BLUE_LIGHT": (125, 125, 255),
    "BLUE_VERY_LIGHT": (210, 210, 255),
}

IMAGE_TYPES: list[str] = ["T", "R", "B", "L", "TR", "BR", "BL", "TL"]


LIGHTING_TILE_ROTATE: dict[str, tuple[str, int]] = {
    "T": ("TOP_image", 0),
    "TR": ("TOP_R_image", 0),
    "L": ("TOP_image", 90),
    "TL": ("TOP_R_image", 90),
    "B": ("TOP_image", 180),
    "BL": ("TOP_R_image", 180),
    "R": ("TOP_image", 270),
    "BR": ("TOP_R_image", 270),
}
