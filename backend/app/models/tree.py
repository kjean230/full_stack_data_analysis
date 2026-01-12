# tree.py
# This file defines the Tree model for the application.
from __future__ import annotations

from datetime import datetime
from typing import Optional

from geoalchemy2 import Geometry
from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Float,
    Index,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Tree(Base):
    __tablename__ = "trees"

    # Internal surrogate key (stable for APIs, joins, future references)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Source dataset identifier (traceability + dedupe across ETL re-runs)
    census_tree_id: Mapped[str] = mapped_column(String(64), nullable=False)

    # Census year
    year: Mapped[int] = mapped_column(Integer, nullable=False)

    # Location + geo
    borough: Mapped[str] = mapped_column(String(50), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    location: Mapped[bytes] = mapped_column(
        Geometry(geometry_type="POINT", srid=4326),
        nullable=False,
    )

    # Tree attributes
    species: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    health: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)        # Good/Fair/Poor
    health_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)     # 2/1/0
    dbh: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    __table_args__ = (
        # Prevent duplicates on re-run (year-scoped)
        UniqueConstraint("year", "census_tree_id", name="uq_trees_year_census_tree_id"),

        # Filter/query indexes
        Index("ix_trees_year_borough", "year", "borough"),
        Index("ix_trees_year_species", "year", "species"),
        Index("ix_trees_year_health", "year", "health"),

        # Spatial index for bbox queries
        Index("ix_trees_location", "location", mysql_using="SPATIAL"),

        # Validation
        CheckConstraint("year IN (1995, 2005, 2015)", name="ck_trees_year"),
        CheckConstraint("health IN ('Good', 'Fair', 'Poor') OR health IS NULL", name="ck_trees_health"),
        CheckConstraint("health_score IN (0, 1, 2) OR health_score IS NULL", name="ck_trees_health_score"),
        CheckConstraint("latitude BETWEEN -90 AND 90", name="ck_trees_latitude"),
        CheckConstraint("longitude BETWEEN -180 AND 180", name="ck_trees_longitude"),
    )
