from datetime import datetime, timezone
from pathlib import Path

import requests
from requests import Response

from classes.JiraRequestPayload import JiraRequestPayload
from utilities.Constants import ENV_FILE_PATH


def submitWorklog(jiraEnvironment: dict[str, str], issueKey: str, hours: float):
    """Calculates time in seconds and submits the worklog to Jira."""
    seconds = int(round(hours * 3600))

    # Use timezone-aware datetime and standard ISO format for max compatibility
    started_time = datetime.now(timezone.utc).isoformat()

    # The comment is now handled by a default in the dataclass
    payload = JiraRequestPayload(timeSpentSeconds=seconds, started=started_time)

    try:
        response = _sendToJira(jiraEnvironment, issueKey, payload)

        if response.status_code in (200, 201):
            h = int(hours)
            m = int(round((hours - h) * 60))
            print("Worklog successfully submitted!")
            print(f"   Issue: {issueKey}")
            print(f"   Time: {h}h {m}m")
        else:
            print(f"Error submitting worklog (Status: {response.status_code})")
            print(f"   Response: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")


def loadJiraEnvironmentFile() -> dict[str, str] | None:
    """Loads and validates the configuration from the .env file."""
    if not ENV_FILE_PATH.exists():
        print(f"Error: Environment file not found at: {ENV_FILE_PATH}")
        print("\nPlease create a 'jira.env' file with:")
        print("JIRA_URL=https://your-domain.atlassian.net")
        print("EMAIL=your-email@example.com")
        print("API_TOKEN=your-api-token")
        return None

    env_vars = _parse_env_file(ENV_FILE_PATH)
    required_keys = ['JIRA_URL', 'EMAIL', 'API_TOKEN']

    if not all(key in env_vars for key in required_keys):
        print(f"Error: Environment file must contain the keys: {', '.join(required_keys)}")
        return None

    return env_vars


def recordIssue(currentIssueFilePath: Path, endWorkDate: datetime, newIssueKey: str):
    """Saves the new issue and start timestamp to the state file."""
    # .isoformat() is standard and is correctly read by dateutil.parser
    new_timestamp = endWorkDate.isoformat()
    new_file_content = f"{newIssueKey}:{new_timestamp}"

    with open(currentIssueFilePath, "w") as f:
        f.write(new_file_content)


# -- Private Helper Functions --

def _sendToJira(jiraEnvironment: dict[str, str], issueKey: str, payload: JiraRequestPayload) -> Response:
    """Builds and sends the POST request to Jira."""
    url = f"{jiraEnvironment['JIRA_URL'].rstrip('/')}/rest/api/3/issue/{issueKey}/worklog"
    auth = (jiraEnvironment['EMAIL'], jiraEnvironment['API_TOKEN'])
    headers = {"Content-Type": "application/json"}

    return requests.post(
        url,
        json=payload.as_dict(),
        auth=auth,
        headers=headers,
        timeout=15  # Increased slightly for safety
    )


def _parse_env_file(path: Path) -> dict[str, str]:
    """Reads a .env file and parses it into a dictionary."""
    config = {}
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, value = line.split('=', 1)
                # Remove optional surrounding quotes
                value = value.strip().strip('"').strip("'")
                config[key.strip()] = value
    return config
