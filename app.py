import sys
from datetime import datetime
from pathlib import Path

import requests


# -- METHODS --

def load_config():
    """Reads configuration from the .env file"""

    script_dir = Path(__file__).parent
    env_file = script_dir / ".env"

    if not env_file.exists():
        print(f".env file not found in: {env_file}")
        print("\nPlease, create a .env file with:")
        print("JIRA_URL=https://your.jira.url")
        print("EMAIL=your@jira.username")
        print("API_TOKEN=your-api-token")
        return None

    # Read the variables from .env
    config = {}
    with open(env_file, 'r') as f:
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


def submit_worklog(config, issue_key, hours):
    """Submits the worklog to Jira"""

    seconds = int(hours * 3600)

    # Current timestamp in ISO format
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000+0000")

    payload = {
        "timeSpentSeconds": seconds,
        "comment": "Manual entry",
        "started": now
    }

    url = f"{config['JIRA_URL']}/rest/api/3/issue/{issue_key}/worklog"
    auth = (config['EMAIL'], config['API_TOKEN'])
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, auth=auth, headers=headers)

        if response.status_code == 200:
            h = int(hours)
            m = int((hours - h) * 60)
            print("Worklog successfully recorded!")
            print(f"   Issue: {issue_key}")
            print(f"   Time: {h}h {m}m")
        else:
            print(f"Error in recording (Status: {response.status_code})")
            print(f"   {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")


# -- MAIN --

def main():
    """Main function"""
    if len(sys.argv) != 2:
        print("Usage: tb [HISTL_number] [hours_also_with_decimals]")
        sys.exit(1)

    issue_key = sys.argv[1]

    hours = float(sys.argv[2])
    if hours <= 0:
        print("Invalid time. Use a positive decimal number.")
        sys.exit(1)

    config = load_config()
    if not config:
        sys.exit(1)

    submit_worklog(config, issue_key, hours)


if __name__ == "__main__":
    main()
