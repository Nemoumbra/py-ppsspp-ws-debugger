from dataclasses import dataclass

from ppsspp.model.requests.base_request import BaseRequest


@dataclass(kw_only=True)
class HleModuleListRequest(BaseRequest):
    pass


@dataclass(kw_only=True)
class HleBacktraceRequest(BaseRequest):
    thread: int | None = None
