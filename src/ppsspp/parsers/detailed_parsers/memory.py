
from src.ppsspp.parsers.base_event_parser import BaseEventParser

from src.ppsspp.model.events.breakpoints.memory import (
    MemoryBreakpointAddEvent, MemoryBreakpointUpdateEvent, MemoryBreakpointRemoveEvent, MemoryBreakpointListEvent
)
from src.ppsspp.model.events.disassembly.common import (
    MemoryBaseEvent, MemoryDisasmEvent, MemorySearchDisasmEvent, MemoryAssembleEvent
)
from src.ppsspp.model.events.memory.common import (
    MemoryReadU8Event, MemoryReadU16Event, MemoryReadU32Event, MemoryReadEvent,
    MemoryReadStringUtf8Event, MemoryReadStringB64Event,
    MemoryWriteU8Event, MemoryWriteU16Event, MemoryWriteU32Event, MemoryWriteEvent
)
from src.ppsspp.model.events.memory.memory_info import (
    MemoryMappingEvent,
    MemoryInfoConfigEvent, MemoryInfoSetEvent, MemoryInfoListEvent, MemoryInfoSearchEvent
)

class MemoryEventParser(BaseEventParser):
    def __init__(self):
        lookup_table = {
            "memory.breakpoint.add": MemoryBreakpointAddEvent,
            "memory.breakpoint.update": MemoryBreakpointUpdateEvent,
            "memory.breakpoint.remove": MemoryBreakpointRemoveEvent,
            "memory.breakpoint.list": MemoryBreakpointListEvent,

            "memory.base": MemoryBaseEvent,
            "memory.disasm": MemoryDisasmEvent,
            "memory.searchDisasm": MemorySearchDisasmEvent,
            "memory.assemble": MemoryAssembleEvent,

            "memory.read_u8": MemoryReadU8Event,
            "memory.read_u16": MemoryReadU16Event,
            "memory.read_u32": MemoryReadU32Event,
            "memory.read": MemoryReadEvent,
            "memory.readString": MemoryReadStringUtf8Event | MemoryReadStringB64Event,
            "memory.write_u8": MemoryWriteU8Event,
            "memory.write_u16": MemoryWriteU16Event,
            "memory.write_u32": MemoryWriteU32Event,
            "memory.write": MemoryWriteEvent,

            "memory.mapping": MemoryMappingEvent,
            "memory.info.config": MemoryInfoConfigEvent,
            "memory.info.set": MemoryInfoSetEvent,
            "memory.info.list": MemoryInfoListEvent,
            "memory.info.search": MemoryInfoSearchEvent,
        }

        BaseEventParser.__init__(self, lookup_table)
