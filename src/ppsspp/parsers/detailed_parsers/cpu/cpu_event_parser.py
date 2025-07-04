from src.ppsspp.parsers.base_event_parser import BaseEventParser
from src.ppsspp.parsers.detailed_parsers.cpu.cpu_stepping import (
    stepping, resumed
)


class CPUEventParser(BaseEventParser):
    def __init__(self):
        BaseEventParser.__init__(self)

        # TODO:
        # cpu.breakpoint.add
        # cpu.breakpoint.update
        # cpu.breakpoint.remove
        # cpu.breakpoint.list

        # cpu.status
        # cpu.getAllRegs
        # cpu.getReg
        # cpu.setReg
        # cpu.evaluate
        self._detailed_lookup_table = {
            "cpu.stepping": stepping,
            "cpu.resume": resumed
        }
