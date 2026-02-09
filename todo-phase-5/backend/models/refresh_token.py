"""
RefreshToken database model for JWT token management.
"""
from datetime import datetime
from sqlmodel import SQLModel, Field
from uuid import uuid4


class RefreshToken(SQLModel, table=True):
    """RefreshToken model for JWT refresh token storage and revocation."""

    __tablename__ = "refresh_tokens"

    id: str = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True
    )
    user_id: str = Field(
        foreign_key="users.id"
    )
    token_id: str = Field(
        unique=True,
        index=True,
        max_length=255
    )
    expires_at: datetime
    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )
