from dataclasses import dataclass


@dataclass(kw_only=True)
class HleModuleListRequest:
    pass


@dataclass(kw_only=True)
class HleBacktraceRequest:
    thread: int | None = None
