from dataclasses import dataclass

from ppsspp.model.requests.base_request import BaseRequest


@dataclass(kw_only=True)
class GameResetRequest(BaseRequest):
    break_: bool | None = None


@dataclass(kw_only=True)
class GameStatusRequest(BaseRequest):
    pass
