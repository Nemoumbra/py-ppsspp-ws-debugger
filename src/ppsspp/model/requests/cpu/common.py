from dataclasses import dataclass


@dataclass(kw_only=True)
class CpuSteppingRequest:
    pass


@dataclass(kw_only=True)
class CpuResumeRequest:
    pass


@dataclass(kw_only=True)
class CpuStatusRequest:
    pass


@dataclass(kw_only=True)
class CpuEvaluateRequest:
    thread: int | None = None
    expression: str
