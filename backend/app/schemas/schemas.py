"""Pydantic schemas for API validation."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# Auth schemas
class UserRegister(BaseModel):
    """Schema for user registration."""

    username: str = Field(..., min_length=3, max_length=48)
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    """Schema for user login."""

    email: EmailStr
    password: str


class Token(BaseModel):
    """Schema for token response."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int = 3600


# User schemas
class UserBase(BaseModel):
    """Base user schema."""

    username: str
    email: EmailStr
    role: str = "author"


class UserOut(UserBase):
    """Schema for user output."""

    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Category schemas
class CategoryBase(BaseModel):
    """Base category schema."""

    name: str = Field(..., max_length=64)
    slug: str = Field(..., max_length=80)
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    """Schema for creating a category."""

    pass


class CategoryOut(CategoryBase):
    """Schema for category output."""

    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Tag schemas
class TagBase(BaseModel):
    """Base tag schema."""

    name: str = Field(..., max_length=48)
    slug: str = Field(..., max_length=64)


class TagCreate(TagBase):
    """Schema for creating a tag."""

    pass


class TagOut(TagBase):
    """Schema for tag output."""

    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Article schemas
class ArticleBase(BaseModel):
    """Base article schema."""

    title: str = Field(..., max_length=160)
    slug: str = Field(..., max_length=180)
    excerpt: Optional[str] = None
    content_md: Optional[str] = None
    content_html: Optional[str] = None
    status: str = "draft"
    category_id: Optional[int] = None


class ArticleCreate(ArticleBase):
    """Schema for creating an article."""

    tags: list[str] = []


class ArticleUpdate(BaseModel):
    """Schema for updating an article."""

    title: Optional[str] = Field(None, max_length=160)
    slug: Optional[str] = Field(None, max_length=180)
    excerpt: Optional[str] = None
    content_md: Optional[str] = None
    content_html: Optional[str] = None
    status: Optional[str] = None
    category_id: Optional[int] = None
    tags: Optional[list[str]] = None


class ArticleOut(ArticleBase):
    """Schema for article output."""

    id: int
    author_id: int
    published_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    tags: list[TagOut] = []

    model_config = ConfigDict(from_attributes=True)


class ArticleDetailOut(ArticleOut):
    """Schema for detailed article output with author info."""

    author: UserOut
    category: Optional[CategoryOut] = None

    model_config = ConfigDict(from_attributes=True)


# System schemas
class HealthCheck(BaseModel):
    """Schema for health check response."""

    status: str
    version: str


class VersionInfo(BaseModel):
    """Schema for version info response."""

    version: str
    build: str
