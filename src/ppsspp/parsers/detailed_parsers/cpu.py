
from src.ppsspp.parsers.base_event_parser import BaseEventParser

from src.ppsspp.model.events.breakpoints.cpu import (
    CpuBreakpointAddEvent, CpuBreakpointUpdateEvent, CpuBreakpointRemoveEvent, CpuBreakpointListEvent
)
from src.ppsspp.model.events.cpu.common import (
    CpuSteppingEvent, CpuResumeEvent, CpuStatusEvent, CpuEvaluateEvent
)
from src.ppsspp.model.events.cpu.registers import (
    CpuGetRegEvent, CpuSetRegEvent, CpuGetAllRegsEvent
)


class CPUEventParser(BaseEventParser):
    def __init__(self):
        lookup_table = {
            "cpu.breakpoint.add": CpuBreakpointAddEvent,
            "cpu.breakpoint.update": CpuBreakpointUpdateEvent,
            "cpu.breakpoint.remove": CpuBreakpointRemoveEvent,
            "cpu.breakpoint.list": CpuBreakpointListEvent,

            "cpu.stepping": CpuSteppingEvent,
            "cpu.resume": CpuResumeEvent,
            "cpu.status": CpuStatusEvent,
            "cpu.evaluate": CpuEvaluateEvent,

            "cpu.getReg": CpuGetRegEvent,
            "cpu.setReg": CpuSetRegEvent,
            "cpu.getAllRegs": CpuGetAllRegsEvent,
        }

        BaseEventParser.__init__(self, lookup_table)
