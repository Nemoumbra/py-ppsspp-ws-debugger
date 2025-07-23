from enum import Enum, auto


class LogLevel(Enum):
    notice = 1
    error = auto()
    warn = auto()
    info = auto()
    debug = auto()
    verbose = auto()
