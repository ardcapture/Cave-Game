import pygame
from src.position import Position

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.level import Level


class TileGenerator:
    def __init__(
        self,
        level: "Level",
        y_start: int,
        adjust: int,
        surface: pygame.surface.Surface,
    ):
        self.grid_size = level.GRID_SIZE
        self.top_offset = level.top_offset
        self.width = level.WIDTH_GS

        self.adjust = adjust
        self.y_start = y_start
        self.y_stop = self.grid_size * (self.top_offset - self.adjust)
        self.surface = surface

    @property
    def positions(self):
        return (
            Position(x, y)
            for x in range(0, self.width, self.grid_size)
            for y in range(self.y_start, self.y_stop, self.grid_size)
        )
