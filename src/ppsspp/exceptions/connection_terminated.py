
class ConnectionTerminated(Exception):
    def __init__(self):
        super().__init__("PPSSPP connection was closed")
