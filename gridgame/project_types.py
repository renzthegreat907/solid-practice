from dataclasses import dataclass
from enum import Enum, auto


# Probably better as `typing.NewType('PlayerId', int)`
type PlayerId = int

type Symbol = str


@dataclass(frozen=True)
class Cell:
    row: int
    col: int


class Feedback(Enum):
    VALID = auto()
    OUT_OF_BOUNDS = auto()
    OCCUPIED = auto()
    INVALID_SYMBOL = auto()
    GAME_OVER = auto()
