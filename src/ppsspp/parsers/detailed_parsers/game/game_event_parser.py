from src.ppsspp.parsers.base_event_parser import BaseEventParser
from src.ppsspp.parsers.detailed_parsers.game.game import (
    game_start, game_quit, game_pause, game_resume
)


class GameEventParser(BaseEventParser):
    def __init__(self):
        BaseEventParser.__init__(self)

        # game.reset
        # game.status
        self._lookup_table = {
            "game.start": game_start,
            "game.quit": game_quit,
            "game.resume": game_resume,
            "game.pause": game_pause
        }
