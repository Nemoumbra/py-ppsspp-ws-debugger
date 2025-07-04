from src.ppsspp.exceptions.event_parse_error import EventParseError
from src.ppsspp.events.cpu.cpu_stepping import SteppingEvent
from src.ppsspp.events.cpu.cpu_resume import ResumedEvent


def stepping(event: dict):
    try:
        stepping_event = SteppingEvent()
        stepping_event.pc = event["pc"]
        stepping_event.ticks = event["ticks"]
        return stepping_event
    except KeyError as e:
        raise EventParseError("Missing stepping parameter", e) from None
    except ValueError as e:
        raise EventParseError(e) from None


def resumed(event: dict):
    try:
        resumed_event = ResumedEvent()
        return resumed_event
    except ValueError as e:
        raise EventParseError(e) from None
