"""Tests for MapleCMS backend."""
import pytest
from httpx import AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_root():
    """Test root endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()
        assert "Welcome to MapleCMS" in response.json()["message"]


@pytest.mark.asyncio
async def test_health_check():
    """Test health check endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_version():
    """Test version endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/version")
        assert response.status_code == 200
        assert "version" in response.json()
        assert "build" in response.json()
