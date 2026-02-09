#!/usr/bin/env python3
"""
Test script that removes problematic paths before importing the application.
"""

import sys
import os

def remove_problematic_paths():
    """Remove problematic paths from sys.path."""
    problematic_path = r"D:\hackathons-piaic\Hackathon-2\todo-evolution\src"

    # Remove the problematic path if it exists
    if problematic_path in sys.path:
        sys.path.remove(problematic_path)
        print(f"REMOVED: {problematic_path}")

    # Also check for similar patterns
    paths_to_remove = []
    for path in sys.path:
        if "todo-evolution" in path and "src" in path.split(os.sep)[-1:]:
            if path != os.path.join(os.getcwd(), "src"):  # Don't remove local src
                paths_to_remove.append(path)

    for path in paths_to_remove:
        sys.path.remove(path)
        print(f"REMOVED: {path}")

def test_chat():
    print("Starting chat functionality test...")
    print(f"Current working directory: {os.getcwd()}")

    # Clean up problematic paths
    remove_problematic_paths()

    print("\nUpdated sys.path:")
    for i, path in enumerate(sys.path[:10]):  # Show first 10 paths
        print(f"  {i}: {path}")
    if len(sys.path) > 10:
        print(f"  ... and {len(sys.path) - 10} more")

    # Now try to import and test the chat functionality
    try:
        from services.agent_service import process_user_message
        import asyncio

        print("\nSUCCESS: Successfully imported chat functionality!")

        # Mock conversation history
        conversation_history = []

        # Test a simple message
        async def run_test():
            try:
                response, tool_calls = await process_user_message(
                    user_id="test_user",
                    conversation_history=conversation_history,
                    user_message="Add a test task"
                )
                print(f"Response: {response}")
                print(f"Tool calls: {tool_calls}")
                return True
            except Exception as e:
                print(f"Error during chat processing: {e}")
                import traceback
                traceback.print_exc()
                return False

        # Run the async test
        success = asyncio.run(run_test())
        if success:
            print("\nSUCCESS: Chat functionality test PASSED!")
        else:
            print("\nFAILED: Chat functionality test FAILED!")

    except ImportError as e:
        print(f"\nERROR: Import error: {e}")
        print("This indicates there are still import issues to resolve.")
        import traceback
        traceback.print_exc()
    except Exception as e:
        print(f"\nERROR: Unexpected error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_chat()