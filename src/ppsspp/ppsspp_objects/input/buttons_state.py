from src.ppsspp.ppsspp_objects.input.button import Button


class ButtonsState:
    __slots__ = "_button_values"

    def __init__(self):
        self._button_values = {
            button.name: True
            for button in Button
        }
        pass

    def __getitem__(self, item: Button):
        return self._button_values[item.name]

    def __setitem__(self, key: Button, value: bool):
        self._button_values[key.name] = value

    def __setattr__(self, key: str, value):
        # This looks ugly
        if key == "_button_values":
            super().__setattr__("_button_values", value)
            return

        try:
            button = Button[key]  # string validation
            self[button] = value
        except KeyError:
            raise ValueError("Unknown PPSSPP button", key) from None

    def __getattr__(self, item: str):
        try:
            button = Button[item]  # string validation
            return self[button]
        except KeyError:
            raise ValueError("Unknown PPSSPP button", item) from None

    def to_dict(self):
        return self._button_values.copy()

    def from_dict(self, dictionary: dict):
        try:
            for name in self._button_values:
                self._button_values[name] = dictionary[name]
        except KeyError as e:
            raise ValueError("Missing buttons state parameter", e) from None
        unknown = set(dictionary.keys()) - set(self._button_values.keys())
        if unknown:
            raise ValueError("Unknown buttons state parameters", unknown)
