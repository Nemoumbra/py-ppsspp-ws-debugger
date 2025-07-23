from src.ppsspp.requests.base_request_builder import BaseRequestBuilder
from src.ppsspp.ppsspp_request import PPSSPPRequest
from src.ppsspp.exceptions.request_build_error import RequestBuildError

from src.ppsspp.model.ppsspp_objects.input.buttons_change import ButtonsChange
from src.ppsspp.model.ppsspp_objects.input.button import Button
from src.ppsspp.model.ppsspp_objects.input.analog import Analog


class InputRequestBuilder(BaseRequestBuilder):
    def __init__(self):
        BaseRequestBuilder.__init__(self)
        self._request_lookup_table = {
            "input.buttons.send": input_buttons_send,
            "input.buttons.press": input_buttons_press,
            "input.analog.send": input_analog_send
        }


def input_buttons_send(**kwargs):
    event_name = "input.buttons.send"

    # Read the arguments
    try:
        buttons_arg = kwargs.pop("buttons")
    except KeyError as e:
        raise RequestBuildError(f"Missing {event_name} parameter", e) from None
    except ValueError as e:
        raise RequestBuildError(e) from None

    if kwargs:
        params = map(str, kwargs.keys())
        raise RequestBuildError(f"Unknown {event_name} parameters specified", f"{{{', '.join(params)}}}")

    # Now let's validate the data (client-side validation)

    if type(buttons_arg) is not dict:
        raise RequestBuildError(f"{event_name} request parameter 'buttons' must be a dictionary")

    try:
        changed = ButtonsChange()
        changed.from_dict(buttons_arg)  # the value is discarded after this
    except ValueError as e:
        raise RequestBuildError(e) from None

    # Now we know there are no issues with the data we need, let's build the request!
    request = PPSSPPRequest(event_name)
    request.add(buttons=buttons_arg)
    return request


def input_buttons_press(**kwargs):
    event_name = "input.buttons.press"

    # Read the arguments
    try:
        button_arg = kwargs.pop("button")
        duration_arg = kwargs.pop("duration", None)
    except KeyError as e:
        raise RequestBuildError(f"Missing {event_name} parameter", e) from None
    except ValueError as e:
        raise RequestBuildError(e) from None

    if kwargs:
        params = map(str, kwargs.keys())
        raise RequestBuildError(f"Unknown {event_name} parameters specified", f"{{{', '.join(params)}}}")

    # Now let's validate the data (client-side validation)

    if type(button_arg) is not str:
        raise RequestBuildError(f"{event_name} request parameter 'button' must be a string")

    try:
        button = Button[button_arg]
    except KeyError:
        raise RequestBuildError(f"Unknown Button '{button_arg}'") from None

    if duration_arg is not None and type(duration_arg) is not int:
        raise RequestBuildError(f"{event_name} request parameter 'duration' must be an integer")

    # Now we know there are no issues with the data we need, let's build the request!
    request = PPSSPPRequest(event_name)
    request.add(button=button_arg)
    if duration_arg:
        request.add(duration=duration_arg)

    return request


def input_analog_send(**kwargs):
    event_name = "input.analog.send"

    # Read the arguments
    try:
        x_arg = kwargs.pop("x")
        y_arg = kwargs.pop("y")
        stick_arg = kwargs.pop("stick", None)
    except KeyError as e:
        raise RequestBuildError(f"Missing {event_name} parameter", e) from None
    except ValueError as e:
        raise RequestBuildError(e) from None

    if kwargs:
        params = map(str, kwargs.keys())
        raise RequestBuildError(f"Unknown {event_name} parameters specified", f"{{{', '.join(params)}}}")

    # Now let's validate the data (client-side validation)

    if type(x_arg) is not float:
        raise RequestBuildError(f"{event_name} request parameter 'x' must be a dictionary")
    if type(y_arg) is not float:
        raise RequestBuildError(f"{event_name} request parameter 'y' must be a dictionary")

    if not (-1. <= x_arg <= 1):
        raise RequestBuildError(f"{event_name} request parameter 'x' must be in range from -1.0 to 1.0")
    if not (-1. <= y_arg <= 1):
        raise RequestBuildError(f"{event_name} request parameter 'y' must be in range from -1.0 to 1.0")

    if stick_arg is not None:
        if type(stick_arg) is not str:
            raise RequestBuildError(f"{event_name} request parameter 'stick' must be a string")

        try:
            analog = Analog[stick_arg]
        except KeyError:
            raise RequestBuildError(f"Unknown Analog '{stick_arg}'") from None

    # Now we know there are no issues with the data we need, let's build the request!
    request = PPSSPPRequest(event_name)
    request.add(x=x_arg, y=y_arg)
    if stick_arg:
        request.add(stick=stick_arg)

    return request
