
class ConnectionTerminated(Exception):
    def __init__(self, *args):
        self._msgs = args
        Exception.__init__(self, args)
