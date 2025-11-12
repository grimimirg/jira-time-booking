import json


class JiraRequestPayload:
    timeSpentSeconds: int
    comment: str
    started: str

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, timeSpentSeconds, comment, started):
        self.timeSpentSeconds = timeSpentSeconds
        self.comment = comment
        self.started = started

    def toJsonRequest(self):
        return json.dump(self.__dict__)
