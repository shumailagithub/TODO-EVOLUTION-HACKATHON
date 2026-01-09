"""
JWT token generation and validation utilities.
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from config import (
    JWT_SECRET,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS
)


def generate_access_token(user_id: str) -> str:
    """
    Generate an access token (short-lived, for API requests).

    Args:
        user_id: User ID string

    Returns:
        JWT access token string
    """
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "sub": user_id,
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    }
    return jwt.encode(to_encode, JWT_SECRET, algorithm="HS256")


def generate_refresh_token(user_id: str) -> str:
    """
    Generate a refresh token (long-lived, for token refresh).

    Args:
        user_id: User ID string

    Returns:
        JWT refresh token string with unique token ID (jti)
    """
    from uuid import uuid4
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    token_id = str(uuid4())  # Unique ID for revocation

    to_encode = {
        "sub": user_id,
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh",
        "jti": token_id
    }
    return jwt.encode(to_encode, JWT_SECRET, algorithm="HS256")


def decode_token(token: str) -> dict:
    """
    Decode and validate a JWT token.

    Args:
        token: JWT token string

    Returns:
        Decoded token payload dictionary

    Raises:
        JWTError: If token is invalid, expired, or malformed
    """
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=["HS256"]
        )
        return payload
    except JWTError as e:
        raise JWTError(f"Invalid token: {str(e)}")
