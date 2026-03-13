import click
from datetime import datetime, timedelta
from dotenv import load_dotenv
from admin_toolbox.jira_report import fetch_and_export_jira_issues

# Load environment variables from .env file
load_dotenv()

@click.group()
def main():
    """Admin Toolbox - A collection of utility tools."""
    pass

@main.command()
@click.option('--start-date', type=str, help='Start date for filtering CLOSED tasks (resolved >= date) in YYYY-MM-DD format (default: 1st of current month)')
@click.option('--end-date', type=str, help='End date for filtering CLOSED tasks (resolved <= date) in YYYY-MM-DD format (default: end of current week)')
@click.option('--projects', '-p', multiple=True, required=True, help='Jira project keys/names to include')
@click.option('--output', '-o', default='jira_report.md', help='Output Markdown file name')
def jira_report(start_date, end_date, projects, output):
    """Generate a status-grouped Jira issues report. 
    Includes all assigned open tasks and closed tasks resolved within the specified date range.
    """
    
    today = datetime.now()
    if not start_date:
        start_date = today.replace(day=1).strftime('%Y-%m-%d')
    if not end_date:
        # Calculate the end of the current week (Sunday)
        end_of_week = today + timedelta(days=(6 - today.weekday()))
        end_date = end_of_week.strftime('%Y-%m-%d')

    try:
        fetch_and_export_jira_issues(projects, start_date, end_date, output)
        click.echo(f"Report successfully generated: {output}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)

if __name__ == '__main__':
    main()
