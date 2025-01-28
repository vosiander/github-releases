import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API Settings
    api_title: str = "GitHub Releases API"
    api_description: str = "API for managing GitHub repository releases and tags"
    api_version: str = "1.0.0"
    
    # File paths (set via CLI)
    repositories_file: Path = Path(os.getenv("GITHUB_RELEASES_REPOS_FILE", "repositories.txt"))
    history_file: Path = Path(os.getenv("GITHUB_RELEASES_HISTORY_FILE", "history.txt"))
    
    # GitHub settings
    github_token: Optional[str] = None
    
    # Server settings
    host: str = "127.0.0.1"
    port: int = 8000

    class Config:
        env_prefix = "GITHUB_RELEASES_"

settings = Settings()
