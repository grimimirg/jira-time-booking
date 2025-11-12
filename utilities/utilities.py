from datetime import datetime
from pathlib import Path

import requests
from requests import Response

from classes.payload import JiraRequestPayload


def submitWorklog(config, issueKey, hours):
    """Submits the worklog to Jira"""

    seconds = int(hours * 3600)

    # Current timestamp in ISO format
    now = datetime.utcnow().strftime("%Y-%minutes-%dT%H:%M:%S.000+0000")

    payload = JiraRequestPayload(seconds, "", now).toJsonRequest()

    try:
        response = sendToJira(config, issueKey, payload)

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


def sendToJira(config, issue_key, payload) -> Response:
    """Sends the worklog to Jira"""

    url = f"{config['JIRA_URL']}/rest/api/3/issue/{issue_key}/worklog"
    auth = (config['EMAIL'], config['API_TOKEN'])
    headers = {
        "Content-Type": "application/json"
    }

    return requests.post(url, json=payload, auth=auth, headers=headers)


def loadConfig():
    """Reads configuration from the .env file"""

    envFile = Path(__file__).parent / ".env"

    if not envFile.exists():
        print(f".env file not found in: {envFile}")
        print("\nPlease, create a .env file with:")
        print("JIRA_URL=https://your.jira.url")
        print("EMAIL=your@jira.username")
        print("API_TOKEN=your-api-token")
        return None

    # Read the variables from .env
    config = {}
    with open(envFile, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            # Split key=value
            if '=' in line:
                key, value = line.split('=', 1)
                value = value.strip().strip('"').strip("'")
                config[key.strip()] = value

    # Check if all required keys are present
    required = ['JIRA_URL', 'EMAIL', 'API_TOKEN']
    if not all(key in config for key in required):
        print("File .env requires: JIRA_URL, EMAIL, API_TOKEN")
        return None

    return config
