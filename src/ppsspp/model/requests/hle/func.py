from dataclasses import dataclass


@dataclass(kw_only=True)
class HleFuncListRequest:
    pass


@dataclass(kw_only=True)
class HleFuncAddRequest:
    address: int
    size: int | None = None
    name: str | None = None


@dataclass(kw_only=True)
class HleFuncRemoveRequest:
    address: int


@dataclass(kw_only=True)
class HleFuncRemoveRangeRequest:
    address: int
    size: int


@dataclass(kw_only=True)
class HleFuncRenameRequest:
    address: int
    name: str


@dataclass(kw_only=True)
class HleFuncScanRequest:
    address: int
    size: int
    remove: bool | None = None
