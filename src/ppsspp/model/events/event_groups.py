
from typing import Type

from src.ppsspp.model.events.game.common import (
    GameStartEvent, GameQuitEvent, GamePauseEvent, GameResumeEvent
)

from src.ppsspp.model.events.other.log import LogEvent

from src.ppsspp.model.events.input.analog import InputAnalogEvent
from src.ppsspp.model.events.input.buttons import InputButtonsEvent

from src.ppsspp.model.events.cpu.common import CpuSteppingEvent, CpuResumeEvent



kLoggingEvents: set[Type] = {LogEvent}
kGameEvents: set[Type] = {GameStartEvent, GamePauseEvent, GameQuitEvent, GameResumeEvent}
kInputEvents: set[Type] = {InputAnalogEvent, InputButtonsEvent}
kCpuEvents: set[Type] = {CpuSteppingEvent, CpuResumeEvent}

kBroadcastEvents = kLoggingEvents.union(kGameEvents).union(kInputEvents).union(kCpuEvents)
