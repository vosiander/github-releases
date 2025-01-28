from pydantic import BaseModel, Field
from typing import List, Optional

class Repository(BaseModel):
    repository: str = Field(..., pattern=r"^[^/]+/[^/]+$", description="Repository in format owner/repo")

class Tag(BaseModel):
    repository: str
    tag: str
    previous_tag: Optional[str] = None
    changed: bool = False
    url: Optional[str] = None

class TagList(BaseModel):
    repositories: List[Tag]

class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None
