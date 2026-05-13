from dataclasses import dataclass


@dataclass(kw_only=True)
class InputButtonsSendRequest:
    # TODO: maybe use the ButtonsState and ButtonsChange objects?
    buttons: dict[str, bool]


@dataclass(kw_only=True)
class InputButtonsPressRequest:
    button: str
    duration: int | None = None
