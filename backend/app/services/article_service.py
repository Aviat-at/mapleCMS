"""Article service for business logic."""

from typing import Optional, List
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
from slugify import slugify

from app.models.article import Article
from app.models.article_tag import ArticleTag
from app.schemas.article import ArticleCreate, ArticleUpdate


async def get_article_by_id(db: AsyncSession, article_id: int) -> Optional[Article]:
    """Get article by ID with relationships."""
    result = await db.execute(
        select(Article)
        .options(selectinload(Article.author), selectinload(Article.category))
        .where(Article.id == article_id)
    )
    return result.scalar_one_or_none()


async def get_article_by_slug(db: AsyncSession, slug: str) -> Optional[Article]:
    """Get article by slug."""
    result = await db.execute(
        select(Article)
        .options(selectinload(Article.author), selectinload(Article.category))
        .where(Article.slug == slug)
    )
    return result.scalar_one_or_none()


async def get_articles(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    author_id: Optional[int] = None,
    category_id: Optional[int] = None,
) -> List[Article]:
    """Get list of articles with filters."""
    query = select(Article).options(
        selectinload(Article.author),
        selectinload(Article.category)
    )
    
    conditions = []
    if status:
        conditions.append(Article.status == status)
    if author_id:
        conditions.append(Article.author_id == author_id)
    if category_id:
        conditions.append(Article.category_id == category_id)
    
    if conditions:
        query = query.where(and_(*conditions))
    
    query = query.order_by(Article.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    return list(result.scalars().all())


async def create_article(
    db: AsyncSession, article_data: ArticleCreate, author_id: int
) -> Article:
    """Create a new article."""
    # Generate slug
    base_slug = slugify(article_data.title)
    slug = base_slug
    counter = 1
    
    while await get_article_by_slug(db, slug):
        slug = f"{base_slug}-{counter}"
        counter += 1
    
    # Set published_at if status is published
    published_at = None
    if article_data.status == "published":
        published_at = datetime.utcnow()
    
    # Create article
    article = Article(
        title=article_data.title,
        slug=slug,
        excerpt=article_data.excerpt,
        content_md=article_data.content_md,
        content_html=article_data.content_html,
        status=article_data.status,
        author_id=author_id,
        category_id=article_data.category_id,
        published_at=published_at,
        meta_json=article_data.meta_json,
    )
    
    db.add(article)
    await db.flush()
    
    # Add tags
    if article_data.tag_ids:
        for tag_id in article_data.tag_ids:
            article_tag = ArticleTag(article_id=article.id, tag_id=tag_id)
            db.add(article_tag)
    
    await db.flush()
    await db.refresh(article)
    return article


async def update_article(
    db: AsyncSession, article_id: int, article_data: ArticleUpdate
) -> Article:
    """Update article."""
    article = await get_article_by_id(db, article_id)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )
    
    # Update fields
    if article_data.title is not None:
        article.title = article_data.title
        # Regenerate slug if title changed
        base_slug = slugify(article_data.title)
        if base_slug != article.slug:
            slug = base_slug
            counter = 1
            while True:
                existing = await get_article_by_slug(db, slug)
                if not existing or existing.id == article_id:
                    break
                slug = f"{base_slug}-{counter}"
                counter += 1
            article.slug = slug
    
    if article_data.excerpt is not None:
        article.excerpt = article_data.excerpt
    
    if article_data.content_md is not None:
        article.content_md = article_data.content_md
    
    if article_data.content_html is not None:
        article.content_html = article_data.content_html
    
    if article_data.status is not None:
        # Set published_at when changing to published
        if article_data.status == "published" and article.status != "published":
            article.published_at = datetime.utcnow()
        article.status = article_data.status
    
    if article_data.category_id is not None:
        article.category_id = article_data.category_id
    
    if article_data.meta_json is not None:
        article.meta_json = article_data.meta_json
    
    # Update tags
    if article_data.tag_ids is not None:
        # Remove existing tags
        await db.execute(
            select(ArticleTag).where(ArticleTag.article_id == article_id)
        )
        existing_tags = (await db.execute(
            select(ArticleTag).where(ArticleTag.article_id == article_id)
        )).scalars().all()
        
        for tag in existing_tags:
            await db.delete(tag)
        
        # Add new tags
        for tag_id in article_data.tag_ids:
            article_tag = ArticleTag(article_id=article.id, tag_id=tag_id)
            db.add(article_tag)
    
    await db.flush()
    await db.refresh(article)
    return article


async def delete_article(db: AsyncSession, article_id: int) -> bool:
    """Delete article."""
    article = await get_article_by_id(db, article_id)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )
    
    await db.delete(article)
    await db.flush()
    return True
