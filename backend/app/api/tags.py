"""Tag routes."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import require_role
from app.schemas.tag import TagCreate, TagUpdate, TagOut
from app.services import tag_service


router = APIRouter(prefix="/tags", tags=["Tags"])


@router.get("/", response_model=List[TagOut])
async def list_tags(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    """List all tags."""
    tags = await tag_service.get_tags(db, skip=skip, limit=limit)
    return tags


@router.get("/{tag_id}", response_model=TagOut)
async def get_tag(
    tag_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get tag by ID."""
    tag = await tag_service.get_tag_by_id(db, tag_id)
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found",
        )
    return tag


@router.post("/", response_model=TagOut, status_code=status.HTTP_201_CREATED)
async def create_tag(
    tag_data: TagCreate,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(require_role("author")),
):
    """Create a new tag."""
    tag = await tag_service.create_tag(db, tag_data)
    return tag


@router.put("/{tag_id}", response_model=TagOut)
async def update_tag(
    tag_id: int,
    tag_data: TagUpdate,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(require_role("editor")),
):
    """Update tag (editor/admin only)."""
    tag = await tag_service.update_tag(db, tag_id, tag_data)
    return tag


@router.delete("/{tag_id}")
async def delete_tag(
    tag_id: int,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(require_role("admin")),
):
    """Delete tag (admin only)."""
    await tag_service.delete_tag(db, tag_id)
    return {"message": "Tag deleted successfully"}
