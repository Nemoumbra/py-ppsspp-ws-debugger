from dataclasses import dataclass

from ppsspp.model.requests.base_request import BaseRequest


@dataclass(kw_only=True)
class InputButtonsSendRequest(BaseRequest):
    # TODO: maybe use the ButtonsState and ButtonsChange objects?
    buttons: dict[str, bool]


@dataclass(kw_only=True)
class InputButtonsPressRequest(BaseRequest):
    button: str
    duration: int | None = None
