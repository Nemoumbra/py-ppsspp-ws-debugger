
from src.ppsspp.parsers.base_event_parser import BaseEventParser

from src.ppsspp.model.events.game.common import (
    GameResetEvent, GameStatusEvent, GamePauseEvent, GameResumeEvent, GameStartEvent, GameQuitEvent
)


class GameEventParser(BaseEventParser):
    def __init__(self):
        lookup_table = {
            "game.reset": GameResetEvent,
            "game.status": GameStatusEvent,
            "game.pause": GamePauseEvent,
            "game.resume": GameResumeEvent,
            "game.start": GameStartEvent,
            "game.quit": GameQuitEvent,
        }

        BaseEventParser.__init__(self, lookup_table)
