from abc import ABC, abstractmethod

from pygame import Surface

from src.utilities import Positions


class LevelObject(ABC):
    def __init__(self, rect, position: Positions) -> None:
        self._position: Positions = position
        self.rect = rect

    @property
    def position(self) -> Positions:
        return self._position

    @position.setter
    def position(self, position: Positions):
        self._position = position

    @abstractmethod
    def surface(self) -> Surface:
        pass
