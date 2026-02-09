"""
Test script to verify chat intent handling with Task CRUD operations.
"""
import asyncio
from services.agent_service import process_user_message

async def test_chat_intents():
    """Test various chat intents to ensure they work properly."""

    # Test ADD_TASK intent
    print("Testing ADD_TASK intent...")
    user_id = "test_user_123"
    conversation_history = []

    # Test adding a task
    response, tool_calls = await process_user_message(
        user_id=user_id,
        conversation_history=conversation_history,
        user_message="add buy groceries"
    )
    print(f"Response: {response}")
    print(f"Tool calls: {tool_calls}")
    print()

    # Test LIST_TASKS intent
    print("Testing LIST_TASKS intent...")
    response, tool_calls = await process_user_message(
        user_id=user_id,
        conversation_history=conversation_history,
        user_message="show my tasks"
    )
    print(f"Response: {response}")
    print(f"Tool calls: {tool_calls}")
    print()

    # Test COMPLETE_TASK intent
    print("Testing COMPLETE_TASK intent...")
    response, tool_calls = await process_user_message(
        user_id=user_id,
        conversation_history=conversation_history,
        user_message="mark task 1 as done"
    )
    print(f"Response: {response}")
    print(f"Tool calls: {tool_calls}")
    print()

if __name__ == "__main__":
    asyncio.run(test_chat_intents())