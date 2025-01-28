from fastapi import APIRouter, HTTPException, Depends
from pathlib import Path
from typing import Optional
from github_releases.api.models import Repository, Tag, TagList, ApiResponse
from github_releases.services.github import GitHubService

router = APIRouter()

def get_github_service(token: Optional[str] = None):
    return GitHubService(token=token)

@router.post("/repositories", response_model=ApiResponse)
async def add_repository(
    repo: Repository,
    repos_file: str = "repositories.txt",
    github_service: GitHubService = Depends(get_github_service)
):
    """Add a new repository to the tracking list."""
    if github_service.add_repository(repos_file, repo.repository):
        return ApiResponse(
            success=True,
            message=f"Repository {repo.repository} added successfully",
            data={"repository": repo.repository}
        )
    raise HTTPException(status_code=500, detail="Failed to add repository")

@router.post("/repositories/refresh", response_model=TagList)
async def refresh_repositories(
    repos_file: str = "repositories.txt",
    history_file: str = "history.txt",
    github_service: GitHubService = Depends(get_github_service)
):
    """Fetch latest tags from GitHub and update history."""
    try:
        updated_tags = github_service.update_tags(repos_file, history_file)
        return TagList(repositories=updated_tags)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/repositories/{owner}/{repo}/tag", response_model=Tag)
async def get_repository_tag(
    owner: str,
    repo: str,
    github_service: GitHubService = Depends(get_github_service)
):
    """Get the latest tag for a specific repository."""
    tag = github_service.get_repository_tag(owner, repo)
    if tag:
        return tag
    raise HTTPException(status_code=404, detail=f"No tag found for repository {owner}/{repo}")

@router.get("/repositories/history", response_model=TagList)
async def get_history(
    history_file: str = "history.txt",
    github_service: GitHubService = Depends(get_github_service)
):
    """Get all repositories and their tags from history."""
    try:
        history_dict = github_service.txt_to_history(history_file)
        tags = [
            Tag(
                repository=repo_owner,
                tag=tag,
            )
            for repo_owner, tag in history_dict.items()
        ]
        return TagList(repositories=tags)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
