
class QueueClosedError(Exception):
    def __init__(self, *args):
        self._msgs = args
        ValueError.__init__(self, args)
