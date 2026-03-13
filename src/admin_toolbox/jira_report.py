import os
from datetime import datetime, timedelta
from jira import JIRA
from collections import defaultdict

def get_week_range(date_obj):
    # Determine the start (Monday) and end (Sunday) of the week
    start_of_week = date_obj - timedelta(days=date_obj.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    return (
        start_of_week.strftime('%d-%m-%Y'),
        end_of_week.strftime('%d-%m-%Y')
    )

def fetch_and_export_jira_issues(projects, start_date, end_date, output_file):
    jira_url = os.environ.get('JIRA_URL')
    jira_pat = os.environ.get('JIRA_PAT')

    if not jira_url or not jira_pat:
        raise ValueError("Environment variables JIRA_URL and JIRA_PAT must be set.")

    # Authenticate with Jira
    jira = JIRA(server=jira_url, token_auth=jira_pat)
    
    # Construct JQL query
    project_list_str = ", ".join([f'"{p}"' for p in projects])
    jql = (
        f'project in ({project_list_str}) AND '
        f'issuetype in (Task, Epic, Story) AND '
        f'created >= "{start_date}" AND created <= "{end_date}" AND '
        f'assignee = currentUser() ORDER BY created ASC'
    )

    # Fetch issues
    issues = jira.search_issues(jql, maxResults=False)
    grouped_issues = defaultdict(list)

    for issue in issues:
        created_date = datetime.strptime(issue.fields.created.split('T')[0], '%Y-%m-%d')
        week_start, week_end = get_week_range(created_date)
        week_key = f"{week_start} - {week_end}"
        grouped_issues[week_key].append(issue)

    # Sort weeks chronologically
    sorted_weeks = sorted(grouped_issues.keys(), key=lambda x: datetime.strptime(x.split(' - ')[0], '%d-%m-%Y'))

    # Write to Markdown file
    with open(output_file, 'w', encoding='utf-8') as f:
        # Table Header
        f.write("| Issues |\n")
        f.write("| --- |\n")
        
        for week in sorted_weeks:
            # Week Header Row
            f.write(f"| **Week: {week}** |\n")
            
            # Issue Rows
            for issue in grouped_issues[week]:
                key = issue.key
                summary = issue.fields.summary.replace('|', r'\|')
                status = issue.fields.status.name
                f.write(f"| {key} - {summary} - {status} |\n")
