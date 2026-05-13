from dataclasses import dataclass

from ppsspp.model.requests.base_request import BaseRequest


@dataclass(kw_only=True)
class HleFuncListRequest(BaseRequest):
    pass


@dataclass(kw_only=True)
class HleFuncAddRequest(BaseRequest):
    address: int
    size: int | None = None
    name: str | None = None


@dataclass(kw_only=True)
class HleFuncRemoveRequest(BaseRequest):
    address: int


@dataclass(kw_only=True)
class HleFuncRemoveRangeRequest(BaseRequest):
    address: int
    size: int


@dataclass(kw_only=True)
class HleFuncRenameRequest(BaseRequest):
    address: int
    name: str


@dataclass(kw_only=True)
class HleFuncScanRequest(BaseRequest):
    address: int
    size: int
    remove: bool | None = None
