
from ppsspp.parsers.base_event_parser import BaseEventParser

from ppsspp.model.events.other.version import VersionEvent


class VersionEventParser(BaseEventParser):
    def __init__(self):
        lookup_table = {
            "version": VersionEvent,
        }

        super().__init__(lookup_table)
