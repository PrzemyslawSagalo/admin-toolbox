import os
from jira import JIRA

def fetch_and_export_jira_issues(projects, start_date, end_date, output_file):
    jira_url = os.environ.get('JIRA_URL')
    jira_pat = os.environ.get('JIRA_PAT')

    if not jira_url or not jira_pat:
        raise ValueError("Environment variables JIRA_URL and JIRA_PAT must be set.")

    # Authenticate with Jira
    jira = JIRA(server=jira_url, token_auth=jira_pat)
    
    # Construct JQL query
    project_list_str = ", ".join([f'"{p}"' for p in projects])
    
    # JQL with full filtration for open/closed tasks
    jql = (
        f'project in ({project_list_str}) AND '
        f'assignee = currentUser() AND '
        f'status != "Cancelled" AND '
        f'(status != "Done" OR (status = "Done" AND resolutiondate >= "{start_date}" AND resolutiondate <= "{end_date} 23:59")) '
        f'ORDER BY status ASC, created ASC'
    )

    # Fetch issues
    issues = jira.search_issues(jql, maxResults=False)
    
    if not issues:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("No issues found for the specified criteria.\n")
        return

    # Find the maximum status length for padding to ensure same size for all rows
    max_status_len = max(len(issue.fields.status.name) for issue in issues)

    # Write to Markdown file as a bulleted list
    with open(output_file, 'w', encoding='utf-8') as f:
        for issue in issues:
            status = issue.fields.status.name
            key = issue.key
            summary = issue.fields.summary
            
            # Pad status for consistent width
            padded_status = status.ljust(max_status_len)
            f.write(f"- [{padded_status}] {key} - {summary}\n")
