# 🗃️ MapleCMS Database Schema

This document defines the **core data model** for MapleCMS — a lightweight, extensible schema optimized for readability, performance, and future growth.

- **DB Engine:** PostgreSQL (13+)
- **ORM:** SQLAlchemy + Alembic
- **Naming conventions:** snake_case for tables/columns, singular table names
- **Time fields:** `created_at`, `updated_at` (UTC, `timestamptz`)

---

## 🧩 Entities (MVP)

- **User** — authentication & roles
- **Article** — main content entity
- **Category** — top-level grouping
- **Tag** — flexible labels
- **ArticleTag** — many-to-many between Article and Tag
- **Media** — uploaded files/objects (S3-backed)
- **RefreshToken** — token rotation (optional if using opaque refresh)

> Future-ready (optional): `Setting`, `Webhook`, `Plugin`, `AuditLog`

---

## 🔗 ER Diagram (ASCII)

```
+---------+        1         *      +----------+       *        *     +-----+
| User    |------------------------>| Article  |<----------------------| Tag |
+---------+                         +----------+                     /  +-----+
| id (PK) |                         | id (PK)  |                   /
| email   |                         | author_id| (FK -> User.id)  /   +-------------+
| role    |                         | category_id (FK)            ----| ArticleTag |
| ...     |                         | title    |                      +-------------+
+---------+                         | slug     |                      | article_id  |
                                    | content  |                      | tag_id      |
+-----------+                       | status   |                      +-------------+
| Category  | 1                 *   | ...      |
+-----------+---------------------->+----------+
| id (PK)   |
| name      |                 1      *
+-----------+---------------------->+-------+
                                    | Media |
                                    +-------+
                                    | id    |
                                    | url   |
                                    | ...   |
                                    +-------+
```

---

## 🧱 Table Definitions

### 1) `user`
```sql
CREATE TABLE "user" (
  id            BIGSERIAL PRIMARY KEY,
  username      VARCHAR(48)  NOT NULL UNIQUE,
  email         CITEXT       NOT NULL UNIQUE,
  password_hash TEXT         NOT NULL,
  role          VARCHAR(16)  NOT NULL DEFAULT 'author',
  is_active     BOOLEAN      NOT NULL DEFAULT TRUE,
  created_at    TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
  updated_at    TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_user_email ON "user" (email);
```
**Notes**
- `role` enum (suggested values): `admin`, `editor`, `author`, `viewer`.
- Use Argon2/BCrypt for `password_hash`.

---

### 2) `category`
```sql
CREATE TABLE category (
  id          BIGSERIAL PRIMARY KEY,
  name        VARCHAR(64) NOT NULL UNIQUE,
  slug        VARCHAR(80) NOT NULL UNIQUE,
  description TEXT,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

---

### 3) `article`
```sql
CREATE TABLE article (
  id            BIGSERIAL PRIMARY KEY,
  title         VARCHAR(160) NOT NULL,
  slug          VARCHAR(180) NOT NULL UNIQUE,
  excerpt       TEXT,
  content_md    TEXT,                 -- raw Markdown (optional if using MDX)
  content_html  TEXT,                 -- rendered HTML (optional cache)
  status        VARCHAR(16) NOT NULL DEFAULT 'draft', -- draft|published|archived
  author_id     BIGINT NOT NULL REFERENCES "user"(id) ON DELETE RESTRICT,
  category_id   BIGINT REFERENCES category(id) ON DELETE SET NULL,
  published_at  TIMESTAMPTZ,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  meta_json     JSONB DEFAULT '{}'::jsonb
);
CREATE INDEX idx_article_slug ON article (slug);
CREATE INDEX idx_article_status ON article (status);
CREATE INDEX idx_article_published_at ON article (published_at DESC);
```
**Notes**
- `content_md` vs `content_html`: choose one, or keep both for performance.
- `meta_json` can store SEO, reading time, cover image IDs, etc.

---

### 4) `tag`
```sql
CREATE TABLE tag (
  id         BIGSERIAL PRIMARY KEY,
  name       VARCHAR(48) NOT NULL UNIQUE,
  slug       VARCHAR(64) NOT NULL UNIQUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

---

### 5) `article_tag` (junction)
```sql
CREATE TABLE article_tag (
  article_id BIGINT NOT NULL REFERENCES article(id) ON DELETE CASCADE,
  tag_id     BIGINT NOT NULL REFERENCES tag(id)      ON DELETE CASCADE,
  PRIMARY KEY (article_id, tag_id)
);
CREATE INDEX idx_article_tag_tag ON article_tag (tag_id);
```

---

### 6) `media`
```sql
CREATE TABLE media (
  id           BIGSERIAL PRIMARY KEY,
  filename     VARCHAR(256) NOT NULL,
  mime_type    VARCHAR(96)  NOT NULL,
  size_bytes   BIGINT       NOT NULL,
  storage_key  TEXT         NOT NULL,  -- e.g., s3 key: uploads/2025/11/cover.png
  url          TEXT         NOT NULL,  -- signed or public URL
  owner_id     BIGINT REFERENCES "user"(id) ON DELETE SET NULL,
  created_at   TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
  updated_at   TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
  meta_json    JSONB DEFAULT '{}'::jsonb
);
CREATE INDEX idx_media_owner ON media (owner_id);
```

---

### 7) `refresh_token` (optional)
```sql
CREATE TABLE refresh_token (
  id           BIGSERIAL PRIMARY KEY,
  user_id      BIGINT NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
  token_hash   TEXT   NOT NULL,   -- store hash, not raw token
  expires_at   TIMESTAMPTZ NOT NULL,
  created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  revoked      BOOLEAN NOT NULL DEFAULT FALSE
);
CREATE INDEX idx_refresh_user_expires ON refresh_token (user_id, expires_at);
```

---

## 🐍 SQLAlchemy Models (Skeleton)

```python
# models.py (excerpt)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import String, Text, Boolean, ForeignKey, BigInteger, JSON
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String(48), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    role: Mapped[str] = mapped_column(String(16), default="author", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

class Article(Base):
    __tablename__ = "article"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str] = mapped_column(String(160), nullable=False)
    slug: Mapped[str] = mapped_column(String(180), unique=True, nullable=False)
    excerpt: Mapped[str | None] = mapped_column(Text)
    content_md: Mapped[str | None] = mapped_column(Text)
    content_html: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(16), default="draft", nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    category_id: Mapped[int | None] = mapped_column(ForeignKey("category.id"))
    published_at: Mapped[datetime | None]
    meta_json: Mapped[dict] = mapped_column(JSONB, default=dict)

    author = relationship("User")
    tags = relationship("Tag", secondary="article_tag", back_populates="articles")

class Tag(Base):
    __tablename__ = "tag"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(48), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    articles = relationship("Article", secondary="article_tag", back_populates="tags")
```

---

## 🧪 Constraints & Integrity

- **Uniqueness**: `user.email`, `user.username`, `article.slug`, `tag.slug`.
- **Foreign Keys**: `article.author_id`, `article.category_id`, `media.owner_id`.
- **Cascade**: Deleting an `article` cascades to `article_tag`.
- **Set Null**: Deleting a `user` will set `owner_id` to NULL in `media` (preserve files).

---

## ⚡ Performance & Indexing

- **Read-heavy paths**: index `article.slug`, `article.published_at DESC`, `article.status`.
- **Full-text search** (optional): PostgreSQL `tsvector` on `title` + `content_html`.
- **Caching**: Redis for hot lists (latest posts, popular tags).

---

## 🔁 Migrations

Use **Alembic** for schema migrations.

```bash
alembic init alembic
alembic revision -m "create base schema"
alembic upgrade head
```

- Keep migrations **atomic** and **reversible**.
- Record migration IDs in `CHANGELOG.md` for major releases.

---

## 🔒 Security Considerations

- Store **password hashes** only (Argon2/BCrypt), never raw passwords.
- Enforce **row-level authorization** in API (author can edit own drafts, etc.).
- Validate **media MIME types** and sanitize file names.
- Use **signed URLs** for S3 downloads where appropriate.

---

## 📦 Seed Data (Optional)

- Default roles: `admin`, `editor`, `author`, `viewer`.
- Demo user: `admin@example.com` with a random password (printed once).
- Sample categories: `Tutorials`, `Guides`, `News`.

---

## 🧭 Evolution Plan

- Add `AuditLog` for admin actions (GDPR-friendly tracing).
- Add `Revision` table to version articles.
- Add `Webhook` table for outbound integrations (Zapier, Slack).

> The MapleCMS schema is purposefully **minimal yet scalable**, enabling a lightweight MVP that can grow into a robust platform without breaking changes.
