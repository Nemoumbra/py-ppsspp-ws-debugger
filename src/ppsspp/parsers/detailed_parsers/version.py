
from src.ppsspp.parsers.base_event_parser import BaseEventParser

from src.ppsspp.model.events.other.version import VersionEvent


class VersionEventParser(BaseEventParser):
    def __init__(self):
        lookup_table = {
            "version": VersionEvent,
        }

        BaseEventParser.__init__(self, lookup_table)
