from abc import ABC
from dataclasses import dataclass
from typing import Sequence, Tuple, Union
from pygame.color import Color

from game.core.schemas import CellValue, GameField, UITexts, Player, CellPosition, ScreenPosition  # noqa


RGBAOutput = Tuple[int, int, int, int]

ColorValue = Union[Color, int, str, Tuple[int, int, int], RGBAOutput, Sequence[int]]


@dataclass
class Settings(ABC):
    duration_congratulation_sec: int

    line_width_pix: int

    cell_size_pix: int
    button_zone_size_pix: int

    width_pix: int
    height_pix: int

    font_name: str
    texts_font_size: int

    figure_color: ColorValue
    field_color: ColorValue
    congratulation_color: ColorValue
    buttons_labels_color: ColorValue
    buttons_color: ColorValue
