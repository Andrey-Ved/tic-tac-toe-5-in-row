from abc import ABC
from dataclasses import dataclass

from game.core.schemas import CellValue, GameField, CellPosition  # noqa


class Template(str):
    def __new__(cls, string: str):
        valid_chars = ('x', '0', '1')

        if any(char not in valid_chars for char in string):
            raise TypeError('String must contain characters only: %s', valid_chars)

        return super().__new__(cls, string)


@dataclass
class CellPositionWeight:
    position: CellPosition
    weight: int


@dataclass
class Settings(ABC):
    templates: dict[Template, int]
