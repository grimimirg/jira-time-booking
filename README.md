# Jira Time Booker CLI

A simple command-line tool to quickly log work on Jira issues.

## 1\. Setup

Follow these steps to configure the script on your machine.

1.  **Download the Script**

    Save the `tb.py` script to a directory on your computer (e.g., `~/scripts/`).

2.  **Install Dependencies**

    The script requires a few Python libraries listed in `requirements.txt`. Open your terminal, navigate to the script's directory, and run:

    ```
    pip3 install -r requirements.txt
    ```

    _(The `-r` flag tells pip to install from a requirements file)_

3.  **Create a Configuration File**

    In the same directory where you saved `tb.py`, create a file named `jira.env` and add your Jira details:

    ```
    JIRA_URL=https://your-domain.atlassian.net
    EMAIL=your-email@example.com
    API_TOKEN=your-api-token-here
    ```

    > **Security Note**: This file contains sensitive credentials. Make sure to add `jira.env` to your project's `.gitignore` file to avoid accidentally committing it. You must generate an API Token from your Atlassian account settings. **Do not use your password.** You can create a token [here](https://id.atlassian.com/manage-profile/security/api-tokens).

4.  **Make the Script Executable**

    To run the script without typing `python3` each time, make it executable. In your terminal, run:

    ```
    chmod +x tb.py
    ```


## 2\. Usage Modes

The script can be used in two ways: Manual Logging or Automatic Timer.

### Mode 1: Manual Logging

Use this mode to log a specific amount of time on a Jira issue.

**Syntax:** `./tb.py ISSUE-KEY HOURS`

*   `ISSUE-KEY`: The key of the Jira issue (e.g., `PROJ-123`).
*   `HOURS`: The hours to log. Decimals are allowed.

#### Examples

```
# Log 2 hours
$ ./tb.py PROJ-123 2
Worklog submitted successfully!
   Issue: PROJ-123
   Time: 2h 0m
```

```
# Log 1 hour and 30 minutes
$ ./tb.py PROJ-456 1.5
Worklog submitted successfully!
   Issue: PROJ-456
   Time: 1h 30m
```

```
# Log 15 minutes
$ ./tb.py PROJ-789 0.25
Worklog submitted successfully!
   Issue: PROJ-789
   Time: 0h 15m
```

### Mode 2: Automatic Logging (Timer)

This mode acts like a "stopwatch". When you switch from one ticket to another, the script automatically calculates the elapsed time, logs it on the **previous** ticket, and starts the timer for the new one.

**Syntax:** `./tb.py NEW-ISSUE-KEY`

#### How It Works

1.  When you start working on a ticket, you run the script passing its key as the only argument.
2.  The script reads a local file to find out which ticket you were working on previously and at what time you started.
3.  It calculates the time elapsed between then and now.
4.  It automatically logs that time on the **previous** Jira ticket.
5.  Finally, it saves the new ticket and the current time as the new starting point for the next cycle.

#### Workflow Example

1.  **9:00 AM** - You start working on ticket `PROJ-101`. Run this command to "start the timer":

    ```
    ./tb.py PROJ-101
    ```

2.  **11:30 AM** - You've finished with `PROJ-101` and are now starting on ticket `PROJ-205`. Run the command:

    ```
    ./tb.py PROJ-205
    ```

    At this point, the script performs two actions:

    *   Automatically logs **2.5 hours** of work on ticket `PROJ-101`.
    *   Starts the timer for the new ticket, `PROJ-205`.
3.  **12:00 PM** - You're ready to work on `PROJ-300`.

    ```
    ./tb.py PROJ-300
    ```

    The script will log **0.5 hours** (30 minutes) of work on `PROJ-205` and set `PROJ-300` as the current ticket.


> **Note:** The very first time you use this mode on a ticket, it only saves it as the starting point. The first actual time log will occur on the **second** run of the script.

## 3\. Optional: Create a Global Command

To run the script from any directory without typing the full path, you can add an alias to your shell's configuration file (e.g., `.zshrc` or `.bashrc`).

1.  Open your config file (e.g., `nano ~/.zshrc`).
2.  Add the following line, replacing `/path/to/script/` with the **absolute path** to your script's folder.

    ```
    alias tb='/path/to/script/tb.py'
    ```

3.  Reload your shell (`source ~/.zshrc`) or open a new terminal tab.

Now you can use the `tb` command from anywhere on your system:

```
# Log time manually from any directory
$ tb PROJ-123 0.5

# Switch ticket using automatic mode
$ tb PROJ-456
```
