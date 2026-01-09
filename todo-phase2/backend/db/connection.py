"""
Database connection and session management.
Configured for NeonDB (serverless PostgreSQL).
"""
from sqlmodel import Session, create_engine
from sqlalchemy import text
from sqlalchemy.engine import Engine
from typing import Generator
from config import DATABASE_URL

# NeonDB Connection Requirements:
# - SSL is required: connection string must include ?sslmode=require
# - Format: postgresql://username:password@host/dbname?sslmode=require
# - Serverless architecture: connections are pooled and auto-scaled

# Create SQLAlchemy engine with NeonDB-optimized settings
engine = create_engine(
    DATABASE_URL,
    # Connection pool settings for serverless databases
    pool_size=5,              # Number of persistent connections
    max_overflow=10,          # Additional connections when pool is full
    pool_pre_ping=True,       # Verify connections before using (critical for serverless)
    pool_recycle=3600,        # Recycle connections after 1 hour
    echo=False,               # Set to True for SQL query logging in development
    connect_args={
        "connect_timeout": 10,  # Connection timeout in seconds
    }
)


def get_engine() -> Engine:
    """
    Returns the SQLAlchemy engine instance.

    Returns:
        Engine: The configured database engine
    """
    return engine


def get_session() -> Generator[Session, None, None]:
    """
    Dependency function that yields a database session.
    Used with FastAPI's Depends() for automatic session management.
    The session is properly closed after use.

    Yields:
        Session: Database session for executing queries
    """
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()


def test_connection() -> bool:
    """
    Test database connection.
    Useful for health checks and startup validation.

    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        with Session(engine) as session:
            session.exec(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False
