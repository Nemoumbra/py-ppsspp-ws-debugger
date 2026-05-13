from dataclasses import dataclass


@dataclass(kw_only=True)
class VersionRequest:
    name: str | None = None
    version: str | None = None
