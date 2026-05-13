from dataclasses import dataclass


@dataclass(kw_only=True)
class ReplayTimeGetRequest:
    pass


@dataclass(kw_only=True)
class ReplayTimeSetRequest:
    value: int
