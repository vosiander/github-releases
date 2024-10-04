import typer
from rich import box
from colorama import Fore, Style, init
from rich.console import Console
from rich.table import Table
from rich.progress import track
from loguru import logger
import requests

class Github:
    def __init__(self, token=None):
        """
        Initialize the Github object. An optional token can be provided for authenticated requests.

        :param token: Github Personal Access Token (optional)
        """
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {token}" if token else None,
            "Accept": "application/vnd.github.v3+json"
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
                'tag_name': latest_release['tag_name'],
                'name': latest_release['name'],
                'published_at': latest_release['published_at'],
                'html_url': latest_release['html_url'],
                'body': latest_release['body']
            }
        else:
            return None

def txt_to_dict(file_path):
    repo_dict = {}
    with open(file_path, 'r') as file:
        for line in file:
            # Remove any surrounding whitespace or newline characters
            line = line.strip()
            if line:  # Skip empty lines
                repo, owner = line.split('/')
                repo_dict[repo] = owner
    return repo_dict

# Initialize colorama
init(autoreset=True)

# Create a Typer app
app = typer.Typer()

@app.command()
def main(token: str = typer.Option(None, help="Github token"),
         repos: str = typer.Option(..., help="Repositories to fetch")):
    github = Github(token=token)

    # Convert the file path to a dictionary of repositories
    releases = txt_to_dict(repos)
    console = Console()

    # Set up the table for displaying release information
    table = Table(show_header=True, header_style="bold magenta", show_footer=False, row_styles=["none", "dim"], pad_edge=False, box=box.SIMPLE_HEAD)
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
            print(f"{Fore.RED}Failed to fetch the latest release information for {owner}/{repo}.{Style.RESET_ALL}")

    console.print(table)

if __name__ == "__main__":
    app()
