from dataclasses import dataclass


@dataclass(kw_only=True)
class HleThreadListRequest:
    pass


@dataclass(kw_only=True)
class HleThreadWakeRequest:
    thread: int


@dataclass(kw_only=True)
class HleThreadStopRequest:
    thread: int
