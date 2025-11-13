"""Articles API routes."""
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import Article, Tag
from app.schemas.schemas import (ArticleCreate, ArticleDetailOut, ArticleOut,
                                 ArticleUpdate)

router = APIRouter(prefix="/articles", tags=["Articles"])


@router.get("/", response_model=list[ArticleOut])
async def list_articles(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """Get all articles."""
    result = await db.execute(
        select(Article)
        .options(selectinload(Article.tags))
        .order_by(Article.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    articles = result.scalars().all()
    return articles


@router.get("/{article_id}", response_model=ArticleDetailOut)
async def get_article(article_id: int, db: AsyncSession = Depends(get_db)):
    """Get article by ID."""
    result = await db.execute(
        select(Article)
        .options(
            selectinload(Article.author),
            selectinload(Article.category),
            selectinload(Article.tags),
        )
        .where(Article.id == article_id)
    )
    article = result.scalar_one_or_none()

    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article not found"
        )

    return article


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_article(
    article_data: ArticleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Create a new article."""
    # Check if slug already exists
    result = await db.execute(select(Article).where(Article.slug == article_data.slug))
    existing_article = result.scalar_one_or_none()
    if existing_article:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Article with this slug already exists",
        )

    # Create new article
    article_dict = article_data.model_dump(exclude={"tags"})
    article = Article(**article_dict, author_id=current_user["id"])

    # Set published_at if status is published
    if article.status == "published" and not article.published_at:
        article.published_at = datetime.now(timezone.utc)

    # Handle tags
    if article_data.tags:
        for tag_name in article_data.tags:
            # Find or create tag
            tag_slug = tag_name.lower().replace(" ", "-")
            result = await db.execute(select(Tag).where(Tag.slug == tag_slug))
            tag = result.scalar_one_or_none()

            if not tag:
                tag = Tag(name=tag_name, slug=tag_slug)
                db.add(tag)

            article.tags.append(tag)

    db.add(article)
    await db.commit()
    await db.refresh(article)

    return {"id": article.id, "message": "Article created successfully"}


@router.put("/{article_id}", response_model=dict)
async def update_article(
    article_id: int,
    article_data: ArticleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Update an article."""
    result = await db.execute(
        select(Article)
        .options(selectinload(Article.tags))
        .where(Article.id == article_id)
    )
    article = result.scalar_one_or_none()

    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article not found"
        )

    # Check if slug already exists (if being updated)
    if article_data.slug and article_data.slug != article.slug:
        result = await db.execute(
            select(Article).where(Article.slug == article_data.slug)
        )
        existing = result.scalar_one_or_none()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Article with this slug already exists",
            )

    # Update article fields
    update_data = article_data.model_dump(exclude_unset=True, exclude={"tags"})
    for field, value in update_data.items():
        setattr(article, field, value)

    # Update published_at if status changed to published
    if article_data.status == "published" and not article.published_at:
        article.published_at = datetime.now(timezone.utc)

    # Handle tags if provided
    if article_data.tags is not None:
        article.tags.clear()
        for tag_name in article_data.tags:
            tag_slug = tag_name.lower().replace(" ", "-")
            result = await db.execute(select(Tag).where(Tag.slug == tag_slug))
            tag = result.scalar_one_or_none()

            if not tag:
                tag = Tag(name=tag_name, slug=tag_slug)
                db.add(tag)

            article.tags.append(tag)

    await db.commit()

    return {"message": "Article updated"}


@router.delete("/{article_id}", response_model=dict)
async def delete_article(
    article_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Delete an article."""
    result = await db.execute(select(Article).where(Article.id == article_id))
    article = result.scalar_one_or_none()

    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article not found"
        )

    await db.delete(article)
    await db.commit()

    return {"message": "Article deleted successfully"}
