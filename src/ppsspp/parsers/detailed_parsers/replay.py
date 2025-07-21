
from src.ppsspp.parsers.base_event_parser import BaseEventParser

from src.ppsspp.model.events.replay.common import (
    ReplayBeginEvent, ReplayAbortEvent, ReplayFlushEvent, ReplayExecuteEvent, ReplayStatusEvent
)
from src.ppsspp.model.events.replay.time import (
    ReplayTimeGetEvent, ReplayTimeSetEvent
)

class ReplayEventParser(BaseEventParser):
    def __init__(self):
        lookup_table = {
            "replay.begin": ReplayBeginEvent,
            "replay.abort": ReplayAbortEvent,
            "replay.flush": ReplayFlushEvent,
            "replay.execute": ReplayExecuteEvent,
            "replay.status": ReplayStatusEvent,

            "replay.time.get": ReplayTimeGetEvent,
            "replay.time.set": ReplayTimeSetEvent,
        }

        BaseEventParser.__init__(self, lookup_table)
