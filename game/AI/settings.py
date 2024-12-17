from dataclasses import dataclass, field

from game.AI.schemas import Template, Settings as AISettings


@dataclass
class Settings(AISettings):
    templates: dict[Template, int] = field(default_factory=lambda: {
        'xxxxx': 10000,  # noqa
        '0xxxx0': 1000,
        '0xxxx': 500,
        'xxxx0': 500,
        'xxx0x': 400,
        'x0xxx': 400,
        'xx0xx': 400,
        '000xxx00': 100,
        '00xxx000': 100,
        '00xxx00': 80,
        '00xxx0': 75,
        '0xxx00': 75,
        '0xxx0': 50,
        '00xxx': 50,
        'xxx00': 50,
        '0xx0x': 25,
        'x0xx0': 25,
        '0x0xx': 25,
        'xx0x0': 25,
        'xx00x': 25,
        'x00xx': 25,
        '000xx000': 10,
        '0xx0': 5,
    })


config = Settings()
