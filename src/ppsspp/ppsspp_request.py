from typing import Any
import json


class PPSSPPRequest:
    """
    Create from the event name and add the needed arguments

    Example::

        request = PPSSPPRequest("sample_event")
        request.add("do", value0, arg2=value1, name=value3, test=False, smth=value4)
        request.add("class", value5)
    """
    def __init__(self, event: str):
        self._args: dict = {"event": event}

    def add(self, name: str | None = None, value: Any | None = None, /, **kwargs):
        """
        Appends the arguments to the request. If some of the arguments can't be added as kwargs, they can be included
        manually, one-by-one, using the first 2 positional arguments.

        :param name: the name of the special argument
        :param value: the value of the special argument
        :param kwargs: the pack of arguments which are not reserved Python identifiers
        :return:
        """
        if (name is not None) and (value is not None):
            self._args[name] = value
        self._args.update(kwargs)

    def set_ticket(self, ticket: str):
        self._args["ticket"] = ticket

    def get_ticket(self) -> str | None:
        """
        Fetches the ticket from the request, if present.
        :return: the ticket or None
        """
        return self._args.get("ticket")

    def __str__(self):
        return json.dumps(self._args)
