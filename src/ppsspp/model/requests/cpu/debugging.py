from dataclasses import dataclass


@dataclass(kw_only=True)
class CpuStepIntoRequest:
    thread: int | None = None


@dataclass(kw_only=True)
class CpuStepOverRequest:
    thread: int | None = None


@dataclass(kw_only=True)
class CpuStepOutRequest:
    thread: int | None = None


@dataclass(kw_only=True)
class CpuRunUntilRequest:
    address: int


@dataclass(kw_only=True)
class CpuNextHleRequest:
    pass
