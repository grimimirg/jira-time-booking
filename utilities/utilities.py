from datetime import datetime
from pathlib import Path

import requests
from requests import Response

from classes.payload import JiraRequestPayload
from utilities.constants import ENV_FILE_PATH, DATE_FORMAT


def submitWorklog(jiraEnvironment: dict[str, str], issueKey, hours):
    """Submits the worklog to Jira"""

    seconds = int(hours * 3600)
    now = datetime.utcnow().strftime(DATE_FORMAT)
    payload = JiraRequestPayload(seconds, "Development", now)

    try:
        response = sendToJira(jiraEnvironment, issueKey, payload)

        if response.status_code == 200:
            hours = int(hours)
            minutes = int((hours - hours) * 60)

            print("Worklog successfully recorded!")
            print(f"   Issue: {issueKey}")
            print(f"   Time: {hours}hours {minutes}minutes")
        else:
            print(f"Error in recording (Status: {response.status_code})")
            print(f"   {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")


def sendToJira(jiraEnvironment: dict[str, str], issueKey: str, payload: JiraRequestPayload) -> Response:
    """Sends the worklog to Jira"""

    url = f"{jiraEnvironment['JIRA_URL']}/rest/api/3/issue/{issueKey}/worklog"
    auth = (jiraEnvironment['EMAIL'], jiraEnvironment['API_TOKEN'])
    headers = {
        "Content-Type": "application/json"
    }

    return requests.post(url, json=payload.toJsonRequest(), auth=auth, headers=headers)


def loadJiraEnvironmentFile():
    """Reads configuration from the environment file"""

    if not ENV_FILE_PATH.exists():
        print(f"Environment file not found in: {ENV_FILE_PATH}")
        print("\nPlease, create an environment file with:")
        print("JIRA_URL=https://your.jira.url")
        print("EMAIL=your@jira.username")
        print("API_TOKEN=your-api-token")
        return None

    envVariables = getJiraEnvironmentVariables()

    # Check if all required variables are present
    required = ['JIRA_URL', 'EMAIL', 'API_TOKEN']
    if not all(key in envVariables for key in required):
        print("Environment file requires: JIRA_URL, EMAIL, API_TOKEN")
        return None

    return envVariables


def recordIssue(currentIssueFilePath: Path, endWorkDate: datetime, newIssueKey: str):
    """ Creates the new issue record and store it into the file """

    newIssueTimestamp = f"{endWorkDate.strftime(DATE_FORMAT)}"
    newFileContent = f"{newIssueKey}:{newIssueTimestamp}"

    with open(currentIssueFilePath, "w") as currentIssueFile:
        currentIssueFile.write(newFileContent)


# -- PRIVATES --


def getJiraEnvironmentVariables() -> dict[str, str]:
    config = {}

    with open(ENV_FILE_PATH, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            if '=' in line:
                key, value = line.split('=', 1)
                value = value.strip().strip('"').strip("'")
                config[key.strip()] = value

    return config
