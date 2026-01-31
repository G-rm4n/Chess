from enum import Enum

class GameStates(Enum):
    PLAYING=0
    DRAW=1
    Bot_TURN=2
    CHECKMATE=3
    PREPARINGGAME=4
    PLAYER_TURN=5
    Movement_Choiced=6