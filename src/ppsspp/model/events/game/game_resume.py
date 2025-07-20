from src.ppsspp.model.events.base_event import BaseEvent
from src.ppsspp.model.ppsspp_objects.game.game_info import GameInfo


class GameResumeEvent(BaseEvent):
    __slots__ = "game"

    def __init__(self):
        BaseEvent.__init__(self, "game.resume")
        self.game: GameInfo | None = None
