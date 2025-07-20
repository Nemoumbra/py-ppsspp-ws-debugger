
class GameInfo:
    __slots__ = ("id", "version", "title")

    def __init__(self):
        self.id: str = ""
        self.version: str = ""
        self.title: str = ""

    def to_dict(self):
        return {
            "id": self.id,
            "version": self.version,
            "title": self.title,
        }

    def from_dict(self, dictionary):
        try:
            self.id = dictionary["id"]
            self.version = dictionary["version"]
            self.title = dictionary["title"]
        except KeyError as e:
            raise ValueError("Missing game info parameter", e) from None
