from src.ppsspp.exceptions.event_parse_error import EventParseError
from src.ppsspp.events.game.game_start import GameStartEvent
from src.ppsspp.events.game.game_quit import GameQuitEvent
from src.ppsspp.events.game.game_resume import GameResumeEvent
from src.ppsspp.events.game.game_pause import GamePauseEvent
from src.ppsspp.ppsspp_objects.game.game_info import GameInfo


def game_start(event: dict):
    try:
        started_event = GameStartEvent()
        data = event["game"]
        if data is None:
            started_event.game = None
        else:
            game_info = GameInfo()
            game_info.from_dict(data)
            started_event.game = game_info
        return started_event
    except KeyError as e:
        raise EventParseError("Missing game start parameter", e) from None
    except ValueError as e:
        raise EventParseError(e) from None


def game_quit(event: dict):
    try:
        quit_event = GameQuitEvent()
        data = event["game"]
        if data is not None:
            raise EventParseError("Game quit parameter 'game' is not 'null'")
        return quit_event
    except KeyError as e:
        raise EventParseError("Missing game quit parameter", e) from None
    except ValueError as e:
        raise EventParseError(e) from None


def game_pause(event: dict):
    try:
        paused_event = GamePauseEvent()
        data = event["game"]
        if data is None:
            paused_event.game = None
        else:
            game_info = GameInfo()
            game_info.from_dict(data)
            paused_event.game = game_info
        return paused_event
    except KeyError as e:
        raise EventParseError("Missing game pause parameter", e) from None
    except ValueError as e:
        raise EventParseError(e) from None


def game_resume(event: dict):
    try:
        resumed_event = GameResumeEvent()
        data = event["game"]
        if data is None:
            resumed_event.game = None
        else:
            game_info = GameInfo()
            game_info.from_dict(data)
            resumed_event.game = game_info
        return resumed_event
    except KeyError as e:
        raise EventParseError("Missing game resume parameter", e) from None
    except ValueError as e:
        raise EventParseError(e) from None
