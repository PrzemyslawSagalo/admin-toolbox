# Admin Toolbox

A collection of administration utility tools for various services.

## Environment Variables

The following environment variables must be set (either in your environment or in a `.env` file):

- `JIRA_URL`: The full URL to your Jira instance (e.g., `https://yourdomain.atlassian.net`).
- `JIRA_PAT`: Your Personal Access Token for authentication.

## Usage

### Jira Issue Report

Generates a Markdown report of Jira issues (Tasks, Stories, Epics) assigned to the current user, grouped by week of creation.

```bash
admin-toolbox jira-report --projects PROJ1 --projects PROJ2 --start-date 2024-01-01 --end-date 2024-03-31
```

**Options:**

- `--projects`, `-p`: (Required) List of Jira project keys to include. Can be specified multiple times.
- `--start-date`: (Optional) Start date in `YYYY-MM-DD` format. Defaults to the first day of the current month.
- `--end-date`: (Optional) End date in `YYYY-MM-DD` format. Defaults to the current date.
- `--output`, `-o`: (Optional) Output Markdown file name. Defaults to `jira_report.md`.

