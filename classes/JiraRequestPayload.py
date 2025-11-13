from dataclasses import dataclass, field, asdict


@dataclass
class JiraRequestPayload:
    """Represents the JSON payload for a Jira worklog request."""
    timeSpentSeconds: int
    started: str

    # 'field' allows defining a default value.
    # This default is a standard Atlassian Document Format (ADF) comment.
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
        # asdict is a dataclass helper function
        return asdict(self)
