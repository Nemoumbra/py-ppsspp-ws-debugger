from typing import Any
import json


class PPSSPPRequest:
    """
    Create from the event name and add the needed arguments
    """
    def __init__(self, event: str):
        self._args: dict = {"event": event}

    def add(self, name: str | None = None, value: Any | None = None, /, **kwargs):
        if (name is not None) and (value is not None):
            self._args[name] = value
        self._args.update(kwargs)

    def set_ticket(self, ticket: str):
        self._args["ticket"] = ticket

    def get_ticket(self):
        return self._args.get("ticket")

    def __str__(self):
        return json.dumps(self._args)
