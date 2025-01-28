from typing import Optional, List
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

from github_releases.core.config import settings, get_db
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

def import_repositories_from_file(path: Path, github_service: GitHubService):
    """Import repositories from a text file into the database."""
    logger.info(f"Importing repositories from {path}")
    with open(path, "r") as file:
        for line in file:
            repo = line.strip().strip('-').strip()
            if repo:
                logger.info(f"Adding repository: {repo}")
                github_service.add_repository(repo)

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
    token: Optional[str] = typer.Option(None, help="Github token"),
    updated_only: bool = typer.Option(False, "--updated-only", help="Show only entries with changes"),
    prefill_txt: Optional[Path] = typer.Option(None, help="Import repositories from text file"),
):
    """
    GitHub Releases CLI tool for checking repository releases.
    """
    console = Console()
    db = next(get_db())
    github_service = GitHubService(db=db, token=token)
    
    try:
        # Import repositories if prefill_txt is provided
        if prefill_txt:
            import_repositories_from_file(prefill_txt, github_service)
        
        # Get updated tags
        tags = github_service.update_tags()
        
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
    finally:
        db.close()

@app.command()
def issues(
    issues_file: Path = typer.Argument(..., help="File containing issue URLs"),
    token: Optional[str] = typer.Option(None, help="Github token"),
):
    """
    Check GitHub issue statuses.
    """
    db = next(get_db())
    github = GitHubService(db=db, token=token)
    console = Console()

    try:
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
    finally:
        db.close()

@app.command()
def serve(
    host: str = typer.Option(settings.host, help="Host to bind the server to"),
    port: int = typer.Option(settings.port, help="Port to run the server on"),
    token: Optional[str] = typer.Option(None, help="Github token for API operations"),
    prefill_txt: Optional[Path] = typer.Option(None, help="Import repositories from text file"),
):
    """
    Start the FastAPI server for API access.
    """
    # Set the configuration in environment
    if token:
        os.environ["GITHUB_RELEASES_GITHUB_TOKEN"] = token

    # Import repositories if prefill_txt is provided
    if prefill_txt:
        db = next(get_db())
        github_service = GitHubService(db=db, token=token)
        try:
            import_repositories_from_file(prefill_txt, github_service)
        finally:
            db.close()

    logger.info(f"Starting API server at http://{host}:{port}")
    logger.info("API documentation available at /docs")

    uvicorn.run(
        api,
        host=host,
        port=port,
        log_level="info"
    )

if __name__ == "__main__":
    app()
