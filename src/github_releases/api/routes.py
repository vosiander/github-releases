from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from sqlalchemy.orm import Session
from github_releases.api.models import Repository, Tag, TagList, ApiResponse, TagModel
from github_releases.services.github import GitHubService
from github_releases.core.config import settings, get_db

router = APIRouter()

def get_github_service(
    db: Session = Depends(get_db),
    token: Optional[str] = None
) -> GitHubService:
    return GitHubService(db=db, token=token)

@router.post("/repositories", response_model=ApiResponse)
async def add_repository(
    repo: Repository,
    github_service: GitHubService = Depends(get_github_service)
):
    """Add a new repository to the tracking list."""
    if github_service.add_repository(repo.repository):
        return ApiResponse(
            success=True,
            message=f"Repository {repo.repository} added successfully",
            data={"repository": repo.repository}
        )
    raise HTTPException(status_code=500, detail="Failed to add repository")

@router.post("/repositories/refresh", response_model=TagList)
async def refresh_repositories(
    github_service: GitHubService = Depends(get_github_service)
):
    """Fetch latest tags from GitHub and update history."""
    try:
        updated_tags = github_service.update_tags()
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
    db: Session = Depends(get_db)
):
    """Get all repositories and their tags from history."""
    try:
        tags = db.query(TagModel).all()
        tag_list = [
            Tag(
                repository=tag.repository,
                tag=tag.tag,
                previous_tag=tag.previous_tag,
                url=tag.url,
                changed=False  # Since this is historical data
            )
            for tag in tags
        ]
        return TagList(repositories=tag_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
