from dataclasses import dataclass


class Register:
    pass


@dataclass
class RegisterCategory:
    id: int
    name: str
    register_names: list[str]
    uint_values: list[int]
    float_values: list[str]
