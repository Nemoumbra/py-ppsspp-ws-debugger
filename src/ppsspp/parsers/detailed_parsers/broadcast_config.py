from ppsspp.parsers.base_event_parser import BaseEventParser

from ppsspp.model.events.other.broadcast_config import (
    BroadcastConfigGetEvent, BroadcastConfigSetEvent
)


class BroadcastConfigEventParser(BaseEventParser):
    def __init__(self):
        lookup_table = {
            "broadcast.config.get": BroadcastConfigGetEvent,
            "broadcast.config.set": BroadcastConfigSetEvent,
        }

        super().__init__(lookup_table)
