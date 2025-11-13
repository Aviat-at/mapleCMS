"""Category service for business logic."""

from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from slugify import slugify

from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


async def get_category_by_id(db: AsyncSession, category_id: int) -> Optional[Category]:
    """Get category by ID."""
    result = await db.execute(select(Category).where(Category.id == category_id))
    return result.scalar_one_or_none()


async def get_category_by_slug(db: AsyncSession, slug: str) -> Optional[Category]:
    """Get category by slug."""
    result = await db.execute(select(Category).where(Category.slug == slug))
    return result.scalar_one_or_none()


async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Category]:
    """Get list of categories."""
    result = await db.execute(select(Category).offset(skip).limit(limit))
    return list(result.scalars().all())


async def create_category(db: AsyncSession, category_data: CategoryCreate) -> Category:
    """Create a new category."""
    # Generate slug
    base_slug = slugify(category_data.name)
    slug = base_slug
    counter = 1
    
    while await get_category_by_slug(db, slug):
        slug = f"{base_slug}-{counter}"
        counter += 1
    
    category = Category(
        name=category_data.name,
        slug=slug,
        description=category_data.description,
    )
    
    db.add(category)
    await db.flush()
    await db.refresh(category)
    return category


async def update_category(
    db: AsyncSession, category_id: int, category_data: CategoryUpdate
) -> Category:
    """Update category."""
    category = await get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    
    if category_data.name is not None:
        category.name = category_data.name
        # Regenerate slug
        base_slug = slugify(category_data.name)
        if base_slug != category.slug:
            slug = base_slug
            counter = 1
            while True:
                existing = await get_category_by_slug(db, slug)
                if not existing or existing.id == category_id:
                    break
                slug = f"{base_slug}-{counter}"
                counter += 1
            category.slug = slug
    
    if category_data.description is not None:
        category.description = category_data.description
    
    await db.flush()
    await db.refresh(category)
    return category


async def delete_category(db: AsyncSession, category_id: int) -> bool:
    """Delete category."""
    category = await get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    
    await db.delete(category)
    await db.flush()
    return True
