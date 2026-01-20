from __future__ import annotations

import uuid
from datetime import datetime
from sqlalchemy import BigInteger, CheckConstraint, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

# dataset table to store information about datasets uploaded by users
# will store metadata about the dataset and its processing status
# will have relationships to dataset columns and charts generated from the dataset
# will also have a relationship to the user who uploaded the dataset
# status can be 'uploaded', 'profiling', 'ready', 'failed'
# however, may only accept csv and possible excel files for now
class Dataset(Base):
    __tablename__ = "datasets"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4))
    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="uploaded")

    # FILE PATHS
    # these will be the paths to the raw and processed dataset files
    raw_path: Mapped[str] = mapped_column(String(500), nullable=False)
    parquet_path: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Metadata about the dataset for quick access
    row_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    column_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    file_size_bytes: Mapped[int] = mapped_column(BigInteger, nullable=False)
    error_message: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    # Timestamps for data tracking
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # constraints for status field
    __table_args__ = (
        CheckConstraint(
            "status IN ('uploaded', 'profiling', 'ready', 'failed')",
            name="ck_datasets_status"
        ),
    )

    # Relationships
    user = relationship("User", back_populates="datasets")
    columns = relationship("DatasetColumn", back_populates="dataset", cascade="all, delete-orphan")
    charts = relationship("Chart", back_populates="dataset", cascade="all, delete-orphan")