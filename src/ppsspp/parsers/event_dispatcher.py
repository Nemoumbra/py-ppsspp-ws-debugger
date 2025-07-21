
from src.ppsspp.exceptions.event_parse_error import EventParseError
from src.ppsspp.parsers.base_event_parser import BaseEventParser

from src.ppsspp.model.events.error_event import ErrorEvent, kErrorEvent

from adaptix import Retort

class EventDispatcher:
    def __init__(self, event_lookup_table: dict[str, BaseEventParser]):
        self._event_lookup_table = event_lookup_table
        self._retort = Retort()

    def parse_event(self, event: dict):
        if "event" not in event:
            raise EventParseError("Field 'event' not found in JSON")
        event_name: str = event["event"]
        if type(event_name) is not str:
            raise EventParseError("Field 'event' must be a string")

        event_group = event_name.split(".")[0]
        if event_group == kErrorEvent:
            return self._retort.load(event, ErrorEvent)

        if event_group not in self._event_lookup_table:
            raise EventParseError(f"Unknown event type '{event_group}' (full name '{event_name}')")

        # Now we delegate the parsing to a detailed parser
        result = self._event_lookup_table[event_group].parse(event)
        return result
