"""Refresh Token model."""

from datetime import datetime
from sqlalchemy import String, DateTime, BigInteger, ForeignKey, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base


IDType = BigInteger().with_variant(Integer(), "sqlite")


class RefreshToken(Base):
    """Refresh token model for token rotation."""

    __tablename__ = "refresh_token"

    id: Mapped[int] = mapped_column(IDType, primary_key=True, index=True, autoincrement=True)
    token: Mapped[str] = mapped_column(String(512), unique=True, nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(
        IDType, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    is_revoked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    # Relationships
    user = relationship("User", back_populates="refresh_tokens")

    def __repr__(self) -> str:
        return f"<RefreshToken(id={self.id}, user_id={self.user_id}, revoked={self.is_revoked})>"
