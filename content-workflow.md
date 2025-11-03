# 📝 MapleCMS Content Workflow

This document defines the **content creation, review, and publishing process** used in MapleCMS. It ensures that every article, tutorial, or page follows a consistent quality standard before going live.

---

## 🧭 Overview

MapleCMS uses a flexible editorial workflow designed for both individual creators and collaborative teams.  
Each piece of content (article, page, or media post) moves through distinct **lifecycle stages**:

```
Draft → Review → Approved → Published → Archived
```

---

## 🧱 1. Roles & Permissions

| Role | Permissions |
|------|--------------|
| **Admin** | Full access to all content, users, and settings |
| **Editor** | Can review, edit, and publish articles by others |
| **Author** | Can create and edit their own drafts only |
| **Viewer** | Read-only access (e.g., public site visitor) |

Each API action (create/update/publish/delete) is protected by **role-based access control (RBAC)** in the FastAPI backend.

---

## 🧩 2. Content States

| State | Description |
|--------|--------------|
| **Draft** | Initial version created by author, not visible to the public |
| **In Review** | Submitted for editor or admin approval |
| **Approved** | Reviewed and approved for publishing |
| **Published** | Visible on the live site via the API or CDN |
| **Archived** | Removed from public view but retained for records |

---

## ⚙️ 3. Workflow Steps

### 🪶 Step 1 — Create Draft
- Authors log in and create new articles via `/articles/` POST API or the editor interface.
- Articles are saved in the **Draft** state with version metadata.

```json
{
  "title": "Understanding Async FastAPI",
  "status": "draft",
  "content_md": "FastAPI is async by design..."
}
```

### 🧾 Step 2 — Submit for Review
- Authors change the status to `in_review`.
- Editors receive notification via dashboard or email.

### 🧮 Step 3 — Editorial Review
- Editors check grammar, tags, categories, and metadata.
- Editors can request changes → article reverts to `draft`.
- Once approved → status changes to `approved`.

### 🌍 Step 4 — Publish
- Approved content is set to `published`.
- The frontend (Next.js) fetches it via `/articles?status=published`.
- Published content is statically regenerated or cached in CDN.

### 📦 Step 5 — Archive
- Old or outdated content moves to `archived`.
- Archived content remains available via admin API but is hidden from users.

---

## 🧠 4. Version Control & Drafting

- Each article includes a **revision history** (auto-tracked in DB via `updated_at`).
- Planned feature: `article_revisions` table to log full text diffs.
- Only **authors** of an article or **admins** can revert to a previous version.

---

## 🖋️ 5. Markdown & WYSIWYG Editing

MapleCMS supports multiple editing modes:
- ✍️ **Markdown Mode** – simple, developer-friendly editing
- 🪶 **Rich Text Mode** – powered by a React-based WYSIWYG editor

When saved, both raw Markdown (`content_md`) and rendered HTML (`content_html`) are stored for performance.

---

## 🧾 6. Metadata & SEO
Each article includes metadata for better SEO and indexing.

```json
{
  "title": "FastAPI for Beginners",
  "description": "Learn the basics of FastAPI and async programming.",
  "tags": ["fastapi", "python"],
  "category": "Tutorial",
  "cover_image": "https://cdn.maplecms.com/uploads/cover.png",
  "meta_json": {
    "reading_time": "5 min",
    "keywords": ["python", "async", "cms"]
  }
}
```

The frontend automatically reads this metadata to generate **meta tags**, **Open Graph**, and **Twitter card** previews.

---

## 📤 7. Publishing Flow (Frontend Integration)

### Static Rendering (Next.js)
- Next.js builds static pages for published content using `getStaticProps()`.
- Regeneration occurs automatically on new publishes (ISR).

### API Fetch Example
```tsx
export async function getStaticProps() {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/articles?status=published`);
  const articles = await res.json();
  return { props: { articles }, revalidate: 60 };
}
```

---

## 🔔 8. Notifications (Optional)
- Email or Slack alerts on review requests & publish events.
- Configurable via backend settings or webhook integrations.

---

## 🧩 9. Automation & AI (Future)
- GPT-powered **content quality check** (grammar, readability, tone)
- AI-generated summaries or SEO tags
- Smart internal link suggestions

---

## 🧭 Summary
- Simple 5-stage content lifecycle.
- Clear role-based permissions and API enforcement.
- SEO-friendly publishing system with caching and version control.

> MapleCMS content workflow empowers teams to create, review, and publish knowledge efficiently — combining editorial structure with developer freedom.
