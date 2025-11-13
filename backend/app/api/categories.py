"""Categories API routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import Category
from app.schemas.schemas import CategoryCreate, CategoryOut

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=list[CategoryOut])
async def list_categories(db: AsyncSession = Depends(get_db)):
    """Get all categories."""
    result = await db.execute(select(Category).order_by(Category.name))
    categories = result.scalars().all()
    return categories


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Create a new category."""
    # Check if category with same slug exists
    result = await db.execute(
        select(Category).where(Category.slug == category_data.slug)
    )
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this slug already exists",
        )

    category = Category(**category_data.model_dump())
    db.add(category)
    await db.commit()
    await db.refresh(category)

    return {"message": "Category created", "id": category.id}
