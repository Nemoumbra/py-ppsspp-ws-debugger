
from src.ppsspp.parsers.base_event_parser import BaseEventParser

from src.ppsspp.model.events.hle.thread import (
    HleThreadListEvent, HleThreadStopEvent, HleThreadWakeEvent
)
from src.ppsspp.model.events.hle.func import (
    HleFuncListEvent, HleFuncAddEvent, HleFuncRemoveEvent,
    HleFuncRemoveRangeEvent, HleFuncRenameEvent, HleFuncScanEvent
)
from src.ppsspp.model.events.hle.common import (
    HleModuleListEvent, HleBacktraceEvent
)


class HLEEventParser(BaseEventParser):
    def __init__(self):
        lookup_table = {
            "hle.thread.list": HleThreadListEvent,
            "hle.thread.wake": HleThreadWakeEvent,
            "hle.thread.stop": HleThreadStopEvent,

            "hle.func.list": HleFuncListEvent,
            "hle.func.add": HleFuncAddEvent,
            "hle.func.remove": HleFuncRemoveEvent,
            "hle.func.removeRange": HleFuncRemoveRangeEvent,
            "hle.func.rename": HleFuncRenameEvent,
            "hle.func.scan": HleFuncScanEvent,

            "hle.module.list": HleModuleListEvent,
            "hle.backtrace": HleBacktraceEvent,
        }

        BaseEventParser.__init__(self, lookup_table)
