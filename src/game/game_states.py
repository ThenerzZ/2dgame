from enum import Enum, auto

class GameStates(Enum):
    """Game state enumeration"""
    MENU = auto()
    PLAYING = auto()
    SHOPPING = auto()
    GAME_OVER = auto()
    PAUSED = auto() 