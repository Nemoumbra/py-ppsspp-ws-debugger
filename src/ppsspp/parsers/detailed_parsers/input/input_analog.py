from src.ppsspp.exceptions.event_parse_error import EventParseError
from src.ppsspp.model.events.input.analog.input_analog import InputAnalogEvent
from src.ppsspp.ppsspp_objects.input.analog_state import AnalogState


def input_analog(event: dict):
    try:
        input_analog_event = InputAnalogEvent()

        analog_state = AnalogState()
        analog_state.from_dict(event)
        input_analog_event.state = analog_state

        return input_analog_event
    except KeyError as e:
        raise EventParseError("Missing input analog parameter", e) from None
    except ValueError as e:
        raise EventParseError(e) from None
