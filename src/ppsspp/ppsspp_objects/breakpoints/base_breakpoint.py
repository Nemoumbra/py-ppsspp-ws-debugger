import json


class BaseBreakpoint:
    __slots__ = ("address", "enabled", "log", "cond", "fmt")

    def __init__(self):
        self.address: int = 0
        self.enabled: bool = False
        self.log: bool = False
        self.cond: str = ""
        self.fmt: str = ""

    def to_dict(self):
        raise NotImplementedError

    def from_dict(self, dictionary: dict):
        raise NotImplementedError

    def to_json(self):
        return json.dumps(self.to_dict())
