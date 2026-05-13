from dataclasses import dataclass


@dataclass(kw_only=True)
class MemoryBreakpointAddRequest:
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
class MemoryBreakpointUpdateRequest:
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
class MemoryBreakpointRemoveRequest:
    address: int
    size: int


@dataclass(kw_only=True)
class MemoryBreakpointListRequest:
    pass
