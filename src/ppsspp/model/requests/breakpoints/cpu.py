from dataclasses import dataclass


@dataclass(kw_only=True)
class CpuBreakpointAddRequest:
    address: int
    enabled: bool | None = None
    log: bool | None = None
    condition: str | None = None
    log_format: str | None = None


@dataclass(kw_only=True)
class CpuBreakpointUpdateRequest:
    address: int
    enabled: bool | None = None
    log: bool | None = None
    condition: str | None = None
    log_format: str | None = None


@dataclass(kw_only=True)
class CpuBreakpointRemoveRequest:
    address: int


@dataclass(kw_only=True)
class CpuBreakpointListRequest:
    pass
