"""Article routes."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user, require_role
from app.schemas.article import ArticleCreate, ArticleUpdate, ArticleOut, ArticleList
from app.services import article_service
from app.models.user import User


router = APIRouter(prefix="/articles", tags=["Articles"])


@router.get("/", response_model=List[ArticleList])
async def list_articles(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    author_id: Optional[int] = None,
    category_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    """List articles with optional filters."""
    articles = await article_service.get_articles(
        db,
        skip=skip,
        limit=limit,
        status=status,
        author_id=author_id,
        category_id=category_id,
    )
    return articles


@router.get("/{article_id}", response_model=ArticleOut)
async def get_article(
    article_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get article by ID."""
    article = await article_service.get_article_by_id(db, article_id)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )
    return article


@router.get("/slug/{slug}", response_model=ArticleOut)
async def get_article_by_slug(
    slug: str,
    db: AsyncSession = Depends(get_db),
):
    """Get article by slug."""
    article = await article_service.get_article_by_slug(db, slug)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )
    return article


@router.post("/", response_model=ArticleOut, status_code=status.HTTP_201_CREATED)
async def create_article(
    article_data: ArticleCreate,
    current_user: User = Depends(require_role("author")),
    db: AsyncSession = Depends(get_db),
):
    """Create a new article."""
    article = await article_service.create_article(db, article_data, current_user.id)
    return article


@router.put("/{article_id}", response_model=ArticleOut)
async def update_article(
    article_id: int,
    article_data: ArticleUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update article."""
    # Check if article exists
    article = await article_service.get_article_by_id(db, article_id)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )
    
    # Check permissions: author can edit own articles, editor/admin can edit any
    if current_user.role == "author" and article.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to edit this article",
        )
    
    article = await article_service.update_article(db, article_id, article_data)
    return article


@router.delete("/{article_id}")
async def delete_article(
    article_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete article."""
    # Check if article exists
    article = await article_service.get_article_by_id(db, article_id)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )
    
    # Check permissions: author can delete own articles, editor/admin can delete any
    if current_user.role == "author" and article.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this article",
        )
    
    await article_service.delete_article(db, article_id)
    return {"message": "Article deleted successfully"}
