from dataclasses import dataclass

from ppsspp.model.ppsspp_objects.input.analog_stick import AnalogStick


# Fields like in InputAnalogEvent
@dataclass
class AnalogStickState:
    stick: AnalogStick
    x: float
    y: float
