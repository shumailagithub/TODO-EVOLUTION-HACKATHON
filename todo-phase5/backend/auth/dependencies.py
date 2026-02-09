"""
FastAPI authentication dependencies.
Provides token extraction and user authentication for protected routes.
"""
from fastapi import Depends, HTTPException, Header
from sqlmodel import Session
from jose import JWTError
from typing import Annotated
from db.connection import get_session
from auth.tokens import decode_token
from models.user import User
from db.user_operations import get_user_by_id


async def get_access_token(
    authorization: Annotated[str, Header()]
) -> str:
    """
    Extract and validate access token from Authorization header.

    Args:
        authorization: Authorization header value (e.g., "Bearer <token>")

    Returns:
        Token string without "Bearer " prefix

    Raises:
        HTTPException: 401 if header is missing
    """
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header is required"
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Authorization header must start with 'Bearer '"
        )

    return authorization[7:].strip()  # Remove "Bearer " prefix


async def validate_access_token(
    token: Annotated[str, Depends(get_access_token)]
) -> dict:
    """
    Validate and decode access token.

    Args:
        token: JWT token string

    Returns:
        Decoded token payload

    Raises:
        HTTPException: 401 if token is invalid or expired
    """
    try:
        payload = decode_token(token)

        # Verify token type is "access"
        if payload.get("type") != "access":
            raise HTTPException(
                status_code=401,
                detail="Invalid token type: expected access token"
            )

        return payload
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )


async def get_current_user(
    token_payload: Annotated[dict, Depends(validate_access_token)],
    session: Session = Depends(get_session)
) -> User:
    """
    Get currently authenticated user from token and database.

    Args:
        token_payload: Decoded JWT token payload
        session: Database session

    Returns:
        User object

    Raises:
        HTTPException: 401 if user not found or missing
    """
    user_id = token_payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Token payload missing user ID"
        )

    user = get_user_by_id(session, user_id)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user
