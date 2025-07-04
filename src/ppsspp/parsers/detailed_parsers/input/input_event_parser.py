from src.ppsspp.parsers.base_event_parser import BaseEventParser
from src.ppsspp.parsers.detailed_parsers.input.input_buttons import (
    input_buttons
)
from src.ppsspp.parsers.detailed_parsers.input.input_analog import (
    input_analog
)


class InputEventParser(BaseEventParser):
    def __init__(self):
        BaseEventParser.__init__(self)
        # TODO:
        # input.buttons.send
        # input.buttons.press
        # input.analog.send

        self._lookup_table = {
            "input.buttons": input_buttons,
            "input.analog": input_analog
        }

