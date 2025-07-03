from src.ppsspp.events.base_event import BaseEvent


class GameQuitEvent(BaseEvent):
    __slots__ = "game"

    def __init__(self):
        BaseEvent.__init__(self, "game.quit")
        self.game: None = None

