from dataclasses import dataclass

from src.ppsspp.model.events.base_event import BaseEvent

@dataclass(kw_only=True)
class InputAnalogEvent(BaseEvent):
    # TODO: decide what to do with AnalogState and Analog
    stick: str
    x: float
    y: float

@dataclass(kw_only=True)
class InputAnalogSendEvent(BaseEvent):
    pass
