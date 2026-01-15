# dataset_column.py

from __future__ import annotations
from sqlalchemy import Boolean, ForeignKey, Integer, JSON, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

class DatasetColumn(Base):
    __tablename__ = "dataset_columns"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    dataset_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("datasets.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False) 
    inferred_type: Mapped[str] = mapped_column(String(50), nullable=False) # data types such as integer, string, date, etc.
    is_nullable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    sample_values: Mapped[dict | None] = mapped_column(JSON, nullable=True) # store first 5-10 sample values as JSON

    __table_args__ = (
        UniqueConstraint("dataset_id", "name", name="uq_dataset_columns_dataset_id_name"),
    )

    # Relationship to Dataset
    dataset = relationship("Dataset", back_populates="columns")