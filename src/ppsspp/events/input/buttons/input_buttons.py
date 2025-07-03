from src.ppsspp.events.base_event import BaseEvent
from src.ppsspp.ppsspp_objects.input.buttons_state import ButtonsState
from src.ppsspp.ppsspp_objects.input.buttons_change import ButtonsChange


class InputButtonsEvent(BaseEvent):
    __slots__ = ("buttons", "changed")

    def __init__(self):
        BaseEvent.__init__(self, "input.buttons")
        self.buttons = ButtonsState()
        self.changed = ButtonsChange()
