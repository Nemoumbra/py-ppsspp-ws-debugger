from dataclasses import dataclass

from src.ppsspp.model.events.base_event import BaseEvent
from src.ppsspp.model.ppsspp_objects.hle.stack_frame import StackFrameInfo
from src.ppsspp.model.ppsspp_objects.hle.user_module import UserModuleInfo


@dataclass(kw_only=True)
class HleModuleListEvent(BaseEvent):
    modules: list[UserModuleInfo]


@dataclass(kw_only=True)
class HleBacktraceEvent(BaseEvent):
    frames: list[StackFrameInfo]
