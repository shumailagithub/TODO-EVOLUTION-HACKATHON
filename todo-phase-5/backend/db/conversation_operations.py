"""
Conversation and message database operations.
Manages chat conversation history and message storage.
"""
from typing import List
from sqlmodel import Session, select
from datetime import datetime
from .connection import get_session
from models.conversation import Conversation
from models.message import Message, Role


async def create_conversation(user_id: str) -> int:
    """
    Create a new conversation for the user.

    Args:
        user_id: User ID

    Returns:
        ID of the created conversation
    """
    with next(get_session()) as session:
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation.id


async def get_conversation_history(conversation_id: int) -> List[dict]:
    """
    Get all messages in a conversation.

    Args:
        conversation_id: Conversation ID

    Returns:
        List of message dictionaries
    """
    with next(get_session()) as session:
        statement = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.asc())

        results = session.exec(statement)
        messages = results.all()

        return [
            {
                "role": msg.role,
                "content": msg.content
            }
            for msg in messages
        ]


async def add_message(conversation_id: int, user_id: str, role: str, content: str) -> int:
    """
    Add a message to a conversation.

    Args:
        conversation_id: Conversation ID
        user_id: User ID
        role: Message role ('user' or 'assistant')
        content: Message content

    Returns:
        ID of the created message
    """
    with next(get_session()) as session:
        message = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role=role,
            content=content
        )
        session.add(message)
        session.commit()
        session.refresh(message)
        return message.id