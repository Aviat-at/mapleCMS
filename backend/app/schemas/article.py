"""Article schemas."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

from app.schemas.user import UserOut
from app.schemas.category import CategoryOut
from app.schemas.tag import TagOut


class ArticleBase(BaseModel):
    """Base article schema."""
    title: str = Field(..., min_length=1, max_length=160)
    excerpt: Optional[str] = None
    content_md: Optional[str] = None
    content_html: Optional[str] = None
    status: str = Field(default="draft", pattern="^(draft|published|archived)$")
    category_id: Optional[int] = None
    meta_json: Dict[str, Any] = Field(default_factory=dict)


class ArticleCreate(ArticleBase):
    """Schema for creating a new article."""
    tag_ids: List[int] = Field(default_factory=list)


class ArticleUpdate(BaseModel):
    """Schema for updating an article."""
    title: Optional[str] = Field(None, min_length=1, max_length=160)
    excerpt: Optional[str] = None
    content_md: Optional[str] = None
    content_html: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(draft|published|archived)$")
    category_id: Optional[int] = None
    tag_ids: Optional[List[int]] = None
    meta_json: Optional[Dict[str, Any]] = None


class ArticleList(BaseModel):
    """Schema for article list item."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    slug: str
    excerpt: Optional[str]
    status: str
    author_id: int
    category_id: Optional[int]
    published_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime


class ArticleOut(ArticleBase):
    """Schema for article output with full details."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    author_id: int
    published_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
