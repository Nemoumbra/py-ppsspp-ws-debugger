from dataclasses import dataclass

from ppsspp.model.requests.base_request import BaseRequest


@dataclass(kw_only=True)
class InputButtonsSendRequest(BaseRequest):
    buttons: dict[str, bool]


@dataclass(kw_only=True)
class InputButtonsPressRequest(BaseRequest):
    button: str
    duration: int | None = None
