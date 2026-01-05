from sqlalchemy.orm import DeclarativeBase
from app import models # noqa: F401

class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass