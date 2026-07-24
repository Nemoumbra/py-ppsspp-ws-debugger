from ppsspp.model.ppsspp_objects.logs.log_level import LogLevel

from dataclasses import dataclass


@dataclass
class PpssppLog:
    timestamp: str
    header: str
    message: str
    level: LogLevel
    channel: str
