"""SQLAlchemy models for the application."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from .database import Base


class User(Base):
    """User model with username, email, password_hash, and created_at."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)