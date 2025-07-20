from src.ppsspp.model.ppsspp_objects.input.analog import Analog


class AnalogState:
    __slots__ = ("stick", "x", "y")

    def __init__(self):
        self.stick = Analog.left
        self.x: float = 0.0
        self.y: float = 0.0

    def to_dict(self):
        return {
            "stick": self.stick.name,
            "x": self.x,
            "y": self.y
        }

    def from_dict(self, dictionary: dict):
        try:
            stick = dictionary["stick"]
            self.x = dictionary["x"]
            self.y = dictionary["y"]
        except KeyError as e:
            raise ValueError("Missing analog state parameter", e) from None
        try:
            self.stick = Analog[stick]
        except KeyError as e:
            raise ValueError(f"Unknown analog stick type '{e}'") from None
