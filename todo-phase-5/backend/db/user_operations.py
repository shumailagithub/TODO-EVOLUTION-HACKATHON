"""
User CRUD database operations.
"""
from typing import Optional
from sqlmodel import Session, select
from models.user import User


def create_user(session: Session, name: str, email: str, password_hash: str) -> User:
    """
    Create a new user in the database.

    Args:
        session: Database session
        name: User's full name
        email: User's email (must be unique)
        password_hash: Hashed password

    Returns:
        Created User object

    Raises:
        ValueError: If email already exists
    """
    # Check if email already exists
    existing_user = session.exec(
        select(User).where(User.email == email)
    ).first()

    if existing_user:
        raise ValueError(f"Email '{email}' already exists")

    user = User(name=name, email=email, password_hash=password_hash)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_user_by_email(session: Session, email: str) -> Optional[User]:
    """
    Retrieve a user by email.

    Args:
        session: Database session
        email: Email to search for

    Returns:
        User object if found, None otherwise
    """
    return session.exec(
        select(User).where(User.email == email)
    ).first()


def get_user_by_id(session: Session, user_id: str) -> Optional[User]:
    """
    Retrieve a user by ID.

    Args:
        session: Database session
        user_id: User ID (UUID string)

    Returns:
        User object if found, None otherwise
    """
    return session.exec(
        select(User).where(User.id == user_id)
    ).first()
