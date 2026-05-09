
from dataclasses import dataclass
from ppsspp.model.events.base_event import BaseEvent


@dataclass(kw_only=True)
class VersionEvent(BaseEvent):
    name: str
    version: str
