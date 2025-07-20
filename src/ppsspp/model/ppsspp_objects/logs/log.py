from src.ppsspp.model.ppsspp_objects.logs.log_level import LogLevel


class PPSSPPLog:
    __slots__ = ("timestamp", "header", "message", "level", "channel")

    def __init__(self):
        self.timestamp: str = ""
        self.header: str = ""
        self.message: str = ""
        self.level: LogLevel = LogLevel.notice
        self.channel: str = ""

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "header": self.header,
            "message": self.message,
            "level": self.level.value,
            "channel": self.channel
        }

    def from_dict(self, dictionary):
        try:
            self.timestamp = dictionary["timestamp"]
            self.header = dictionary["header"]
            self.message = dictionary["message"]
            self.level = LogLevel(dictionary["level"])  # may throw ValueError
            self.channel = dictionary["channel"]
        except KeyError as e:
            raise ValueError("Missing log parameter", e) from None
