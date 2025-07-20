from src.ppsspp.model.events.base_event import BaseEvent


class SteppingEvent(BaseEvent):
    __slots__ = ("pc", "ticks")

    def __init__(self):
        BaseEvent.__init__(self, "cpu.stepping")
        self.pc = 0x0
        self.ticks = 0
