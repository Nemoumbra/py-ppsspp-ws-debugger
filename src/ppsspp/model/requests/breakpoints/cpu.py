from dataclasses import dataclass

from ppsspp.model.requests.base_request import BaseRequest


@dataclass(kw_only=True)
class CpuBreakpointAddRequest(BaseRequest):
    address: int
    enabled: bool | None = None
    log: bool | None = None
    condition: str | None = None
    log_format: str | None = None


@dataclass(kw_only=True)
class CpuBreakpointUpdateRequest(BaseRequest):
    address: int
    enabled: bool | None = None
    log: bool | None = None
    condition: str | None = None
    log_format: str | None = None


@dataclass(kw_only=True)
class CpuBreakpointRemoveRequest(BaseRequest):
    address: int


@dataclass(kw_only=True)
class CpuBreakpointListRequest(BaseRequest):
    pass
