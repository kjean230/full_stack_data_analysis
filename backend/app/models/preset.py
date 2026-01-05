from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any
from sqlalchemy import CheckConstraint, DateTime, ForeignKey, JSON, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

# created the preset table (for SQL database) to store user presets for data analysis
# each preset is linked to a user and contains settings for data analysis views and filters
class Preset(Base):
    __tablename__ = "presets"

    preset_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Preset details
    # name must be unique per user
    # study must be either "S1" or "S2"
    # view must be either "table" or "map"
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    study: Mapped[str] = mapped_column(String(2), nullable=False)   # "S1" | "S2"
    view: Mapped[str] = mapped_column(String(5), nullable=False)    # "table" | "map"
    filters: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # constraints that are enforced at the database level
    # utilizes the UniqueConstraint and CheckConstraint features of SQLAlchemy
    # and uses the __table_args__ attribute to define them
    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_presets_user_id_name"),
        CheckConstraint("study IN ('S1','S2')", name="ck_presets_study"),
        CheckConstraint("view IN ('table','map')", name="ck_presets_view"),
    )

    # relationship to User model
    user = relationship("User", back_populates="presets")