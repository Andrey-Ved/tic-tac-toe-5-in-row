from dataclasses import dataclass

from game.core.schemas import UITexts, Settings as CoreSettings


@dataclass
class Settings(CoreSettings):
    field_size: int = 15

    human_player_name: str = 'Man'
    ai_player_name: str = 'AI'

    fps: int = 60

    ui_texts: UITexts = UITexts(
        new_game_with_cross='Start with crosses',
        new_game_with_zeros='Start with zeros',
        congratulation='The victory of ',
        title='tic tac toe',
    )


config = Settings()
