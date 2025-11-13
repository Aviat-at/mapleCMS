"""Tests for article endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_article(client: AsyncClient, auth_headers):
    """Test article creation."""
    response = await client.post(
        "/api/v1/articles/",
        headers=auth_headers,
        json={
            "title": "Test Article",
            "content_md": "This is a test article",
            "status": "draft",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Article"
    assert data["slug"] == "test-article"
    assert data["status"] == "draft"


@pytest.mark.asyncio
async def test_list_articles(client: AsyncClient, auth_headers):
    """Test listing articles."""
    # Create an article first
    await client.post(
        "/api/v1/articles/",
        headers=auth_headers,
        json={
            "title": "Test Article",
            "content_md": "Content",
            "status": "published",
        },
    )
    
    # List articles
    response = await client.get("/api/v1/articles/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.asyncio
async def test_get_article_by_id(client: AsyncClient, auth_headers):
    """Test getting article by ID."""
    # Create article
    create_response = await client.post(
        "/api/v1/articles/",
        headers=auth_headers,
        json={
            "title": "Test Article",
            "content_md": "Content",
            "status": "published",
        },
    )
    article_id = create_response.json()["id"]
    
    # Get article
    response = await client.get(f"/api/v1/articles/{article_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == article_id
    assert data["title"] == "Test Article"


@pytest.mark.asyncio
async def test_update_article(client: AsyncClient, auth_headers):
    """Test updating article."""
    # Create article
    create_response = await client.post(
        "/api/v1/articles/",
        headers=auth_headers,
        json={
            "title": "Original Title",
            "content_md": "Content",
            "status": "draft",
        },
    )
    article_id = create_response.json()["id"]
    
    # Update article
    response = await client.put(
        f"/api/v1/articles/{article_id}",
        headers=auth_headers,
        json={"title": "Updated Title"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"


@pytest.mark.asyncio
async def test_delete_article(client: AsyncClient, auth_headers):
    """Test deleting article."""
    # Create article
    create_response = await client.post(
        "/api/v1/articles/",
        headers=auth_headers,
        json={
            "title": "To Delete",
            "content_md": "Content",
            "status": "draft",
        },
    )
    article_id = create_response.json()["id"]
    
    # Delete article
    response = await client.delete(
        f"/api/v1/articles/{article_id}",
        headers=auth_headers,
    )
    assert response.status_code == 200
    
    # Verify deletion
    get_response = await client.get(f"/api/v1/articles/{article_id}")
    assert get_response.status_code == 404
