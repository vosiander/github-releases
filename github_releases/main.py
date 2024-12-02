from typing import Optional
import typer
from rich import box
from colorama import Fore, Style, init
from rich.console import Console
from rich.table import Table
from rich.progress import track
import os
from loguru import logger
from pathlib import Path
from github_releases.github_api import Tools

# Remove the default handler
logger.remove()

# Check the environment variable "DEBUG"
if os.getenv("DEBUG") == "1":
    # If DEBUG is set to "1", enable DEBUG level logging
    logger.add(lambda msg: print(msg, end=''), level="DEBUG")
else:
    # Otherwise, default to WARNING level logging
    logger.add(lambda msg: print(msg, end=''), level="WARNING")


def txt_to_dict(file_path: str) -> dict:
    """
    Reads a text file containing repository information and converts it to a dictionary.

    Each line in the file should contain a repository name followed by the owner's name,
    separated by a slash (e.g., 'repo_name/owner_name').

    Args:
        file_path (str): Path to the text file containing the repository data.

    Returns:
        dict: A dictionary where the keys are repository names and the values are their corresponding owners.
    """
    repo_dict = {}
    with open(file_path, "r") as file:
        for line in file:
            # Remove any surrounding whitespace or newline characters
            line = line.strip()
            if line:  # Skip empty lines
                repo, owner = line.split("/")
                repo_dict[repo] = owner
    return repo_dict

def txt_to_history(file_path: str) -> dict:
    """
        Reads a text file containing repository information and converts it to a dictionary.

        Each line in the file should contain a repository name followed by the owner's name,
        separated by a slash (e.g., 'repo_name/owner_name').

        Args:
            file_path (str): Path to the text file containing the repository data.

        Returns:
            dict: A dictionary where the keys are repository names and the values are their corresponding owners.
        """
    repo_dict = {}
    with open(file_path, "r") as file:
        for line in file:
            # Remove any surrounding whitespace or newline characters
            line = line.strip()
            if line:  # Skip empty lines
                repo_owner, tag = line.split(":")
                repo_dict[repo_owner] = tag
    return repo_dict


def txt_to_list(file_path: str) -> list:
    """
    Reads a text file containing issue URLs and converts it to a list.

    Each line in the file should contain a full issue URL.

    Args:
        file_path (str): Path to the text file containing the issue URLs.

    Returns:
        list: A list of issue URLs.
    """
    issue_list = []
    with open(file_path, "r") as file:
        for line in file:
            # Remove any surrounding whitespace or newline characters
            line = line.strip()
            if line:  # Skip empty lines
                issue_list.append(line)
    return issue_list


# Initialize colorama
init(autoreset=True)

# Create a Typer app
app = typer.Typer()

@app.command()
def main(
    repos: Path = typer.Argument(..., help="Repositories to fetch"),
    token: Optional[str] = typer.Option(None, help="Github token"),
    history: Optional[Path] = typer.Option(None, help="Path to history file"),
):
    logger.debug("Received repos path: {}", repos)
    logger.debug("Repos type: {}", type(repos))
    github = Tools.Github(token=token)

    # Convert the file path to a dictionary of repositories
    releases = txt_to_dict(str(repos))
    console = Console()

    # Load history if specified
    history_dict = {}
    if history:
        if not history.exists():
            history.touch()  # Create the file if it does not exist
        history_dict = txt_to_history(str(history))

    # Set up the table for displaying release information
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

    # Iterate through repositories
    new_history = []
    for owner, repo in track(releases.items(), description="Finding releases..."):
        latest_release = github.get_latest_release(owner, repo)
        previous_tag = history_dict.get(f"{owner}/{repo}", "N/A")

        if latest_release:
            table.add_row(
                f"{owner}/{repo}",
                f"{latest_release['tag_name']}",
                previous_tag,
                "X" if previous_tag != latest_release['tag_name'] else "-",
                f"https://github.com/{owner}/{repo}/releases/tag/{latest_release['tag_name']}",
            )
            new_history.append(f"{owner}/{repo}:{latest_release['tag_name']}")
        else:
            print(
                f"{Fore.RED}Failed to fetch the latest release information for {owner}/{repo}.{Style.RESET_ALL}"
            )

    console.print(table)

    # Ask user if they want to write new history to file
    if history:
        if typer.confirm("Do you want to write the changes to the history file?"):
            with open(history, "w") as file:
                for entry in new_history:
                    file.write(f"{entry}\n")
        else:
            console.print("No changes were made to the history file.")


@app.command()
def issues(
    issues_file: Path = typer.Argument(..., help="File containing issue URLs"),
    token: Optional[str] = typer.Option(None, help="Github token"),
):
    logger.debug("Received issues file path: {}", issues_file)
    logger.debug("Issues file type: {}", type(issues_file))
    github = Tools.Github(token=token)

    # Convert the file path to a list of issue URLs
    issues = txt_to_list(str(issues_file))
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

    # Iterate through issues
    for issue_url in track(issues, description="Fetching issue statuses..."):
        issue_status = github.get_issue_status(issue_url)

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
            print(
                f"{Fore.RED}Failed to fetch issue status for {issue_url}.{Style.RESET_ALL}"
            )

    console.print(table)


if __name__ == "__main__":
    app()
