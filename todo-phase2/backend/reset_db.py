"""
Script to reset the database schema to match the new User model.
"""
from sqlmodel import SQLModel, text
from db.connection import engine

def reset_database():
    """Drop all tables and recreate them with the new schema."""
    print("Dropping all tables...")

    # Reflect and drop all tables
    from models.user import User
    from models.refresh_token import RefreshToken
    from models.task import Task

    # Drop all tables
    SQLModel.metadata.drop_all(engine)
    print("All tables dropped.")

    # Create all tables with new schema
    print("Creating tables with new schema...")
    SQLModel.metadata.create_all(engine)
    print("Tables created with new schema successfully!")

    print("\nDatabase reset complete!")
    print("- Users table now has: id, name, email, password_hash, created_at, updated_at")
    print("- All old data has been cleared")

if __name__ == "__main__":
    reset_database()