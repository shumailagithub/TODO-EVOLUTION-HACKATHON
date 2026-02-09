"""
User database model.
"""
from datetime import datetime
from sqlmodel import SQLModel, Field
from uuid import uuid4
from typing import Optional


class User(SQLModel, table=True):
    """User model for authentication and task ownership."""

    __tablename__ = "users"

    id: str = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True
    )
    name: str = Field(
        max_length=100
    )
    email: str = Field(
        index=True,
        unique=True,
        max_length=100
    )
    password_hash: str = Field(
        max_length=255
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow
    )
