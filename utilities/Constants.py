from pathlib import Path

# Defines the project's root folder path (the folder above 'utilities').
# This ensures that the .env and .txt files are located in the correct folder,
# regardless of where the script is run from.
PROJECT_ROOT = Path(__file__).parent.parent

CURRENT_ISSUE_FILE_PATH = PROJECT_ROOT / "current-issue.txt"
ENV_FILE_PATH = PROJECT_ROOT / "jira.env"
