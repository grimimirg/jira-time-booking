from dataclasses import dataclass, field, asdict


@dataclass
class JiraRequestPayload:
    """Represents the JSON payload for a Jira worklog request."""
    timeSpentSeconds: int
    started: str

    comment: dict = field(default_factory=lambda: {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "Development"
                    }
                ]
            }
        ]
    })

    def as_dict(self) -> dict:
        """Converts the class instance to a dictionary for the JSON request."""
        return asdict(self)
