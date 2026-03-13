# Admin Toolbox

A collection of administration utility tools for various services.

## Installation

```bash
pip install admin-toolbox
```

## Environment Variables

The following environment variables must be set (either in your environment or in a `.env` file):

- `JIRA_URL`: The full URL to your Jira instance (e.g., `https://yourdomain.atlassian.net`).
- `JIRA_PAT`: Your Personal Access Token for authentication.

## Usage

### Jira Issue Report

Generates a Markdown report of Jira issues assigned to the current user, grouped by status.

**Behavior:**
- Includes all issues that are currently in an **open** state (not Done/Cancelled).
- Includes issues in a **closed** state (Done) ONLY if they were resolved within the specified date range.
- Excludes all issues in the **Cancelled** status.

```bash
admin-toolbox jira-report --projects PROJ1 --projects PROJ2 --start-date 2024-01-01 --end-date 2024-03-31
```

**Options:**

- `--projects`, `-p`: (Required) List of Jira project keys to include. Can be specified multiple times.
- `--start-date`: (Optional) Start date for filtering closed/resolved tasks in `YYYY-MM-DD` format. Defaults to the first day of the current month.
- `--end-date`: (Optional) End date for filtering closed/resolved tasks in `YYYY-MM-DD` format. Defaults to the last day (Sunday) of the current week.
- `--output`, `-o`: (Optional) Output Markdown file name. Defaults to `jira_report.md`.

