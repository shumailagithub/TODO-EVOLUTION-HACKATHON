from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
import asyncio
from datetime import datetime

from services.agent_service import process_user_message
from db.conversation_operations import (
    create_conversation,
    get_conversation_history,
    add_message
)
from models.message import Role as MessageRole

router = APIRouter()

class ChatRequest(BaseModel):
    conversation_id: Optional[int] = None
    message: str

class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: list[str]

@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat_endpoint(user_id: str, request: ChatRequest):
    """
    Chat endpoint that processes user messages through the AI agent
    """
    try:
        # If no conversation_id provided, create a new conversation
        if request.conversation_id is None:
            conversation_id = await create_conversation(user_id)
        else:
            conversation_id = request.conversation_id

        # Add user message to conversation history
        await add_message(
            conversation_id=conversation_id,
            user_id=user_id,
            role=MessageRole.USER,
            content=request.message
        )

        # Get conversation history to provide context to the agent
        conversation_history = await get_conversation_history(conversation_id)

        # Process the message through the AI agent
        agent_response, tool_calls = await process_user_message(
            user_id=user_id,
            conversation_history=conversation_history,
            user_message=request.message
        )

        # Add assistant response to conversation history
        await add_message(
            conversation_id=conversation_id,
            user_id=user_id,
            role=MessageRole.ASSISTANT,
            content=agent_response
        )

        return ChatResponse(
            conversation_id=conversation_id,
            response=agent_response,
            tool_calls=tool_calls
        )
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Register the router in main.py when needed