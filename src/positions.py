from src.utilities import Position


class Positions:
    def __inti__(self, positions: list[Position]):
        self.positions = positions

    def filter_positions_above_height(self, positions: list[Position], height: float):
        filtered_positions = [position for position in positions if position.y > height]
        return filtered_positions
