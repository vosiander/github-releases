import os
from typing import Optional
from pydantic_settings import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from github_releases.api.models import Base

class Settings(BaseSettings):
    # API Settings
    api_title: str = "GitHub Releases API"
    api_description: str = "API for managing GitHub repository releases and tags"
    api_version: str = "1.0.0"
    
    # Database settings
    database_url: str = os.getenv("GITHUB_RELEASES_DATABASE_URL", "sqlite:///github_releases.db")
    
    # GitHub settings
    github_token: Optional[str] = None
    
    # Server settings
    host: str = "127.0.0.1"
    port: int = 8000

    class Config:
        env_prefix = "GITHUB_RELEASES_"

settings = Settings()

# Database setup
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
