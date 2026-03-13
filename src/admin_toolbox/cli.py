import click
from datetime import datetime
from dotenv import load_dotenv
from admin_toolbox.jira_report import fetch_and_export_jira_issues

# Load environment variables from .env file
load_dotenv()

@click.group()
def main():
    """Admin Toolbox - A collection of utility tools."""
    pass

@main.command()
@click.option('--start-date', type=str, help='Start date in YYYY-MM-DD format (default: 1st of current month)')
@click.option('--end-date', type=str, help='End date in YYYY-MM-DD format (default: today)')
@click.option('--projects', '-p', multiple=True, required=True, help='Jira project keys/names to include')
@click.option('--output', '-o', default='jira_report.md', help='Output Markdown file name')
def jira_report(start_date, end_date, projects, output):
    """Generate a grouped Jira issues report exported to Markdown."""
    
    today = datetime.now()
    if not start_date:
        start_date = today.replace(day=1).strftime('%Y-%m-%d')
    if not end_date:
        end_date = today.strftime('%Y-%m-%d')

    try:
        fetch_and_export_jira_issues(projects, start_date, end_date, output)
        click.echo(f"Report successfully generated: {output}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)

if __name__ == '__main__':
    main()
