from __future__ import annotations
import uuid 
from datetime import datetime
from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

class User(Base):
    pass