
from src.ppsspp.exceptions.event_parse_error import EventParseError


# TODO: instead of the lookup table, use the retorts from adaptix
class BaseEventParser:
    def __init__(self):
        self._lookup_table = {}

    def parse(self, event: dict):
        event_name = event["event"]
        if event_name not in self._lookup_table:
            raise EventParseError(f"Unknown event '{event_name}'")

        return self._lookup_table[event_name](event)
