from src.level.build import Paths_Build
from src.utilities import Direction, Positions


grid_size = 32
width = 1184
top_offset = 5
height = 768

direction = Direction(x=1, y=0)

# res = Position(x=992, y=416)


paths_build = Paths_Build(grid_size, width, top_offset, height)


paths_build.position_current = Positions(x=1056, y=416)


res = paths_build.get_position_poss(direction)

print(f"{res=}")
