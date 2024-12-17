from abc import ABC
from dataclasses import dataclass
from enum import Enum


class CellValue(Enum):
    VOID: int = 0
    CROSS: int = 1
    ZERO: int = 2

    def __str__(self):
        return str(self.name)


@dataclass
class CellPosition:
    x: int
    y: int

    def __str__(self) -> str:
        return f"(x={self.x}, y={self.y})"

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self) -> int:
        return hash((self.x, self.y))


@dataclass
class ScreenPosition(CellPosition):
    pass


class _Field:
    def __init__(self, field_size):
        self._size = field_size

        self._field = {
            CellPosition(x=x, y=y): CellValue.VOID
            for x in range(field_size)
            for y in range(field_size)
        }

    def __setitem__(
            self,
            key: CellPosition,
            value: CellValue,
    ):
        if key not in self._field:
            raise TypeError('Adding field cells is prohibited')

        self._field[key] = value

    def __getitem__(
            self,
            key: CellPosition,
    ):
        return self._field[key]

    def __delitem__(
            self,
            key: CellPosition,
    ):
        raise TypeError('Deleting field cells is prohibited')

    def __contains__(
            self,
            key: CellPosition,
    ):
        return key in self._field

    def __str__(self) -> str:
        return f"{[f'{str(k)} - {str(v)}' for k, v in self._field.items()]}"


class GameField:
    def __init__(self, field_size):
        self._size = field_size
        self._cells = _Field(field_size)

    @property
    def size(self):
        return self._size

    @property
    def cells(self):
        return self._cells

    def __new__(cls, field_size: int):
        if field_size > 20:
            raise TypeError('The field size must be less than 21')

        return super().__new__(cls)

    def __str__(self) -> str:
        return f"{self._cells}"


@dataclass
class Player:
    name: str
    cell_type: CellValue


@dataclass
class UITexts:
    new_game_with_cross: str
    new_game_with_zeros: str
    congratulation: str
    title: str


@dataclass
class Settings(ABC):
    field_size: int

    human_player_name: str
    ai_player_name: str

    fps: int

    ui_texts: UITexts
