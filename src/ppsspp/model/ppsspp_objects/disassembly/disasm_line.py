
from dataclasses import dataclass
from .branches import BranchInfo

@dataclass
class DataSymbol:
    start: int
    label: str | None


@dataclass
class DisasmLineBreakpoint:
    enabled: bool
    address: int
    condition: str | None


@dataclass
class DisasmLineRelevantData:
    address: int
    uint_value: int | None
    string_value: str | None


@dataclass
class DisasmLineDataAccess:
    address: int
    size: int
    uint_value: int | None
    symbol: str | None
    value_symbol: str | None


@dataclass
class DisasmLine:
    type: str
    address: int
    address_size: int
    encoding: int
    macro_encoding: list[int] | None
    background_color: str
    name: str
    params: str
    symbol: str | None
    function: str | None
    data_symbol: DataSymbol | None
    breakpoint: DisasmLineBreakpoint | None
    is_current_pc: bool
    branch: BranchInfo | None
    relevant_data: DisasmLineRelevantData | None
    condition_met: bool | None
    data_access: DisasmLineDataAccess | None
