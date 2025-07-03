
class EventParseError(ValueError):
    def __init__(self, *args):
        self._msgs = args
        ValueError.__init__(self, args)
