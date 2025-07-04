from src.ppsspp.parsers.base_event_parser import BaseEventParser
from src.ppsspp.exceptions.event_parse_error import EventParseError
from src.ppsspp.ppsspp_objects.logs.log import PPSSPPLog
from src.ppsspp.events.other.log import LogEvent


class LogEventParser(BaseEventParser):
    def __init__(self):
        BaseEventParser.__init__(self)
        self._detailed_lookup_table = {
            "log": log
        }


def log(event: dict):
    try:
        log_event = LogEvent()

        ppsspp_log = PPSSPPLog()
        ppsspp_log.from_dict(event)

        log_event.log = ppsspp_log
        return log_event
    except ValueError as e:
        raise EventParseError(e) from None
