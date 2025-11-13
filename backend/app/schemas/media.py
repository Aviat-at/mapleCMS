"""Media schemas."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict


class MediaUpload(BaseModel):
    """Schema for media upload response."""
    message: str
    media_id: int
    url: str


class MediaOut(BaseModel):
    """Schema for media output."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    filename: str
    original_filename: str
    file_path: str
    file_size: int
    mime_type: str
    url: str
    created_at: datetime
    updated_at: datetime
