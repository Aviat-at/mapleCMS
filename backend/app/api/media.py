"""Media routes for file uploads."""

import os
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import require_role
from app.core.config import settings
from app.schemas.media import MediaOut, MediaUpload
from app.models.media import Media


router = APIRouter(prefix="/media", tags=["Media"])


def get_file_extension(filename: str) -> str:
    """Get file extension from filename."""
    return filename.rsplit(".", 1)[1].lower() if "." in filename else ""


def is_allowed_file(filename: str) -> bool:
    """Check if file extension is allowed."""
    ext = get_file_extension(filename)
    return ext in settings.ALLOWED_EXTENSIONS


@router.post("/upload", response_model=MediaUpload)
async def upload_file(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    _: None = Depends(require_role("author")),
):
    """Upload a file to S3 or local storage."""
    # Validate file
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No filename provided",
        )
    
    if not is_allowed_file(file.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed types: {', '.join(settings.ALLOWED_EXTENSIONS)}",
        )
    
    # Read file content
    content = await file.read()
    file_size = len(content)
    
    if file_size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Maximum size: {settings.MAX_UPLOAD_SIZE} bytes",
        )
    
    # Generate unique filename
    ext = get_file_extension(file.filename)
    unique_filename = f"{uuid.uuid4()}.{ext}"
    
    # For now, we'll simulate S3 upload with a local path
    # In production, this would use boto3 to upload to S3
    file_path = f"uploads/{unique_filename}"
    
    # Create uploads directory if it doesn't exist
    os.makedirs("uploads", exist_ok=True)
    
    # Save file locally (in production, upload to S3)
    with open(file_path, "wb") as f:
        f.write(content)
    
    # Generate URL (in production, this would be S3 URL)
    file_url = f"{settings.FRONTEND_URL}/{file_path}"
    
    # Save media record to database
    media = Media(
        filename=unique_filename,
        original_filename=file.filename,
        file_path=file_path,
        file_size=file_size,
        mime_type=file.content_type or "application/octet-stream",
        url=file_url,
    )
    
    db.add(media)
    await db.flush()
    await db.refresh(media)
    
    return MediaUpload(
        message="File uploaded successfully",
        media_id=media.id,
        url=media.url,
    )


@router.get("/", response_model=List[MediaOut])
async def list_media(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    """List all media files."""
    from sqlalchemy import select
    result = await db.execute(
        select(Media).order_by(Media.created_at.desc()).offset(skip).limit(limit)
    )
    media_list = result.scalars().all()
    return list(media_list)


@router.get("/{media_id}", response_model=MediaOut)
async def get_media(
    media_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get media by ID."""
    from sqlalchemy import select
    result = await db.execute(select(Media).where(Media.id == media_id))
    media = result.scalar_one_or_none()
    
    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media not found",
        )
    
    return media


@router.delete("/{media_id}")
async def delete_media(
    media_id: int,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(require_role("editor")),
):
    """Delete media file."""
    from sqlalchemy import select
    result = await db.execute(select(Media).where(Media.id == media_id))
    media = result.scalar_one_or_none()
    
    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media not found",
        )
    
    # Delete file from storage
    if os.path.exists(media.file_path):
        os.remove(media.file_path)
    
    # Delete from database
    await db.delete(media)
    await db.flush()
    
    return {"message": "Media deleted successfully"}
