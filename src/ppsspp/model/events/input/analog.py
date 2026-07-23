from dataclasses import dataclass

from ppsspp.model.events.base_event import BaseEvent
from ppsspp.model.ppsspp_objects.input.analog_stick import AnalogStick


@dataclass(kw_only=True)
class InputAnalogEvent(BaseEvent):
    stick: AnalogStick
    x: float
    y: float


@dataclass(kw_only=True)
class InputAnalogSendEvent(BaseEvent):
    pass
