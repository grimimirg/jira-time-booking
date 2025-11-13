import sys
from datetime import datetime, timezone

from dateutil import parser

from utilities.Constants import CURRENT_ISSUE_FILE_PATH
from utilities.Utilities import submitWorklog, loadJiraEnvironmentFile, recordIssue


#  -- METHODS --

def manualSubmit(jiraEnvironment: dict[str, str]):
    """Handles the manual logging of a worklog."""
    try:
        issueKey = sys.argv[1]
        hours = float(sys.argv[2])
    except (ValueError, IndexError):
        print("Error: Invalid arguments for manual mode.")
        _print_usage()
        sys.exit(1)

    if hours <= 0:
        print("Error: Hours must be a positive number.")
        sys.exit(1)

    submitWorklog(jiraEnvironment, issueKey, hours)


def automaticSubmit(jiraEnvironment: dict[str, str]):
    """
    Handles automatic logging: closes the previous worklog
    and starts the timer for the new one.
    """
    try:
        newIssueKey = sys.argv[1]
    except IndexError:
        print("Error: Missing issue key for automatic mode.")
        _print_usage()
        sys.exit(1)

    now = datetime.now(timezone.utc)

    # Handle the case where the file doesn't exist (first run)
    try:
        with open(CURRENT_ISSUE_FILE_PATH, "r") as currentIssueFile:
            currentIssueFileContent = currentIssueFile.read().strip()
    except FileNotFoundError:
        print(f"Starting timer for new issue: {newIssueKey}")
        recordIssue(CURRENT_ISSUE_FILE_PATH, now, newIssueKey)
        return  # Exit after starting the first timer

    # If the file exists, proceed with normal logic
    currentIssueKey, startTimeStr = currentIssueFileContent.split(':', 1)

    startWorkDate = parser.parse(startTimeStr)
    timeDifference = now - startWorkDate

    # Calculate hours and submit to Jira
    hoursSpent = timeDifference.total_seconds() / 3600
    print(f"Stopping timer for {currentIssueKey}...")
    submitWorklog(jiraEnvironment, currentIssueKey, hoursSpent)

    # Record the new issue as the current one
    print(f"\nStarting timer for new issue: {newIssueKey}")
    recordIssue(CURRENT_ISSUE_FILE_PATH, now, newIssueKey)


def _print_usage():
    """Prints usage instructions to the console."""
    print("\nUsage:")
    print(f"  Automatic mode: python {sys.argv[0]} <NEW_ISSUE_KEY>")
    print(f"  Manual mode:    python {sys.argv[0]} <ISSUE_KEY> <HOURS_TO_LOG>")


# -- MAIN --

def main():
    """Main entry point for the script."""
    jiraEnvironment = loadJiraEnvironmentFile()
    if not jiraEnvironment:
        sys.exit(1)

    # The sys.argv list includes the script name as its first element.
    # len=1: script only, no args
    # len=2: script + 1 arg (automatic mode)
    # len=3: script + 2 args (manual mode)
    num_args = len(sys.argv)

    if num_args == 2:
        automaticSubmit(jiraEnvironment)
    elif num_args == 3:
        manualSubmit(jiraEnvironment)
    else:
        _print_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
