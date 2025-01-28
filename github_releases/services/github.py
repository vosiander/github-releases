from pathlib import Path
from typing import List, Dict, Optional
from loguru import logger
from github_releases.core.github_api import Tools
from github_releases.api.models import Tag

class GitHubService:
    def __init__(self, token: Optional[str] = None):
        self.github = Tools.Github(token=token)

    def txt_to_dict(self, file_path: str) -> dict:
        """Reads repository information from a text file."""
        repo_dict = {}
        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    repo, owner = line.split("/")
                    repo_dict[repo] = owner
        return repo_dict

    def txt_to_history(self, file_path: str) -> dict:
        """Reads tag history from a text file."""
        history_dict = {}
        try:
            with open(file_path, "r") as file:
                for line in file:
                    line = line.strip()
                    if line:
                        repo_owner, tag = line.split(":")
                        history_dict[repo_owner] = tag
        except FileNotFoundError:
            Path(file_path).touch()
        return history_dict

    def add_repository(self, repos_file: str, repository: str) -> bool:
        """Adds a new repository to the repositories file."""
        try:
            with open(repos_file, "a") as file:
                file.write(f"{repository}\n")
            return True
        except Exception as e:
            logger.error(f"Error adding repository: {e}")
            return False

    def get_repository_tag(self, owner: str, repo: str) -> Optional[Tag]:
        """Fetches the latest tag for a specific repository."""
        latest_release = self.github.get_latest_release(owner, repo)
        if latest_release:
            return Tag(
                repository=f"{owner}/{repo}",
                tag=latest_release["tag_name"],
                url=latest_release["html_url"]
            )
        return None

    def update_tags(self, repos_file: str, history_file: str) -> List[Tag]:
        """Updates tags for all repositories and returns the changes."""
        releases = self.txt_to_dict(repos_file)
        history_dict = self.txt_to_history(history_file)
        updated_tags = []
        new_history = []

        for owner, repo in releases.items():
            latest_release = self.github.get_latest_release(owner, repo)
            if latest_release:
                repo_key = f"{owner}/{repo}"
                previous_tag = history_dict.get(repo_key, "N/A")
                has_changed = previous_tag != latest_release["tag_name"]
                
                tag = Tag(
                    repository=repo_key,
                    tag=latest_release["tag_name"],
                    previous_tag=previous_tag,
                    changed=has_changed,
                    url=latest_release["html_url"]
                )
                updated_tags.append(tag)
                new_history.append(f"{repo_key}:{latest_release['tag_name']}")

        # Update history file
        with open(history_file, "w") as file:
            for entry in new_history:
                file.write(f"{entry}\n")

        return updated_tags
