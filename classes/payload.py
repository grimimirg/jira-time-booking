import json


class JiraRequestPayload:
    def __init__(self, timeSpentSeconds, comment, started):
        self.timeSpentSeconds = timeSpentSeconds
        self.comment = comment
        self.started = started

    def toJsonRequest(self):
        return {
            "timeSpentSeconds": self.timeSpentSeconds,
            "comment": self.comment,
            "started": self.started
        }
