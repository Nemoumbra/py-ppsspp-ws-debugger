
from dataclasses import dataclass

from src.ppsspp.model.events.base_event import BaseEvent
from src.ppsspp.model.ppsspp_objects.game.game_info import GameInfo


@dataclass(kw_only=True)
class GameResetEvent(BaseEvent):
    pass


@dataclass(kw_only=True)
class GameStatusEvent(BaseEvent):
    game: GameInfo | None
    paused: bool


@dataclass(kw_only=True)
class GamePauseEvent(BaseEvent):
    game: GameInfo | None


@dataclass(kw_only=True)
class GameResumeEvent(BaseEvent):
    game: GameInfo | None


@dataclass(kw_only=True)
class GameStartEvent(BaseEvent):
    game: GameInfo | None


@dataclass(kw_only=True)
class GameQuitEvent(BaseEvent):
    game: None  # Not a typo
