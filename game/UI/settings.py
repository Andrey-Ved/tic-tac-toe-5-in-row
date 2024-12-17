from dataclasses import dataclass

from game.core.settings import config as core_config

from game.UI.schemas import ColorValue, Settings as UISettings


@dataclass
class Settings(UISettings):
    duration_congratulation_sec: int = 2

    line_width_pix: int = 2

    cell_size_pix: int = 40
    button_zone_size_pix: int = 60

    width_pix: int = core_config.field_size * cell_size_pix
    height_pix: int = width_pix + button_zone_size_pix

    font_name: str = 'ARIAL'
    texts_font_size: int = 32

    figure_color: ColorValue = (255, 255, 255)
    field_color: ColorValue = (125, 125, 125)
    congratulation_color: ColorValue = (200, 200, 255)
    buttons_labels_color: ColorValue = (125, 125, 125)
    buttons_color: ColorValue = (255, 255, 255)


config = Settings()
