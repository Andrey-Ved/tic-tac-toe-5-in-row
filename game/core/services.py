import pygame

from game.core.interfaces import (
    FieldViewInterface,
    AIInterface,
    RoundManagerInterface,
    GameInterface,
    IOCContainerInterface,
)
from game.core.schemas import (
    CellValue,
    CellPosition,
    ScreenPosition,
    GameField,
    Player,
)


class GameRoundManager(RoundManagerInterface):
    def __init__(
            self,
            ioc_container: IOCContainerInterface,
            player1: Player,
            player2: Player,
    ):

        self._ioc_container = ioc_container
        self._conf = ioc_container.core_conf

        self.players = [player1, player2]

        if player1.cell_type == CellValue.CROSS:
            self.current_player = 1
        else:
            self.current_player = 0

        self.field = GameField(self._conf.field_size)

        self._widget: FieldViewInterface = self._ioc_container.get_game_field_view(
            field=self.field,
            texts=self._conf.ui_texts
        )

        self._ai: AIInterface = self._ioc_container.get_ai(
            field=self.field,
            blunt=False,
            player_cell_type=player2.cell_type,
        )

    def _checking_ending(
            self,
            cell_pos: CellPosition,
    ) -> bool:

        line = [
            [] for _ in range(4)
        ]

        for deviation in range(-4, 5):
            for n, current_cell_pos in enumerate(
                    [
                        CellPosition(cell_pos.x + deviation, cell_pos.y),
                        CellPosition(cell_pos.x, cell_pos.y + deviation),
                        CellPosition(cell_pos.x + deviation, cell_pos.y + deviation),
                        CellPosition(cell_pos.x + deviation, cell_pos.y - deviation),
                    ]
            ):

                if 0 <= current_cell_pos.x < self.field.size \
                        and 0 <= current_cell_pos.y < self.field.size:
                    line[n].append(current_cell_pos)

        for n in range(4):
            count = 0

            for k in range(len(line[n])):
                current_cell_pos = line[n][k]

                if self.field.cells[current_cell_pos] == \
                        self.players[self.current_player].cell_type:
                    count += 1
                else:
                    count = 0

                if count > 4:
                    self._widget.draw_congratulation(
                        self.players[self.current_player]
                    )
                    return True

        return False

    def _checking_if_cell_is_empty(
            self,
            cell_pos: CellPosition,
    ) -> bool:
        if self.field.cells[cell_pos] == CellValue.VOID:
            return True

        return False

    def _players_move(
            self,
            cell_pos: CellPosition,
    ):
        self.field.cells[cell_pos] = self.players[self.current_player].cell_type
        self._widget.draw_cell(cell_pos)

    def ai_move(
            self,
    ) -> CellPosition:
        self.current_player = 1 - self.current_player
        ai_cell_pos = self._ai.get_move_variant()

        self._players_move(ai_cell_pos)
        return ai_cell_pos

    def handle_click(
            self,
            screen_pos: ScreenPosition,
    ) -> bool:
        cell_pos = self._widget.get_coords(screen_pos)

        if not self._checking_if_cell_is_empty(cell_pos):
            return False

        self.current_player = 1 - self.current_player
        self._players_move(cell_pos)

        if self._checking_ending(cell_pos):
            return True

        ai_cell_pos = self.ai_move()

        return self._checking_ending(ai_cell_pos)

    def check_coords_correct(
            self,
            screen_pos: ScreenPosition,
    ) -> bool:
        return self._widget.check_coords_correct(screen_pos)

    def pressed_button_is_one(
            self,
            screen_pos: ScreenPosition,
    ) -> bool:
        return self._widget.pressed_button_is_one(screen_pos)


class Game(GameInterface):
    def __init__(
            self,
            ioc_container: IOCContainerInterface,
    ):
        self._ioc_container = ioc_container
        self._conf = ioc_container.core_conf

        self._game_manager: RoundManagerInterface | None = None

        self._restart_game(
            pressed_button_is_one=True
        )

    def _restart_game(
            self,
            pressed_button_is_one: bool,
    ):
        if pressed_button_is_one:
            self._game_manager = self._ioc_container.get_game_round_manager(
                ioc_container=self._ioc_container,
                player1_cell_value=CellValue.CROSS,
                player2_cell_value=CellValue.ZERO,
            )
        else:
            self._game_manager = self._ioc_container.get_game_round_manager(
                ioc_container=self._ioc_container,
                player1_cell_value=CellValue.ZERO,
                player2_cell_value=CellValue.CROSS,

            )
            self._game_manager.ai_move()

    def main_loop(
            self,
    ):
        finished = False
        end = False
        clock = pygame.time.Clock()

        while not finished:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    screen_pos = ScreenPosition(*pygame.mouse.get_pos())

                    if self._game_manager.check_coords_correct(
                            screen_pos,
                    ):
                        if not end:
                            end = self._game_manager.handle_click(
                                screen_pos,
                            )
                    else:
                        end = False
                        self._restart_game(
                            self._game_manager.pressed_button_is_one(
                                screen_pos,
                            )
                        )

            pygame.display.flip()
            clock.tick(self._conf.fps)
