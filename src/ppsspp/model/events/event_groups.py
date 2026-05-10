from typing import Type

from ppsspp.model.events.game.common import (
    GameStartEvent, GameQuitEvent, GamePauseEvent, GameResumeEvent
)
from ppsspp.model.events.other.log import LogEvent
from ppsspp.model.events.input.analog import InputAnalogEvent
from ppsspp.model.events.input.buttons import InputButtonsEvent
from ppsspp.model.events.cpu.common import CpuSteppingEvent, CpuResumeEvent


kLoggingEvents: set[Type] = {LogEvent}
kGameEvents: set[Type] = {GameStartEvent, GamePauseEvent, GameQuitEvent, GameResumeEvent}
kInputEvents: set[Type] = {InputAnalogEvent, InputButtonsEvent}
kCpuEvents: set[Type] = {CpuSteppingEvent, CpuResumeEvent}

kBroadcastEvents = kLoggingEvents.union(kGameEvents).union(kInputEvents).union(kCpuEvents)
