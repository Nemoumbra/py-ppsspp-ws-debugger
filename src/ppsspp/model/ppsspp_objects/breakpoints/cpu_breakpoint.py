from src.ppsspp.model.ppsspp_objects.breakpoints.base_breakpoint import BaseBreakpoint


# So far this type of breakpoint doesn't have any special fields
class CPUBreakpoint(BaseBreakpoint):
    __slots__ = ()

    def __init__(self):
        BaseBreakpoint.__init__(self)

    def to_dict(self):
        return {
            "address": self.address,
            "enabled": self.enabled,
            "log": self.log,
            "condition": self.cond,
            "logFormat": self.fmt
        }

    def from_dict(self, dictionary: dict):
        try:
            self.address = dictionary["address"]
            self.enabled = dictionary["enabled"]
            self.log = dictionary["log"]
            self.cond = dictionary["condition"]
            self.fmt = dictionary["logFormat"]
        except KeyError as e:
            raise ValueError("Missing breakpoint parameter", e) from None

    def __eq__(self, other: 'CPUBreakpoint'):
        return self.fmt == other.fmt and self.cond == other.cond and self.log == other.log and \
            self.enabled == other.enabled and self.address == other.address
