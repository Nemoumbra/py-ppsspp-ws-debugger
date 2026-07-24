from dataclasses import dataclass

from ppsspp.model.ppsspp_objects.game.game_info import GameInfo


@dataclass
class GameStatus:
    paused: bool
    game_info: GameInfo | None
