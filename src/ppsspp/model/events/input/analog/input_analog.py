from src.ppsspp.model.events.base_event import BaseEvent
from src.ppsspp.ppsspp_objects.input.analog_state import AnalogState


class InputAnalogEvent(BaseEvent):
    __slots__ = ("state")

    def __init__(self):
        BaseEvent.__init__(self, "input.analog")
        # initialize the fields
        self.state = AnalogState()
