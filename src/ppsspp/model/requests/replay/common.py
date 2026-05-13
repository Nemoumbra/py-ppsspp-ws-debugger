from dataclasses import dataclass


@dataclass(kw_only=True)
class ReplayBeginRequest:
    pass


@dataclass(kw_only=True)
class ReplayAbortRequest:
    pass


@dataclass(kw_only=True)
class ReplayFlushRequest:
    pass


@dataclass(kw_only=True)
class ReplayExecuteRequest:
    version: int
    base64: str


@dataclass(kw_only=True)
class ReplayStatusRequest:
    pass
