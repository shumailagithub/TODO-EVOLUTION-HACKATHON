import asyncio
import os
from services.agent_service import process_user_message

async def test_chat():
    print("Testing chat functionality...")

    # Mock conversation history
    conversation_history = []

    # Test a simple message
    try:
        response, tool_calls = await process_user_message(
            user_id="test_user",
            conversation_history=conversation_history,
            user_message="Add a test task"
        )
        print(f"Response: {response}")
        print(f"Tool calls: {tool_calls}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_chat())