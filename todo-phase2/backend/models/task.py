"""
Task database model.
"""
from datetime import datetime
from sqlmodel import SQLModel, Field
from uuid import uuid4
from typing import Optional


class Task(SQLModel, table=True):
    """Task model for user todo items."""

    __tablename__ = "tasks"

    id: str = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True
    )
    user_id: str = Field(
        foreign_key="users.id"
    )
    title: str = Field(
        max_length=200
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000
    )
    completed: bool = Field(
        default=False
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow
    )
