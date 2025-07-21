
from dataclasses import dataclass

from src.ppsspp.model.events.base_event import BaseEvent
from src.ppsspp.model.ppsspp_objects.hle.function_symbol import FunctionSymbolInfo


@dataclass(kw_only=True)
class HleFuncListEvent(BaseEvent):
    functions: list[FunctionSymbolInfo]


@dataclass(kw_only=True)
class HleFuncAddEvent(BaseEvent):
    address: int
    size: int
    name: str


@dataclass(kw_only=True)
class HleFuncRemoveEvent(BaseEvent):
    address: int
    size: int


@dataclass(kw_only=True)
class HleFuncRemoveRangeEvent(BaseEvent):
    count: int


@dataclass(kw_only=True)
class HleFuncRenameEvent(BaseEvent):
    address: int
    size: int
    name: str


@dataclass(kw_only=True)
class HleFuncScanEvent(BaseEvent):
    pass

