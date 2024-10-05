from typing import Annotated
import typer
from rich import box
from colorama import Fore, Style, init
from rich.console import Console
from rich.table import Table
from rich.progress import track
import os
from loguru import logger
from pathlib import Path
import requests

# Remove the default handler
logger.remove()

# Check the environment variable "DEBUG"
if os.getenv("DEBUG") == "1":
    # If DEBUG is set to "1", enable DEBUG level logging
    logger.add(lambda msg: print(msg, end=''), level="DEBUG")
else:
    # Otherwise, default to WARNING level logging
    logger.add(lambda msg: print(msg, end=''), level="WARNING")


class Github:
    def __init__(self, token=None):
        """
        Initialize the Github object. An optional token can be provided for authenticated requests.

        :param token: Github Personal Access Token (optional)
        """
        logger.debug(
            "Initializing Github object with token: {}",
            "provided" if token else "not provided",
        )
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {token}" if token else None,
            "Accept": "application/vnd.github.v3+json",
        }

    def get_latest_release(self, owner, repo):
        """
        Fetches the latest release from a Github repository.

        :param owner: The owner of the repository.
        :param repo: The name of the repository.
        :return: A dictionary containing release details, or None if the request fails.
        """
        url = f"{self.base_url}/repos/{owner}/{repo}/releases/latest"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            latest_release = response.json()
            return {
                "tag_name": latest_release["tag_name"],
                "name": latest_release["name"],
                "published_at": latest_release["published_at"],
                "html_url": latest_release["html_url"],
                "body": latest_release["body"],
            }
        else:
            return None


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



# Initialize colorama
init(autoreset=True)

# Create a Typer app
app = typer.Typer()

@app.command()
def main(
    repos: Path = Annotated[str, typer.Argument(help="Repositories to fetch")],
    token: str = typer.Option(None, help="Github token"),
):
    logger.debug("Received repos path: {}", repos)
    logger.debug("Repos type: {}", type(repos))
    github = Github(token=token)

    # Convert the file path to a dictionary of repositories
    releases = txt_to_dict(str(repos))
    console = Console()

    # Set up the table for displaying release information
    table = Table(
        show_header=True,
        header_style="bold magenta",
        show_footer=False,
        row_styles=["none", "dim"],
        pad_edge=False,
        box=box.SIMPLE_HEAD,
    )
    table.add_column("Repository", style="green")
    table.add_column("Tag", style="yellow")
    table.add_column("URL", style="blue")

    # Iterate through repositories
    for owner, repo in track(releases.items(), description="Finding releases..."):
        latest_release = github.get_latest_release(owner, repo)

        if latest_release:
            table.add_row(
                f"{owner}/{repo}",
                f"{latest_release['tag_name']}",
                f"https://github.com/{owner}/{repo}/releases/tag/{latest_release['tag_name']}",
            )
        else:
            print(
                f"{Fore.RED}Failed to fetch the latest release information for {owner}/{repo}.{Style.RESET_ALL}"
            )

    console.print(table)


if __name__ == "__main__":
    app()
