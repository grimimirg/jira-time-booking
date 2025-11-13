import sys
from datetime import datetime, timezone

from dateutil import parser

from utilities.constants import CURRENT_ISSUE_FILE_PATH
from utilities.utilities import submitWorklog, loadJiraEnvironmentFile, recordIssue


#  -- METHODS --

def manualSubmit(jiraEnvironment: dict[str, str]):
    issueKey = sys.argv[1]

    hours = float(sys.argv[2])
    if hours <= 0:
        print("Invalid time. Use a positive decimal number.")
        sys.exit(1)

    submitWorklog(jiraEnvironment, issueKey, hours)


def automaticSubmit(jiraEnvironment: dict[str, str]):
    newIssueKey = sys.argv[1]

    with open(CURRENT_ISSUE_FILE_PATH, "r") as currentIssueFile:
        currentIssueFileContent = currentIssueFile.read().strip()

    currentIssueKey, startTime = currentIssueFileContent.split(':', 1)

    startWorkDate = parser.parse(startTime)
    endWorkDate = datetime.now(timezone.utc)
    timeDifference = endWorkDate - startWorkDate

    secondsSpent = timeDifference.total_seconds()
    hoursSpent = secondsSpent / 3600

    # Submit the worklog on the previous issue
    submitWorklog(jiraEnvironment, currentIssueKey, hoursSpent)
    # Stores the new issue in the file
    recordIssue(CURRENT_ISSUE_FILE_PATH, endWorkDate, newIssueKey)


# -- MAIN --

def main():
    jiraEnvironment = loadJiraEnvironmentFile()
    if not jiraEnvironment:
        sys.exit(1)

    if len(sys.argv) == 1:
        automaticSubmit(jiraEnvironment)

    if len(sys.argv) == 2:
        manualSubmit(jiraEnvironment)


if __name__ == "__main__":
    main()
