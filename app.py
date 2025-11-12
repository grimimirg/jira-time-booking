import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dateutil import parser

from utilities.utilities import submitWorklog, loadConfig


#  -- METHODS --

def manualSubmit(config: dict[Any, Any]):
    issueKey = sys.argv[1]

    hours = float(sys.argv[2])
    if hours <= 0:
        print("Invalid time. Use a positive decimal number.")
        sys.exit(1)

    submitWorklog(config, issueKey, hours)


def automaticSubmit(config: dict[Any, Any]):
    newIssueKey = sys.argv[1]

    currentIssueFilePath = Path(__file__).parent / "current_issue.txt"

    with open(currentIssueFilePath, "r") as currentIssueFile:
        file_content = currentIssueFile.read().strip()

    issueKey, startTimeStr = file_content.split(':', 1)

    startWorkDate = parser.parse(startTimeStr)

    endWorkDate = datetime.now(timezone.utc)

    timeDifference = endWorkDate - startWorkDate

    secondsSpent = timeDifference.total_seconds()
    hoursSpent = secondsSpent / 3600

    newIssueTimestamp = f"{endWorkDate.strftime('%Y-%m-%dT%H:%M:%S')}.000+0000"
    newFileContent = f"{newIssueKey}:{newIssueTimestamp}"

    with open(currentIssueFilePath, "w") as currentIssueFile:
        currentIssueFile.write(newFileContent)

    submitWorklog(config, issueKey, hoursSpent)


# -- MAIN --

def main():
    config = loadConfig()
    if not config:
        sys.exit(1)

    if len(sys.argv) == 1:
        automaticSubmit(config)

    if len(sys.argv) == 2:
        manualSubmit(config)


if __name__ == "__main__":
    main()
