# 🔗 MapleCMS Integration Plan

This document explains how the **Next.js frontend** communicates with the **FastAPI backend**, forming a seamless, decoupled full-stack architecture. It outlines API routes, data flow, authentication, and environment setup for smooth integration.

---

## 🧱 Overview

MapleCMS is built as a **headless CMS**, where the backend (FastAPI) exposes REST APIs and the frontend (Next.js) consumes them dynamically.  
This design enables multi-platform deployment — websites, mobile apps, or external tools can all use the same API.

```
Next.js (Frontend) ⇄ FastAPI (Backend) ⇄ PostgreSQL / S3 / Redis
```

---

## ⚙️ 1. Communication Protocol

- **API Type:** REST (JSON)
- **Transport:** HTTPS only
- **Authentication:** JWT Bearer Token
- **CORS:** Enabled for the frontend domain(s)
- **Data Format:** UTF-8 JSON payloads

---

## 🌍 2. Environment Configuration

### `.env.local` (Frontend)
```
NEXT_PUBLIC_API_URL=https://api.maplecms.com/api/v1
```

### `.env` (Backend)
```
FRONTEND_URL=https://maplecms.com
CORS_ORIGINS=["https://maplecms.com", "http://localhost:3000"]
```

---

## 🧠 3. API Consumption Flow

### Example – Fetch Articles (Frontend)
```tsx
// frontend/lib/api.ts

export async function getArticles() {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/articles/`);
  if (!res.ok) throw new Error('Failed to fetch articles');
  return res.json();
}
```

### Example – Display Articles
```tsx
// frontend/pages/index.tsx
import { useEffect, useState } from 'react';
import { getArticles } from '@/lib/api';

export default function HomePage() {
  const [articles, setArticles] = useState([]);

  useEffect(() => {
    getArticles().then(setArticles);
  }, []);

  return (
    <main className="p-6">
      <h1 className="text-3xl font-bold mb-4">Latest Articles</h1>
      {articles.map((a) => (
        <div key={a.id} className="mb-3 border-b pb-2">
          <h2 className="text-xl font-semibold">{a.title}</h2>
          <p className="text-gray-600">By {a.author}</p>
        </div>
      ))}
    </main>
  );
}
```

---

## 🔐 4. Authentication Flow

### Login Flow
1. User submits credentials to `/auth/login`.
2. Backend returns a JWT access token and optional refresh token.
3. Frontend stores token securely in **HttpOnly cookies** or **localStorage** (depending on setup).
4. Subsequent API calls include:
```
Authorization: Bearer <token>
```

### Protected Routes (Frontend)
```tsx
export async function getUserProfile(token: string) {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/users/me`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.json();
}
```

---

## 🪣 5. Media Integration (S3)

### Upload Flow
1. Frontend sends file via `multipart/form-data` to `/media/upload`.
2. FastAPI stores file metadata in PostgreSQL.
3. File is uploaded to AWS S3.
4. API returns the public or signed URL.

### Example
```tsx
export async function uploadFile(file: File) {
  const formData = new FormData();
  formData.append('file', file);

  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/media/upload`, {
    method: 'POST',
    body: formData,
  });

  return res.json();
}
```

---

## 🧩 6. Caching & Optimization
- **Next.js ISR (Incremental Static Regeneration)** for article pages.
- **Redis caching** for popular queries (optional backend enhancement).
- **CDN** via AWS CloudFront for all static assets.
- **Compression:** Gzip + Brotli for payloads.

---

## 🔄 7. Error Handling

| Status | Meaning | Action (Frontend) |
|---------|----------|------------------|
| 200 | OK | Render data |
| 400 | Bad Request | Display form validation errors |
| 401 | Unauthorized | Redirect to login |
| 403 | Forbidden | Show permission error |
| 404 | Not Found | Show 404 page |
| 500 | Internal Error | Show retry / bug report |

**Example:**
```tsx
if (res.status === 401) router.push('/login');
```

---

## ⚡ 8. Deployment Sync
- Frontend builds (`npm run build`) use live API URLs.
- Backend deploys via ECS before frontend to ensure API availability.
- Both services are versioned and deployed together via GitHub Actions.

---

## 🧭 Summary
- Next.js fetches data from FastAPI via secure REST APIs.
- Authentication uses JWT tokens with CORS-enabled endpoints.
- File uploads use AWS S3 integration.
- The system supports **decoupled scaling** and **independent deployments**.

> MapleCMS integrates frontend and backend seamlessly — maintaining speed, flexibility, and simplicity for developers.
