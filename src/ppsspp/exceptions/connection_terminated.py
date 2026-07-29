
class ConnectionTerminated(Exception):
    def __init__(self, *args):
        self._msgs = args
        super().__init__(args)
