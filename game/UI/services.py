import pygame
from time import sleep

from game.core.interfaces import FieldViewInterface

from game.UI.schemas import (
    ColorValue,
    CellValue,
    CellPosition,
    ScreenPosition,
    GameField,
    UITexts,
    Player,
    Settings as UISettings
)


class GameFieldView(FieldViewInterface):
    def __init__(
            self,
            field: GameField,
            texts: UITexts,
            ui_conf: UISettings,
    ):
        self._field = field
        self._texts = texts

        self._conf = ui_conf

        pygame.init()
        pygame.font.SysFont(
            self._conf.font_name,
            self._conf.texts_font_size,
        )

        self._font = pygame.font.Font(
            None,
            self._conf.texts_font_size,
        )
        self._screen = pygame.display.set_mode(
            (self._conf.width_pix, self._conf.height_pix)
        )

        pygame.display.set_caption(self._texts.title)

        self._display_new_field()

    def _text_out(
            self,
            text: str,
            color: ColorValue,
            screen_pos: ScreenPosition,
    ):
        text = self._font.render(text, True, color)

        text_rect = text.get_rect()
        text_rect.center = (
            screen_pos.x,
            screen_pos.y
        )

        self._screen.blit(text, text_rect)

    def _display_new_field(
            self,
    ):
        for x in range(0, self._conf.width_pix, self._conf.cell_size_pix):
            for y in range(0, self._conf.width_pix, self._conf.cell_size_pix):
                pygame.draw.rect(
                    self._screen,
                    self._conf.field_color,
                    (
                        x + self._conf.line_width_pix,
                        self._conf.button_zone_size_pix + y + self._conf.line_width_pix,
                        self._conf.cell_size_pix - self._conf.line_width_pix * 2,
                        self._conf.cell_size_pix - self._conf.line_width_pix * 2
                    )
                )

        for x in 0, self._conf.width_pix // 2:
            pygame.draw.rect(
                self._screen,
                self._conf.buttons_color,
                (
                    self._conf.line_width_pix + x,
                    self._conf.line_width_pix, self._conf.width_pix // 2
                    - self._conf.line_width_pix * 2,
                    self._conf.button_zone_size_pix - self._conf.line_width_pix * 2
                )
            )

        button_text = [
            self._texts.new_game_with_cross,
            self._texts.new_game_with_zeros
        ]

        for n in 0, 1:
            self._text_out(
                text=button_text[n],
                color=self._conf.buttons_labels_color,
                screen_pos=ScreenPosition(
                    n * self._conf.width_pix // 2 + self._conf.width_pix // 4,
                    self._conf.button_zone_size_pix // 2
                )
            )

    def draw_cell(
            self,
            cell_pos: CellPosition,
    ):
        if self._field.cells[cell_pos] == CellValue.CROSS:
            text = 'X'
        elif self._field.cells[cell_pos] == CellValue.ZERO:
            text = 'O'
        else:
            text = ''

        self._text_out(
            text=text,
            color=self._conf.figure_color,
            screen_pos=ScreenPosition(
                cell_pos.x * self._conf.cell_size_pix + self._conf.cell_size_pix // 2,
                cell_pos.y * self._conf.cell_size_pix + self._conf.cell_size_pix // 2
                + self._conf.button_zone_size_pix,
            )
        )

    def draw_congratulation(
            self,
            player: Player,
    ):
        self._text_out(
            text=f'{self._texts.congratulation} {player.name}',
            color=self._conf.congratulation_color,
            screen_pos=ScreenPosition(
                self._conf.width_pix // 2,
                self._conf.button_zone_size_pix + self._conf.width_pix // 2
            )
        )

        pygame.display.flip()
        sleep(self._conf.duration_congratulation_sec)

    def check_coords_correct(
            self,
            screen_pos: ScreenPosition,
    ) -> bool:
        if self._conf.button_zone_size_pix <= screen_pos.y <= self._conf.height_pix \
                and 0 <= screen_pos.x <= self._conf.width_pix:
            return True
        return False

    def pressed_button_is_one(
            self,
            screen_pos: ScreenPosition,
    ) -> bool:
        return screen_pos.x < self._field.size * self._conf.cell_size_pix // 2

    def get_coords(
            self,
            screen_pos: CellPosition,
    ) -> CellPosition:
        return CellPosition(
            x=screen_pos.x // self._conf.cell_size_pix,
            y=(screen_pos.y - self._conf.button_zone_size_pix) // self._conf.cell_size_pix,
        )
