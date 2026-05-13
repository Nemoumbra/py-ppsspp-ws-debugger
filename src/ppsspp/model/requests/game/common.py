from dataclasses import dataclass


@dataclass(kw_only=True)
class GameResetRequest:
    break_: bool | None = None


@dataclass(kw_only=True)
class GameStatusRequest:
    pass
