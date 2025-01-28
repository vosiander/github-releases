from typing import List, Optional
from loguru import logger
from sqlalchemy.orm import Session
from github_releases.core.github_api import Tools
from github_releases.api.models import Tag, RepositoryModel, TagModel

class GitHubService:
    def __init__(self, db: Session, token: Optional[str] = None):
        self.db = db
        self.github = Tools.Github(token=token)

    def get_repositories(self) -> List[str]:
        """Gets all repositories from the database."""
        repos = self.db.query(RepositoryModel).all()
        return [repo.repository for repo in repos]

    def add_repository(self, repository: str) -> bool:
        """Adds a new repository to the database."""
        try:
            repo = RepositoryModel(repository=repository)
            self.db.add(repo)
            self.db.commit()
            return True
        except Exception as e:
            logger.error(f"Error adding repository: {e}")
            self.db.rollback()
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

    def update_tags(self) -> List[Tag]:
        """Updates tags for all repositories and returns the changes."""
        updated_tags = []
        repositories = self.get_repositories()

        for repository in repositories:
            owner, repo = repository.split("/")
            latest_release = self.github.get_latest_release(owner, repo)
            
            if latest_release:
                # Get previous tag from database
                existing_tag = self.db.query(TagModel).filter(
                    TagModel.repository == repository
                ).first()

                previous_tag = existing_tag.tag if existing_tag else "N/A"
                has_changed = previous_tag != latest_release["tag_name"]

                # Create or update tag in database
                tag_model = existing_tag or TagModel(repository=repository)
                tag_model.previous_tag = previous_tag if has_changed else tag_model.previous_tag
                tag_model.tag = latest_release["tag_name"]
                tag_model.url = latest_release["html_url"]

                if not existing_tag:
                    self.db.add(tag_model)
                self.db.commit()

                # Create response object
                tag = Tag(
                    repository=repository,
                    tag=latest_release["tag_name"],
                    previous_tag=previous_tag,
                    changed=has_changed,
                    url=latest_release["html_url"]
                )
                updated_tags.append(tag)

        return updated_tags
