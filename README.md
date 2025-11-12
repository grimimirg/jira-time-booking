# Jira Time Booker CLI

A simple command-line tool to quickly log work on Jira issues.

## 1\. Setup

1.  **Download the Script**
    
    Save the `tb.py` script to a directory on your computer (e.g., `~/scripts/`).
    
2.  **Install Dependencies**
    
    The script needs the `requests` library. Open your terminal and run:
    
    ```
    pip3 install requests
    ```
    
3.  **Create a Configuration File**
    
    In the same directory where you saved `tb.py`, create a file named `.env` and add your Jira details:
    
    ```
    # File: .env
    JIRA_URL=https://your-domain.atlassian.net
    EMAIL=your-email@example.com
    API_TOKEN=your-api-token-here
    ```
    
    > **Important**: You must generate an API Token from your Atlassian account settings. Do not use your password. You can create one [here](https://id.atlassian.com/manage-profile/security/api-tokens).
    
4.  **Make the Script Executable**
    
    Navigate to the script's directory and run:
    
    ```
    chmod +x tb.py
    ```
    

## 2\. Usage

To log time, run the script from its directory, followed by the **issue key** and the **hours** to log. Hours can be decimals.

**Syntax:** `./tb.py ISSUE-KEY HOURS`

#### Examples

```
# Log 2 hours
$ ./tb.py PROJ-123 2
Worklog submitted successfully!
   Issue: PROJ-123
   Time: 2h 0m

# Log 1 hour and 30 minutes
$ ./tb.py PROJ-456 1.5
Worklog submitted successfully!
   Issue: PROJ-456
   Time: 1h 30m

# Log 15 minutes
$ ./tb.py PROJ-789 0.25
Worklog submitted successfully!
   Issue: PROJ-789
   Time: 0h 15m
```

## 3\. (Optional) Create a Global Alias

To run the script from any directory, add an alias to your shell's configuration file (e.g., `.zshrc` or `.bashrc`).

1.  Open your config file (e.g., `nano ~/.bashrc`).
2.  Add the following line, replacing `/path/to/script/` with the **absolute path** to your script's folder.
    
    ```
    alias tb='/path/to/script/tb.py'
    ```
    
3.  Reload your shell (`source ~/.bashrc`) or open a new terminal.

Now you can use the `tb` command from anywhere:

```
$ tb PROJ-123 0.5
```
