from dataclasses import dataclass


@dataclass(kw_only=True)
class BroadcastConfigGetRequest:
    pass

# TODO: maybe wrap the dicts into objects?

@dataclass(kw_only=True)
class BroadcastConfigSetRequest:
    disallowed: dict[str, bool]
