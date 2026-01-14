"""
Authentication API endpoints.
Handles user registration, login, refresh, and logout.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from pydantic import BaseModel
from typing import Annotated
from db.connection import get_session
from db.user_operations import create_user, get_user_by_email
from db.token_operations import (
    create_refresh_token,
    delete_refresh_token
)
from auth.password import hash_password, verify_password
from auth.tokens import generate_access_token, generate_refresh_token
from auth.dependencies import get_current_user
from models.user import User


# Request/Response Models
class LoginRequest(BaseModel):
    """Request model for user login."""
    email: str
    password: str


class RegisterRequest(BaseModel):
    """Request model for user registration."""
    name: str
    email: str
    password: str


class RefreshTokenRequest(BaseModel):
    """Request model for token refresh."""
    refresh_token: str


class AuthResponse(BaseModel):
    """Response model with tokens and user info."""
    access_token: str
    refresh_token: str
    user_id: str
    name: str
    email: str


# API Router
router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=AuthResponse)
async def register(
    request: RegisterRequest,
    session: Session = Depends(get_session)
) -> AuthResponse:
    """
    Register a new user account.

    Args:
        request: Name, email, and password
        session: Database session

    Returns:
        AuthResponse with access and refresh tokens

    Raises:
        HTTPException: 400 for invalid input
        HTTPException: 409 for existing email
    """
    # Validate email format
    import re
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, request.email):
        raise HTTPException(
            status_code=400,
            detail="Invalid email format"
        )

    # Validate password length
    if len(request.password) < 8:
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 8 characters"
        )

    # Validate name length
    if len(request.name.strip()) < 1:
        raise HTTPException(
            status_code=400,
            detail="Name cannot be empty"
        )

    # Check if email already exists
    existing_user = get_user_by_email(session, request.email)
    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email is already registered"
        )

    # Hash password
    password_hash = hash_password(request.password)

    # Create user
    from datetime import timedelta, datetime
    user = create_user(session, request.name, request.email, password_hash)

    # Generate tokens
    access_token = generate_access_token(str(user.id))
    refresh_token = generate_refresh_token(str(user.id))

    # Extract jti from refresh token for database storage
    from auth.tokens import decode_token
    refresh_payload = decode_token(refresh_token)
    token_id = refresh_payload.get("jti")

    # Store refresh token in database
    refresh_token_obj = create_refresh_token(
        session,
        user_id=str(user.id),
        token_id=token_id,
        expires_at=datetime.utcnow() + timedelta(days=7)
    )

    return AuthResponse(
        access_token=access_token,
        refresh_token=refresh_token,  # Return the JWT token, not token_id
        user_id=str(user.id),
        name=user.name,
        email=user.email
    )


@router.post("/login", response_model=AuthResponse)
async def login(
    request: LoginRequest,
    session: Session = Depends(get_session)
) -> AuthResponse:
    """
    Authenticate user and return tokens.

    Args:
        request: Email and password
        session: Database session

    Returns:
        AuthResponse with access and refresh tokens

    Raises:
        HTTPException: 400 for missing fields
        HTTPException: 401 for invalid credentials
    """
    if not request.email or not request.password:
        raise HTTPException(
            status_code=400,
            detail="Email and password are required"
        )

    # Find user by email
    user = get_user_by_email(session, request.email)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Verify password
    if not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Generate tokens
    from datetime import timedelta, datetime
    access_token = generate_access_token(str(user.id))
    refresh_token = generate_refresh_token(str(user.id))

    # Extract jti from refresh token for database storage
    from auth.tokens import decode_token
    refresh_payload = decode_token(refresh_token)
    token_id = refresh_payload.get("jti")

    # Store refresh token in database
    refresh_token_obj = create_refresh_token(
        session,
        user_id=str(user.id),
        token_id=token_id,
        expires_at=datetime.utcnow() + timedelta(days=7)
    )

    return AuthResponse(
        access_token=access_token,
        refresh_token=refresh_token,  # Return the JWT token, not token_id
        user_id=str(user.id),
        name=user.name,
        email=user.email
    )


@router.post("/refresh", response_model=dict)
async def refresh_token(
    request: RefreshTokenRequest,
    session: Session = Depends(get_session)
) -> dict:
    """
    Refresh access token using refresh token.

    Args:
        request: Refresh token
        session: Database session

    Returns:
        New access and refresh tokens

    Raises:
        HTTPException: 400 for missing token
        HTTPException: 401 for invalid/expired token
    """
    if not request.refresh_token:
        raise HTTPException(
            status_code=400,
            detail="Refresh token is required"
        )

    # Validate refresh token
    from auth.tokens import decode_token
    try:
        payload = decode_token(request.refresh_token)

        # Verify token type is "refresh"
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=401,
                detail="Invalid token type: expected refresh token"
            )

        # Verify token exists in database and not expired
        from db.token_operations import get_refresh_token
        from datetime import datetime
        token_record = get_refresh_token(session, request.refresh_token)

        if not token_record:
            raise HTTPException(
                status_code=401,
                detail="Refresh token not found or has been revoked"
            )

        if token_record.expires_at < datetime.utcnow():
            raise HTTPException(
                status_code=401,
                detail="Refresh token has expired"
            )

        # Generate new tokens
        user_id = payload.get("sub")
        access_token = generate_access_token(user_id)

        # Revoke old refresh token
        delete_refresh_token(session, request.refresh_token)

        # Create new refresh token
        new_refresh_token_obj = create_refresh_token(
            session,
            user_id=user_id,
            token_id=str(token_record.id) + "_new",  # Unique ID
            expires_at=datetime.utcnow() + timedelta(days=7)
        )
        new_refresh_token = generate_refresh_token(user_id)

        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token_obj.token_id
        }

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired refresh token"
        )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    request: RefreshTokenRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> None:
    """
    Logout user by revoking refresh token.

    Args:
        request: Refresh token to revoke
        current_user: Authenticated user
        session: Database session

    Returns:
        None (204 No Content)

    Raises:
        HTTPException: 400 for missing token
        HTTPException: 401 for invalid access token
    """
    if not request.refresh_token:
        raise HTTPException(
            status_code=400,
            detail="Refresh token is required"
        )

    # Delete refresh token from database
    delete_refresh_token(session, request.refresh_token)
    return None
