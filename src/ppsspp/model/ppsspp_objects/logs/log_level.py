from enum import Enum


class LogLevel(Enum):
    # Not using auto to highlight the fact it's not something I decided on
    NOTICE = 1
    ERROR = 2
    WARN = 3
    INFO = 4
    DEBUG = 5
    VERBOSE = 6
