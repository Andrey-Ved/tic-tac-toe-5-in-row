from typing import Type

from game.AI.schemas import Settings as AISettings
from game.AI.services import AI
from game.AI.settings import config as ai_config

from game.UI.schemas import Settings as UISettings
from game.UI.services import GameFieldView
from game.UI.settings import config as ui_config

from game.core.schemas import Settings as CoreSettings
from game.core.services import GameRoundManager
from game.core.settings import config as core_config

from game.core.interfaces import (
    FieldViewInterface,
    AIInterface,
    RoundManagerInterface,
    IOCContainerInterface,
)
from game.core.schemas import (
    CellValue,
    GameField,
    Player,
    UITexts,
)


class IOCContainer(IOCContainerInterface):
    def __init__(
            self,
            ai_conf: AISettings,
            ui_conf: UISettings,
            core_conf: CoreSettings,
            ai: Type[AIInterface],
            game_field_view: Type[FieldViewInterface],
            game_round_manager: Type[RoundManagerInterface],
    ):
        self._ai_conf = ai_conf
        self._ui_conf = ui_conf
        self._core_conf = core_conf

        self._ai = ai
        self._game_field_view = game_field_view
        self._game_round_manager = game_round_manager

    @property
    def ai_conf(self):
        return self._ai_conf

    @property
    def ui_conf(self):
        return self._ui_conf

    @property
    def core_conf(self):
        return self._core_conf

    def get_ai(
            self,
            field: GameField,
            blunt: bool,
            player_cell_type: CellValue,
    ) -> AIInterface:
        return self._ai(
            field=field,
            blunt=blunt,
            player_cell_type=player_cell_type,
            ai_config=self._ai_conf,
        )

    def get_game_field_view(
            self,
            field: GameField,
            texts: UITexts,
    ) -> FieldViewInterface:
        return GameFieldView(
            field=field,
            texts=texts,
            ui_conf=self._ui_conf,
        )

    def get_game_round_manager(
            self,
            ioc_container: IOCContainerInterface,
            player1_cell_value: CellValue,
            player2_cell_value: CellValue,
    ) -> RoundManagerInterface:
        return GameRoundManager(
            ioc_container=ioc_container,
            player1=Player(
                name=self._core_conf.human_player_name,
                cell_type=player1_cell_value,
            ),
            player2=Player(
                name=self._core_conf.ai_player_name,
                cell_type=player2_cell_value,
            )
        )


container = IOCContainer(
    ai_conf=ai_config,
    ui_conf=ui_config,
    core_conf=core_config,
    ai=AI,
    game_field_view=GameFieldView,
    game_round_manager=GameRoundManager,
)
