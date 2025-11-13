"""Category routes."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import require_role
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryOut
from app.services import category_service


router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=List[CategoryOut])
async def list_categories(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    """List all categories."""
    categories = await category_service.get_categories(db, skip=skip, limit=limit)
    return categories


@router.get("/{category_id}", response_model=CategoryOut)
async def get_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get category by ID."""
    category = await category_service.get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    return category


@router.post("/", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(require_role("editor")),
):
    """Create a new category (editor/admin only)."""
    category = await category_service.create_category(db, category_data)
    return category


@router.put("/{category_id}", response_model=CategoryOut)
async def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(require_role("editor")),
):
    """Update category (editor/admin only)."""
    category = await category_service.update_category(db, category_id, category_data)
    return category


@router.delete("/{category_id}")
async def delete_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(require_role("admin")),
):
    """Delete category (admin only)."""
    await category_service.delete_category(db, category_id)
    return {"message": "Category deleted successfully"}
