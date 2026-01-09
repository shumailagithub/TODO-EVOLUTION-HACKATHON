"""
Password hashing and verification utilities.
Uses bcrypt for secure password storage.
"""
from typing import NewType
from passlib.context import CryptContext

# bcrypt context
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.

    Args:
        password: Plain text password

    Returns:
        Hashed password string (different each call due to salt)
    """
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    """
    Verify a password against a hash.

    Args:
        plain: Plain text password
        hashed: Hashed password to verify against

    Returns:
        True if password matches hash, False otherwise
    """
    return pwd_context.verify(plain, hashed)
