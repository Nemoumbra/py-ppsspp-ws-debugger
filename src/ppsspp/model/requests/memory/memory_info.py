from dataclasses import dataclass


@dataclass(kw_only=True)
class MemoryMappingRequest:
    pass


@dataclass(kw_only=True)
class MemoryInfoConfigRequest:
    detailed: bool | None = None


@dataclass(kw_only=True)
class MemoryInfoSetRequest:
    address: int
    size: int
    # How do we fix the values?
    type: str
    tag: str | None = None
    pc: int | None = None


@dataclass(kw_only=True)
class MemoryInfoListRequest:
    address: int
    size: int
    # How do we fix the values?
    type: str | None = None


@dataclass(kw_only=True)
class MemoryInfoSearchRequest:
    address: int | None = None
    end: int | None = None
    match: str
    type: str | None = None
