from dataclasses import dataclass

from ppsspp.model.events.base_event import BaseEvent
from ppsspp.model.ppsspp_objects.input.button import Button
from ppsspp.model.ppsspp_objects.input.buttons_state import ButtonsState


@dataclass(kw_only=True)
class InputButtonsEvent(BaseEvent):
    buttons: ButtonsState
    changed: dict[Button, bool]


@dataclass(kw_only=True)
class InputButtonsSendEvent(BaseEvent):
    pass


# Sent once the button is released
@dataclass(kw_only=True)
class InputButtonsPressEvent(BaseEvent):
    pass
