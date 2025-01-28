from typing import Optional
import typer
import uvicorn
from fastapi import FastAPI
from rich import box
from rich.console import Console
from rich.table import Table
from rich.progress import track
import os
from loguru import logger
from pathlib import Path

from github_releases.core.config import settings
from github_releases.services.github import GitHubService
from github_releases.api.routes import router as api_router

app = typer.Typer()
api = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
)

# Add API routes
api.include_router(api_router, prefix="/api")

def create_rich_table() -> Table:
    """Create and return a Rich table for displaying release information."""
    table = Table(
        show_header=True,
        header_style="bold magenta",
        show_footer=False,
        row_styles=["none", "cyan"],
        pad_edge=False,
        box=box.SIMPLE_HEAD,
    )
    table.add_column("Repository", style="green")
    table.add_column("Tag", style="yellow")
    table.add_column("Previous Tag", style="red")
    table.add_column("Changed?", style="magenta")
    table.add_column("URL", style="blue")
    return table

@app.command()
def main(
    repos: Path = typer.Argument(..., help="Repositories to fetch"),
    token: Optional[str] = typer.Option(None, help="Github token"),
    history: Optional[Path] = typer.Option(None, help="Path to history file"),
    updated_only: bool = typer.Option(False, "--updated-only", help="Show only entries with changes"),
):
    """
    GitHub Releases CLI tool for checking repository releases.
    """
    console = Console()
    github_service = GitHubService(token=token)
    
    # Load history if specified
    if history and not history.exists():
        history.touch()

    # Get updated tags
    tags = github_service.update_tags(str(repos), str(history) if history else "history.txt")
    
    # Create and populate table
    table = create_rich_table()
    for tag in tags:
        if not updated_only or tag.changed:
            table.add_row(
                tag.repository,
                tag.tag,
                tag.previous_tag or "N/A",
                "X" if tag.changed else "-",
                tag.url or "N/A",
            )

    console.print(table)

@app.command()
def issues(
    issues_file: Path = typer.Argument(..., help="File containing issue URLs"),
    token: Optional[str] = typer.Option(None, help="Github token"),
):
    """
    Check GitHub issue statuses.
    """
    github = GitHubService(token=token)
    console = Console()

    # Set up the table for displaying issue information
    table = Table(
        show_header=True,
        header_style="bold magenta",
        show_footer=False,
        row_styles=["none", "dim"],
        pad_edge=False,
        box=box.SIMPLE_HEAD,
    )
    table.add_column("Issue URL", style="green")
    table.add_column("Status", style="yellow")
    table.add_column("Name", style="blue")
    table.add_column("Published At", style="cyan")
    table.add_column("Last Activity", style="magenta")
    table.add_column("Last Comment", style="red")

    # Read issues from file
    with open(issues_file, "r") as file:
        issues = [line.strip() for line in file if line.strip()]

    # Iterate through issues
    for issue_url in track(issues, description="Fetching issue statuses..."):
        issue_status = github.github.get_issue_status(issue_url)

        if issue_status:
            table.add_row(
                issue_url,
                issue_status["status"],
                issue_status["name"],
                issue_status["published_at"],
                issue_status["last_activity"],
                issue_status["last_comment"],
            )
        else:
            print(f"Failed to fetch issue status for {issue_url}.")

    console.print(table)

@app.command()
def serve(
    host: str = typer.Option(settings.host, help="Host to bind the server to"),
    port: int = typer.Option(settings.port, help="Port to run the server on"),
    token: Optional[str] = typer.Option(None, help="Github token for API operations"),
    repos_file: Path = typer.Option("repositories.txt", help="Path to repositories file"),
    history_file: Path = typer.Option("history.txt", help="Path to history file"),
):
    """
    Start the FastAPI server for API access.
    """
    # Set the configuration in environment
    if token:
        os.environ["GITHUB_RELEASES_GITHUB_TOKEN"] = token
    os.environ["GITHUB_RELEASES_REPOS_FILE"] = str(repos_file)
    os.environ["GITHUB_RELEASES_HISTORY_FILE"] = str(history_file)
        
    logger.info(f"Starting API server at http://{host}:{port}")
    logger.info("API documentation available at /docs")
    logger.info(f"Using repositories file: {repos_file}")
    logger.info(f"Using history file: {history_file}")
    
    # Create files if they don't exist
    repos_file.touch(exist_ok=True)
    history_file.touch(exist_ok=True)
    
    uvicorn.run(
        api,
        host=host,
        port=port,
        log_level="info"
    )

if __name__ == "__main__":
    app()
