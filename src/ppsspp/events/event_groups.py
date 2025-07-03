
from typing import Type

from src.ppsspp.events.game.game_start import GameStartEvent
from src.ppsspp.events.game.game_quit import GameQuitEvent
from src.ppsspp.events.game.game_pause import GamePauseEvent
from src.ppsspp.events.game.game_resume import GameResumeEvent

from src.ppsspp.events.other.log import LogEvent

from src.ppsspp.events.input.analog.input_analog import InputAnalogEvent
from src.ppsspp.events.input.buttons.input_buttons import InputButtonsEvent

from src.ppsspp.events.cpu.cpu_stepping import SteppingEvent
from src.ppsspp.events.cpu.cpu_resume import ResumedEvent

kLoggingEvents: set[Type] = {LogEvent}
kGameEvents: set[Type] = {GameStartEvent, GamePauseEvent, GameQuitEvent, GameResumeEvent}
kInputEvents: set[Type] = {InputAnalogEvent, InputButtonsEvent}
kCpuEvents: set[Type] = {SteppingEvent, ResumedEvent}

kBroadcastEvents = kLoggingEvents.union(kGameEvents).union(kInputEvents).union(kCpuEvents)
