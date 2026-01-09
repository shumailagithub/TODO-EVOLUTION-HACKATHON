"""
Password hashing and verification utilities.
Uses bcrypt directly for secure password storage.
"""
import bcrypt
from typing import NewType


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt directly.

    Args:
        password: Plain text password

    Returns:
        Hashed password string (different each call due to salt)
    """
    # Encode to UTF-8 and truncate to 72 bytes to comply with bcrypt limitations
    password_bytes = password.encode('utf-8')[:72]
    # Generate salt and hash with 12 rounds
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain: str, hashed: str) -> bool:
    """
    Verify a password against a hash.

    Args:
        plain: Plain text password
        hashed: Hashed password to verify against

    Returns:
        True if password matches hash, False otherwise
    """
    # Encode to UTF-8 and truncate to 72 bytes to comply with bcrypt limitations
    password_bytes = plain.encode('utf-8')[:72]
    hashed_bytes = hashed.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)
