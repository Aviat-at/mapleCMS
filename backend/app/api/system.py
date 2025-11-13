"""System API routes."""
from datetime import datetime, timezone

from fastapi import APIRouter

from app.core.config import settings
from app.schemas.schemas import HealthCheck, VersionInfo

router = APIRouter(tags=["System"])


@router.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint."""
    return HealthCheck(status="ok", version=settings.version)


@router.get("/version", response_model=VersionInfo)
async def version_info():
    """Get API version information."""
    return VersionInfo(
        version=settings.version, build=datetime.now(timezone.utc).isoformat()
    )
