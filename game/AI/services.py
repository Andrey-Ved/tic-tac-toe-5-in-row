from random import choice as random_choice
from typing import List

from game.core.interfaces import AIInterface

from game.AI.schemas import (
    CellValue,
    CellPosition,
    CellPositionWeight,
    GameField,
    Template,
    Settings as AISettings,
)


class AI(AIInterface):
    def __init__(
            self,
            field: GameField,
            blunt: bool,
            player_cell_type: CellValue,
            ai_config: AISettings,
    ):
        self._field = field
        self._blunt = blunt
        self._player_cell_type = player_cell_type

        self._templates = ai_config.templates

    def _template_reconciliation(
            self,
            situation: Template,
    ) -> int:
        if self._blunt:
            return 1

        weight = 0

        for item in self._templates:
            if item in situation:
                weight += self._templates[item]

        return weight

    def _get_evaluation(
            self,
            cell_type: CellValue,
            position: CellPosition,
    ) -> int:
        situations: List[Template] = [Template('') for _ in range(4)]

        for deviation in range(-4, 5):
            for n, current_position in enumerate([
                CellPosition(position.x + deviation, position.y),
                CellPosition(position.x, position.y + deviation),
                CellPosition(position.x + deviation, position.y + deviation),
                CellPosition(position.x + deviation, position.y - deviation)
            ]):
                if current_position == position:
                    situations[n] += 'x'
                else:
                    if 0 <= current_position.x < self._field.size \
                            and 0 <= current_position.y < self._field.size:

                        if self._field.cells[current_position] == CellValue.VOID:
                            situations[n] += '0'
                        elif self._field.cells[current_position] == cell_type:
                            situations[n] += 'x'
                        else:
                            situations[n] += '1'

        evaluation = sum(
            map(
                self._template_reconciliation,
                situations,
            )
        )
        return evaluation

    def _variant_choosing(
            self,
            cell_type: CellValue,
            possibles_move: List[CellPosition],
    ) -> CellPositionWeight:

        max_weight_cell_position = CellPositionWeight(
            position=random_choice(possibles_move),
            weight=0,
        )

        for current_position in possibles_move:
            current_weight = self._get_evaluation(
                cell_type=cell_type,
                position=current_position,
            )
            if max_weight_cell_position.weight < current_weight:
                max_weight_cell_position = CellPositionWeight(
                    weight=current_weight,
                    position=current_position,
                )

        return max_weight_cell_position

    def _get_possibles_move(
            self,
    ) -> List[CellPosition]:
        possibles_move = []

        for x in range(self._field.size):
            for y in range(self._field.size):
                if self._field.cells[CellPosition(x, y)] != CellValue.VOID:

                    for current_x in range(x - 2, x + 3):
                        for current_y in range(y - 2, y + 3):

                            if 0 <= current_x < self._field.size \
                                    and 0 <= current_y < self._field.size:
                                if self._field.cells[
                                    CellPosition(current_x, current_y)
                                ] == CellValue.VOID:
                                    possibles_move.append(
                                        CellPosition(
                                            x=current_x,
                                            y=current_y
                                        )
                                    )
        return possibles_move

    def get_move_variant(
            self,
    ):
        possibles_move = self._get_possibles_move()

        if not possibles_move:
            position = CellPosition(
                x=self._field.size // 2,
                y=self._field.size // 2,
            )

        else:
            attack_max_weight_cell_position = self._variant_choosing(
                cell_type=self._player_cell_type,
                possibles_move=possibles_move,
            )
            defense_max_weight_cell_position = self._variant_choosing(
                cell_type=CellValue.ZERO
                if self._player_cell_type == CellValue.CROSS
                else CellValue.CROSS,

                possibles_move=possibles_move,
            )

            if attack_max_weight_cell_position.weight >= defense_max_weight_cell_position.weight:
                position = attack_max_weight_cell_position.position
            else:
                position = defense_max_weight_cell_position.position

        return position
