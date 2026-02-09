"""
Database initialization script.
Creates all tables in PostgreSQL database and necessary views.
"""
from sqlmodel import SQLModel
from db.connection import engine
from db.serial_view import create_tasks_with_serial_view
from sqlmodel import Session

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


def initialize_database() -> None:
    """
    Initialize database with tables and views.
    """
    print("Initializing database...")

    # Create tables first
    create_tables()

    # Create views in a separate session
    with Session(engine) as session:
        print("Creating tasks_with_serial view...")
        success = create_tasks_with_serial_view(session)
        if success:
            print("[SUCCESS] tasks_with_serial view created successfully")
        else:
            print("[ERROR] Failed to create tasks_with_serial view")


if __name__ == "__main__":
    initialize_database()
