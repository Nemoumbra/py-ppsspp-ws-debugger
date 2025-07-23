
from src.ppsspp.parsers.base_event_parser import BaseEventParser

from src.ppsspp.model.events.input.buttons import (
    InputButtonsEvent, InputButtonsSendEvent, InputButtonsPressEvent
)
from src.ppsspp.model.events.input.analog import (
    InputAnalogEvent, InputAnalogSendEvent
)

class InputEventParser(BaseEventParser):
    def __init__(self):
        lookup_table = {
            "input.buttons": InputButtonsEvent,
            "input.buttons.send": InputButtonsSendEvent,
            "input.buttons.press": InputButtonsPressEvent,

            "input.analog": InputAnalogEvent,
            "input.analog.send": InputAnalogSendEvent,
        }

        BaseEventParser.__init__(self, lookup_table)
