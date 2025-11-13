"""Article-Tag junction model."""

from sqlalchemy import BigInteger, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ArticleTag(Base):
    """Junction table for many-to-many relationship between articles and tags."""

    __tablename__ = "article_tag"

    article_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("article.id", ondelete="CASCADE"), primary_key=True
    )
    tag_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("tag.id", ondelete="CASCADE"), primary_key=True
    )

    # Relationships
    article = relationship("Article", back_populates="tags")
    tag = relationship("Tag", back_populates="articles")

    __table_args__ = (
        UniqueConstraint("article_id", "tag_id", name="uq_article_tag"),
    )

    def __repr__(self) -> str:
        return f"<ArticleTag(article_id={self.article_id}, tag_id={self.tag_id})>"
