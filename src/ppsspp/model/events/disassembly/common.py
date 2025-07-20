
from dataclasses import dataclass
from xml.dom.domreg import well_known_implementations

from src.ppsspp.model.events.base_event import BaseEvent
from src.ppsspp.model.ppsspp_objects.disassembly.branches import BranchGuide
from src.ppsspp.model.ppsspp_objects.disassembly.disasm_line import DisasmLine


@dataclass(kw_only=True)
class MemoryBaseEvent(BaseEvent):
    address_hex: str


@dataclass
class DisasmRange:
    start: int
    end: int


@dataclass(kw_only=True)
class MemoryDisasmEvent(BaseEvent):
    range: DisasmRange
    lines: list[DisasmLine]
    branch_guides: list[BranchGuide]


@dataclass(kw_only=True)
class MemorySearchDisasmEvent(BaseEvent):
    address: int | None


@dataclass(kw_only=True)
class MemoryAssembleEvent(BaseEvent):
    encoding: int
