
from src.ppsspp.exceptions.event_parse_error import EventParseError

from adaptix import Retort, name_mapping, NameStyle


class BaseEventParser:
    def __init__(self):
        self._lookup_table = {}
        self._retort = Retort(recipe=[
            name_mapping(name_style=NameStyle.CAMEL)
        ])

    def parse(self, event: dict):
        event_name = event["event"]
        if event_name not in self._lookup_table:
            raise EventParseError(f"Unknown event '{event_name}'")

        cls = self._lookup_table[event_name]
        return self._retort.load(event, cls)
