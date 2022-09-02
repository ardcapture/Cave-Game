DIRECTIONS: list[tuple[int, int]] = [(0, 1), (-1, 0), (1, 0), (0, -1)]

TILE_DIRECTIONS = {
    "T": (0, -1),
    "R": (1, 0),
    "B": (0, 1),
    "L": (-1, 0),
    "TR": (1, -1),
    "BR": (1, 1),
    "BL": (-1, 1),
    "TL": (-1, -1),
}

AROUND = [-1, 0, 1]