from src.ppsspp.exceptions.event_parse_error import EventParseError
from src.ppsspp.events.input.buttons.input_buttons import InputButtonsEvent
from src.ppsspp.ppsspp_objects.input.buttons_state import ButtonsState
from src.ppsspp.ppsspp_objects.input.buttons_change import ButtonsChange


def input_buttons(event: dict):
    try:
        input_buttons_event = InputButtonsEvent()

        buttons = ButtonsState()
        buttons_data = event["buttons"]
        buttons.from_dict(buttons_data)
        input_buttons_event.buttons = buttons

        changed = ButtonsChange()
        changed_data = event["changed"]
        changed.from_dict(changed_data)
        input_buttons_event.changed = changed

        return input_buttons_event
    except KeyError as e:
        raise EventParseError("Missing input buttons parameter", e) from None
    except ValueError as e:
        raise EventParseError(e) from None
