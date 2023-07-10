from abc import ABC, abstractmethod

from pygame import Surface

from src.utilities import Position


class LevelObject(ABC):
    def __init__(self, rect, position: Position) -> None:
        self._position: Position = position
        self.rect = rect

    @property
    def position(self) -> Position:
        return self._position

    @position.setter
    def position(self, position: Position):
        self._position = position

    @abstractmethod
    def surface(self) -> Surface:
        pass
