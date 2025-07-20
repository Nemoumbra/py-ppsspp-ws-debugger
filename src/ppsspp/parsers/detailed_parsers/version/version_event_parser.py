from src.ppsspp.parsers.base_event_parser import BaseEventParser
from src.ppsspp.exceptions.event_parse_error import EventParseError
from src.ppsspp.model.events.other.version import VersionEvent


class VersionEventParser(BaseEventParser):
    def __init__(self):
        BaseEventParser.__init__(self)
        self._lookup_table = {
            "version": version,
        }


def version(event: dict):
    try:
        version_event = VersionEvent()
        version_event.name = event.get("name")
        version_event.version = event.get("version")
        return version_event
    except KeyError as e:
        raise EventParseError("Missing version parameter", e) from None
    except ValueError as e:
        raise EventParseError(e) from None
