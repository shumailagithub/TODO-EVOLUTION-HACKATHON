"""
Script to create only the chat-related database tables without affecting existing data.
This safely adds conversations and messages tables while preserving user and task data.
"""
from sqlmodel import SQLModel
from db.connection import engine

def create_chat_tables():
    """Create only the missing chat-related tables."""
    print("Creating chat-related tables...")

    # Import only the chat-related models
    from models.conversation import Conversation
    from models.message import Message

    # Create only the missing tables (won't drop existing ones)
    SQLModel.metadata.create_all(engine)
    print("Chat-related tables created successfully!")

    print("\nDatabase update complete!")
    print("- Conversations table created")
    print("- Messages table created")
    print("- Existing user and task data preserved")

if __name__ == "__main__":
    create_chat_tables()