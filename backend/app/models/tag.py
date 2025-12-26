"""Tag model."""

from datetime import datetime
from sqlalchemy import String, DateTime, BigInteger, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base


IDType = BigInteger().with_variant(Integer(), "sqlite")


class Tag(Base):
    """Tag model for flexible article labeling."""

    __tablename__ = "tag"

    id: Mapped[int] = mapped_column(IDType, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(48), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    articles = relationship("ArticleTag", back_populates="tag", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Tag(id={self.id}, name={self.name})>"
