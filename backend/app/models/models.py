"""SQLAlchemy models for MapleCMS."""
from datetime import datetime

from sqlalchemy import (BigInteger, Boolean, Column, ForeignKey, String, Table,
                        Text)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base

# Association table for many-to-many relationship between Article and Tag
article_tag = Table(
    "article_tag",
    Base.metadata,
    Column(
        "article_id",
        BigInteger,
        ForeignKey("article.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "tag_id", BigInteger, ForeignKey("tag.id", ondelete="CASCADE"), primary_key=True
    ),
)


class User(Base):
    """User model."""

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String(48), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    role: Mapped[str] = mapped_column(String(16), default="author", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    articles: Mapped[list["Article"]] = relationship("Article", back_populates="author")


class Category(Base):
    """Category model."""

    __tablename__ = "category"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    articles: Mapped[list["Article"]] = relationship(
        "Article", back_populates="category"
    )


class Tag(Base):
    """Tag model."""

    __tablename__ = "tag"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(48), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    articles: Mapped[list["Article"]] = relationship(
        "Article", secondary=article_tag, back_populates="tags"
    )


class Article(Base):
    """Article model."""

    __tablename__ = "article"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str] = mapped_column(String(160), nullable=False)
    slug: Mapped[str] = mapped_column(String(180), unique=True, nullable=False)
    excerpt: Mapped[str | None] = mapped_column(Text)
    content_md: Mapped[str | None] = mapped_column(Text)
    content_html: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(16), default="draft", nullable=False)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="RESTRICT"), nullable=False
    )
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("category.id", ondelete="SET NULL")
    )
    published_at: Mapped[datetime | None]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
    meta_json: Mapped[dict] = mapped_column(JSONB, default=dict, server_default="{}")

    # Relationships
    author: Mapped["User"] = relationship("User", back_populates="articles")
    category: Mapped["Category"] = relationship("Category", back_populates="articles")
    tags: Mapped[list["Tag"]] = relationship(
        "Tag", secondary=article_tag, back_populates="articles"
    )


class Media(Base):
    """Media model."""

    __tablename__ = "media"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    filename: Mapped[str] = mapped_column(String(256), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(96), nullable=False)
    size_bytes: Mapped[int] = mapped_column(BigInteger, nullable=False)
    storage_key: Mapped[str] = mapped_column(Text, nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    owner_id: Mapped[int | None] = mapped_column(
        ForeignKey("user.id", ondelete="SET NULL")
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
    meta_json: Mapped[dict] = mapped_column(JSONB, default=dict, server_default="{}")
