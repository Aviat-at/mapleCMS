"""Tag service for business logic."""

from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from slugify import slugify

from app.models.tag import Tag
from app.schemas.tag import TagCreate, TagUpdate


async def get_tag_by_id(db: AsyncSession, tag_id: int) -> Optional[Tag]:
    """Get tag by ID."""
    result = await db.execute(select(Tag).where(Tag.id == tag_id))
    return result.scalar_one_or_none()


async def get_tag_by_slug(db: AsyncSession, slug: str) -> Optional[Tag]:
    """Get tag by slug."""
    result = await db.execute(select(Tag).where(Tag.slug == slug))
    return result.scalar_one_or_none()


async def get_tags(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Tag]:
    """Get list of tags."""
    result = await db.execute(select(Tag).offset(skip).limit(limit))
    return list(result.scalars().all())


async def create_tag(db: AsyncSession, tag_data: TagCreate) -> Tag:
    """Create a new tag."""
    # Generate slug
    base_slug = slugify(tag_data.name)
    slug = base_slug
    counter = 1
    
    while await get_tag_by_slug(db, slug):
        slug = f"{base_slug}-{counter}"
        counter += 1
    
    tag = Tag(
        name=tag_data.name,
        slug=slug,
    )
    
    db.add(tag)
    await db.flush()
    await db.refresh(tag)
    return tag


async def update_tag(db: AsyncSession, tag_id: int, tag_data: TagUpdate) -> Tag:
    """Update tag."""
    tag = await get_tag_by_id(db, tag_id)
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found",
        )
    
    if tag_data.name is not None:
        tag.name = tag_data.name
        # Regenerate slug
        base_slug = slugify(tag_data.name)
        if base_slug != tag.slug:
            slug = base_slug
            counter = 1
            while True:
                existing = await get_tag_by_slug(db, slug)
                if not existing or existing.id == tag_id:
                    break
                slug = f"{base_slug}-{counter}"
                counter += 1
            tag.slug = slug
    
    await db.flush()
    await db.refresh(tag)
    return tag


async def delete_tag(db: AsyncSession, tag_id: int) -> bool:
    """Delete tag."""
    tag = await get_tag_by_id(db, tag_id)
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found",
        )
    
    await db.delete(tag)
    await db.flush()
    return True
