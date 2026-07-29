
from ppsspp.parsers.base_event_parser import BaseEventParser

from ppsspp.model.events.other.log import LogEvent


class LogEventParser(BaseEventParser):
    def __init__(self):
        lookup_table = {
            "log": LogEvent
        }

        super().__init__(lookup_table)
