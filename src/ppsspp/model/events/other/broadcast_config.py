from dataclasses import dataclass

from ppsspp.model.events.base_event import BaseEvent


@dataclass(kw_only=True)
class BroadcastConfigGetEvent(BaseEvent):
    disallowed: dict


@dataclass(kw_only=True)
class BroadcastConfigSetEvent(BaseEvent):
    disallowed: dict
