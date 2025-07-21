
from dataclasses import dataclass

from src.ppsspp.model.events.base_event import BaseEvent

# TODO: maybe wrap these into objects?

@dataclass(kw_only=True)
class BroadcastConfigGetEvent(BaseEvent):
    disallowed: dict[str: bool]

@dataclass(kw_only=True)
class BroadcastConfigSetEvent(BaseEvent):
    disallowed: dict[str: bool]
