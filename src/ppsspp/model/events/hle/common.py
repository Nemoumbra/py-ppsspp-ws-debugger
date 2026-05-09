from dataclasses import dataclass

from ppsspp.model.events.base_event import BaseEvent
from ppsspp.model.ppsspp_objects.hle.stack_frame import StackFrameInfo
from ppsspp.model.ppsspp_objects.hle.user_module import UserModuleInfo


@dataclass(kw_only=True)
class HleModuleListEvent(BaseEvent):
    modules: list[UserModuleInfo]


@dataclass(kw_only=True)
class HleBacktraceEvent(BaseEvent):
    frames: list[StackFrameInfo]
