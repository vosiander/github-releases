from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from sqlalchemy import Column, String, Boolean, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# SQLAlchemy Models
class RepositoryModel(Base):
    __tablename__ = "repositories"
    
    repository = Column(String, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TagModel(Base):
    __tablename__ = "tags"
    
    repository = Column(String, primary_key=True)
    tag = Column(String, nullable=False)
    previous_tag = Column(String, nullable=True)
    url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Pydantic Models for API
class Repository(BaseModel):
    repository: str = Field(..., pattern=r"^[^/]+/[^/]+$", description="Repository in format owner/repo")

    class Config:
        from_attributes = True

class Tag(BaseModel):
    repository: str
    tag: str
    previous_tag: Optional[str] = None
    changed: bool = False
    url: Optional[str] = None

    class Config:
        from_attributes = True

class TagList(BaseModel):
    repositories: List[Tag]

class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None
