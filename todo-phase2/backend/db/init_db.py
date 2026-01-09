"""
Database initialization script.
Creates all tables in PostgreSQL database.
"""
from sqlmodel import SQLModel
from db.connection import engine

# CRITICAL: Import all models BEFORE creating tables
# This registers them with SQLModel.metadata
from models.user import User
from models.refresh_token import RefreshToken
from models.task import Task


def create_tables() -> None:
    """
    Create all tables defined in SQLModel metadata.
    """
    print("Creating tables: users, refresh_tokens, tasks...")
    SQLModel.metadata.create_all(engine)
    print("[SUCCESS] Database tables created successfully")


if __name__ == "__main__":
    create_tables()
