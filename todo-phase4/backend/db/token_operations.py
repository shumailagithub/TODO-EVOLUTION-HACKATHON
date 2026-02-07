"""
Refresh token CRUD database operations.
"""
from typing import Optional
from datetime import datetime
from sqlmodel import Session, select, delete
from models.refresh_token import RefreshToken


def create_refresh_token(
    session: Session,
    user_id: str,
    token_id: str,
    expires_at: datetime
) -> RefreshToken:
    """
    Create a new refresh token in the database.

    Args:
        session: Database session
        user_id: User ID
        token_id: Token unique identifier (jti from JWT)
        expires_at: Expiration datetime

    Returns:
        Created RefreshToken object
    """
    refresh_token = RefreshToken(
        user_id=user_id,
        token_id=token_id,
        expires_at=expires_at
    )
    session.add(refresh_token)
    session.commit()
    session.refresh(refresh_token)
    return refresh_token


def get_refresh_token(session: Session, token_id: str) -> Optional[RefreshToken]:
    """
    Retrieve a refresh token by token_id.

    Args:
        session: Database session
        token_id: Token unique identifier (jti)

    Returns:
        RefreshToken object if found, None otherwise
    """
    return session.exec(
        select(RefreshToken).where(RefreshToken.token_id == token_id)
    ).first()


def delete_refresh_token(session: Session, token_id: str) -> None:
    """
    Delete a refresh token from the database.

    Args:
        session: Database session
        token_id: Token unique identifier (jti)
    """
    session.exec(
        delete(RefreshToken).where(RefreshToken.token_id == token_id)
    )
    session.commit()


def delete_all_user_tokens(session: Session, user_id: str) -> None:
    """
    Delete all refresh tokens for a specific user.

    Args:
        session: Database session
        user_id: User ID
    """
    session.exec(
        delete(RefreshToken).where(RefreshToken.user_id == user_id)
    )
    session.commit()
