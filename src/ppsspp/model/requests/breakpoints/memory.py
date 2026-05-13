from dataclasses import dataclass

from ppsspp.model.requests.base_request import BaseRequest


@dataclass(kw_only=True)
class MemoryBreakpointAddRequest(BaseRequest):
    address: int
    size: int
    enabled: bool | None = None
    log: bool | None = None
    read: bool | None = None
    write: bool | None = None
    change: bool | None = None
    condition: str | None = None
    log_format: str | None = None


@dataclass(kw_only=True)
class MemoryBreakpointUpdateRequest(BaseRequest):
    address: int
    size: int
    enabled: bool | None = None
    log: bool | None = None
    read: bool | None = None
    write: bool | None = None
    change: bool | None = None
    condition: str | None = None
    log_format: str | None = None


@dataclass(kw_only=True)
class MemoryBreakpointRemoveRequest(BaseRequest):
    address: int
    size: int


@dataclass(kw_only=True)
class MemoryBreakpointListRequest(BaseRequest):
    pass
