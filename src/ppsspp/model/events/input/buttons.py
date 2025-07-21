from dataclasses import dataclass

from src.ppsspp.model.events.base_event import BaseEvent


@dataclass(kw_only=True)
class InputButtonsEvent(BaseEvent):
    # TODO: maybe use the ButtonsState and ButtonsChange objects?
    buttons: dict[str, bool]
    changed: dict[str, bool]

@dataclass(kw_only=True)
class InputButtonsSendEvent(BaseEvent):
    pass

@dataclass(kw_only=True)
class InputButtonsPressEvent(BaseEvent):
    pass
