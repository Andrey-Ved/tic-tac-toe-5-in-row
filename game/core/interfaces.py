from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Type

from game.core.schemas import (
    CellValue,
    CellPosition,
    ScreenPosition,
    GameField,
    UITexts,
    Player,
)


class AIInterface(ABC):
    @abstractmethod
    def __init__(
            self,
            field: GameField,  # noqa
            blunt: bool,  # noqa
            player_cell_type: CellValue,  # noqa
            ai_config: AISettings,  # noqa #
    ):
        ...

    @abstractmethod
    def get_move_variant(
            self,
    ) -> CellPosition:
        ...


class FieldViewInterface(ABC):
    @abstractmethod
    def __init__(
            self,
            field: GameField,  # noqa
            texts: UITexts,  # noqa
            ui_config: UISettings,  # noqa
    ):
        ...

    @abstractmethod
    def draw_cell(
            self,
            cell_pos: CellPosition,
    ):
        ...

    @abstractmethod
    def draw_congratulation(
            self,
            player: Player,
    ):
        ...

    @abstractmethod
    def check_coords_correct(
            self,
            screen_pos: ScreenPosition,
    ) -> bool:
        ...

    @abstractmethod
    def pressed_button_is_one(
            self,
            screen_pos: ScreenPosition,
    ) -> bool:
        ...

    @abstractmethod
    def get_coords(
            self,
            screen_pos: ScreenPosition,
    ) -> CellPosition:
        ...


class RoundManagerInterface(ABC):
    @abstractmethod
    def __init__(
            self,
            ioc_container: IOCContainerInterface,  # noqa
            player1: Player,  # noqa
            player2: Player,  # noqa
    ):
        ...

    @abstractmethod
    def ai_move(
            self,
    ) -> CellPosition:
        ...

    @abstractmethod
    def handle_click(
            self,
            screen_pos: ScreenPosition,
    ) -> bool:
        ...

    @abstractmethod
    def check_coords_correct(
            self,
            screen_pos: ScreenPosition,
    ) -> bool:
        ...

    @abstractmethod
    def pressed_button_is_one(
            self,
            screen_pos: ScreenPosition,
    ) -> bool:
        ...


class GameInterface(ABC):
    @abstractmethod
    def __init__(
            self,
            ioc_container: IOCContainerInterface,  # noqa
    ):
        ...

    @abstractmethod
    def main_loop(
            self,
    ):
        ...


class IOCContainerInterface(ABC):
    @abstractmethod
    def __init__(
            self,
            ai: Type[AIInterface],  # noqa
            game_field_view: Type[FieldViewInterface],  # noqa
            game_round_manager: Type[RoundManagerInterface],  # noqa
    ):
        ...

    @property
    @abstractmethod
    def core_conf(self):
        ...

    @abstractmethod
    def get_ai(
            self,
            field: GameField,
            blunt: bool,
            player_cell_type: CellValue,
    ) -> AIInterface:
        ...

    @abstractmethod
    def get_game_field_view(
            self,
            field: GameField,
            texts: UITexts,
    ) -> FieldViewInterface:
        ...

    @abstractmethod
    def get_game_round_manager(
            self,
            ioc_container: IOCContainerInterface,
            player1_cell_value: CellValue,
            player2_cell_value: CellValue,
    ) -> RoundManagerInterface:
        ...
