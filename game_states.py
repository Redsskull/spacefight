"""
A small but very importent file. it controls the state of the game which in turn controls which screen is shown.
"""

from enum import Enum, auto


class GameState(Enum):
    """
    Enum class for the game states.
    Args:
        auto: Automatically assign the values.
    """

    MAIN_MENU = auto()
    CHARACTER_SELECT = auto()
    STORY = auto()
    LEVEL = auto()
    GAME_OVER = auto()
    PAUSE = auto()
