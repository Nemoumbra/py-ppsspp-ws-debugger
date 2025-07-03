from src.ppsspp.ppsspp_objects.breakpoints.base_breakpoint import BaseBreakpoint
from typing import Dict


class MemoryBreakpoint(BaseBreakpoint):
    __slots__ = ("size", "read", "write", "change")

    def __init__(self):
        BaseBreakpoint.__init__(self)
        self.size: int = 0
        self.read: bool = False
        self.write: bool = False
        self.change: bool = False

    def to_dict(self):
        return {
            "address": self.address,
            "size": self.size,
            "enabled": self.enabled,
            "log": self.log,
            "read": self.read,
            "write": self.write,
            "change": self.change,
            "condition": self.cond,
            "logFormat": self.fmt
        }

    def from_dict(self, dictionary: Dict):
        try:
            self.address = dictionary["address"]
            self.enabled = dictionary["enabled"]
            self.log = dictionary["log"]
            self.read = dictionary["read"]
            self.write = dictionary["write"]
            self.change = dictionary["change"]
            self.cond = dictionary["condition"]
            self.fmt = dictionary["logFormat"]
        except KeyError as e:
            raise ValueError("Missing breakpoint parameter", e) from None

    def __eq__(self, other: 'MemoryBreakpoint'):
        return self.fmt == other.fmt and self.cond == other.cond and self.log == other.log and \
               self.enabled == other.enabled and self.address == other.address and \
               self.change == other.change and self.read == other.read and self.write == other.write
