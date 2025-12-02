# 📚 MapleCMS API Reference

MapleCMS exposes a clean, RESTful API built with **FastAPI**, designed to be fast, secure, and easy to integrate with any frontend or external service.  
This document outlines all key endpoints, authentication methods, and data schemas.

---

## 🧠 Overview

- **Base URL (Local):** `http://localhost:8000/api/v1`
- **Base URL (Production):** `https://api.maplecms.com/api/v1`
- **Format:** JSON (`application/json`)
- **Authentication:** JWT Bearer Token

---

## 🔐 Authentication

### Login
**POST** `/auth/login`
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```
**Response:**
```json
{
  "access_token": "<JWT_TOKEN>",
  "token_type": "bearer",
  "expires_in": 3600
}
```

### Register
**POST** `/auth/register`
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "strongpassword"
}
```
**Response:**
```json
{
  "message": "User registered successfully",
  "user_id": 12
}
```

### Refresh Token
**POST** `/auth/refresh`
```json
{
  "refresh_token": "<REFRESH_TOKEN>"
}
```
**Response:**
```json
{
  "access_token": "<NEW_JWT_TOKEN>"
}
```

---

## 📝 Articles

### Get All Articles
**GET** `/articles/`
**Response:**
```json
[
  {
    "id": 1,
    "title": "Welcome to MapleCMS",
    "slug": "welcome-maplecms",
    "author": "Admin",
    "tags": ["intro", "cms"],
    "created_at": "2025-01-05T10:30:00Z"
  }
]
```

### Get Article by ID
**GET** `/articles/{id}`
**Response:**
```json
{
  "id": 1,
  "title": "Welcome to MapleCMS",
  "content": "<html>Article body here...</html>",
  "author": "Admin",
  "category": "Tutorial",
  "published": true
}
```

### Create Article
**POST** `/articles/`
**Auth Required** ✅
```json
{
  "title": "My New Article",
  "content": "MapleCMS makes content creation simple!",
  "tags": ["fastapi", "nextjs"],
  "category": "Development",
  "published": true
}
```
**Response:**
```json
{
  "id": 22,
  "message": "Article created successfully"
}
```

### Update Article
**PUT** `/articles/{id}`
```json
{
  "title": "Updated Title",
  "content": "Updated content..."
}
```
**Response:**
```json
{
  "message": "Article updated"
}
```

### Delete Article
**DELETE** `/articles/{id}`
**Response:**
```json
{
  "message": "Article deleted successfully"
}
```

---

## 🧩 Media

### Upload File
**POST** `/media/upload`
- **Type:** `multipart/form-data`
```bash
curl -X POST -F "file=@/path/to/image.png" https://api.maplecms.com/api/v1/media/upload
```
**Response:**
```json
{
  "file_url": "https://cdn.maplecms.com/uploads/image.png"
}
```

### List Files
**GET** `/media/`
**Response:**
```json
[
  {"filename": "image.png", "url": "https://cdn.maplecms.com/uploads/image.png"}
]
```

---

## 👥 Users

### Get Profile
**GET** `/users/me`
**Auth Required** ✅
**Response:**
```json
{
  "id": 5,
  "username": "john_doe",
  "email": "john@example.com",
  "role": "editor"
}
```

### List Users (Admin only)
**GET** `/users/`
**Response:**
```json
[
  {"id": 1, "username": "admin"},
  {"id": 2, "username": "editor"}
]
```

---

## 🧱 Categories & Tags

### Get All Categories
**GET** `/categories/`
```json
[
  {"id": 1, "name": "Tutorials"},
  {"id": 2, "name": "Guides"}
]
```

### Create Category
**POST** `/categories/`
```json
{
  "name": "AI"
}
```
**Response:**
```json
{
  "message": "Category created"
}
```

---

## ⚙️ System & Meta Endpoints

### Health Check
**GET** `/health`
```json
{
  "status": "ok",
  "uptime": "3 days, 12 hours"
}
```

### API Version
**GET** `/version`
```json
{
  "version": "1.0.0",
  "build": "2025-01-07T10:00:00Z"
}
```

---

## 🧭 Notes
- All endpoints are **CORS-enabled** for integration with the Next.js frontend.
- Rate limiting and caching can be enabled in production.
- Future versions will include **GraphQL** and **WebSocket** endpoints.

> MapleCMS API — built to be lightweight, scalable, and developer-friendly.
