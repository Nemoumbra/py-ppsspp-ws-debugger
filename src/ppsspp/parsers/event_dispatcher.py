
from src.ppsspp.exceptions.event_parse_error import EventParseError
from src.ppsspp.parsers.base_event_parser import BaseEventParser
from src.ppsspp.events.error_event import ErrorEvent, kErrorEvent


class EventDispatcher:
    def __init__(self, event_lookup_table: dict[str, BaseEventParser]):
        self._event_lookup_table = event_lookup_table

    def parse_event(self, event: dict):
        if "event" not in event:
            raise EventParseError("Field 'event' not found in JSON")
        event_name: str = event["event"]
        if type(event_name) is not str:
            raise EventParseError("Field 'event' must be a string")

        event_group = event_name.split(".")[0]
        if event_group == kErrorEvent:
            error = ErrorEvent()
            try:
                error.from_dict(event)
                return error
            except ValueError as e:
                raise EventParseError(e) from None

        if event_group not in self._event_lookup_table:
            raise EventParseError(f"Unknown event type '{event_group}' (full name '{event_name}')")
        # Now we delegate the parsing to a detailed parser
        result = self._event_lookup_table[event_group].parse(event)
        # Finally, we set up the ticket
        result.ticket = event.get("ticket")
        return result
