# backend\services\agent_service.py
import os
from typing import List, Tuple
from openai import OpenAI
from dotenv import load_dotenv

# Import MCP tools at the top of the file
from mcp.server import (
    add_task,
    list_tasks,
    complete_task,
    delete_task,
    update_task
)
from .intent_parser import IntentParser, IntentType

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def process_user_message(user_id: str, conversation_history: List[dict], user_message: str) -> Tuple[str, List[str]]:
    """
    Process user message through strict intent-based parsing with fallback to OpenAI agent
    """
    intent_parser = IntentParser()

    # First, try strict intent parsing
    intent_type, params = intent_parser.parse(user_message)

    # Validate strict execution rules
    is_valid, error_msg = intent_parser.validate_strict_execution(intent_type, params)

    if not is_valid:
        return f"⚠️ {error_msg}", ["clarification_needed"]

    if intent_type == IntentType.CLARIFICATION_NEEDED:
        # Provide helpful suggestions
        suggestions = params.get("suggestions", [])
        response = "I'm not sure what you mean. Could you try one of these formats?\n"
        response += "\n".join([f"• {suggestion}" for suggestion in suggestions])
        return response, ["clarification_needed"]

    # Execute the appropriate task service method based on intent
    try:
        if intent_type == IntentType.ADD_TASK:
            # Ensure we never create a task unless intent is explicitly ADD_TASK
            result = await add_task(user_id, params['title'])
            if "error" in result:
                return f"⚠️ {result['error']}", ["error"]
            assistant_response = f"✅ Task '{result.get('title', 'unnamed task')}' added successfully."
            return assistant_response, ["add_task"]

        elif intent_type == IntentType.DELETE_TASK:
            # Validate that task_id is provided and is numeric
            if 'task_id' not in params:
                # If only title is provided, we need to find the task ID first
                # For now, return an error as the strict mode requires explicit IDs
                return "⚠️ Please specify the task by its ID number (e.g., 'delete task 2')", ["error"]

            task_id = params['task_id']
            if not isinstance(task_id, int):
                task_id = int(task_id) if str(task_id).isdigit() else None

            if not task_id:
                return "⚠️ Invalid task ID provided", ["error"]

            result = await delete_task(user_id, task_id)
            if "error" in result:
                # If the error is "Task not found", treat as successful deletion
                if "Task not found" in result['error']:
                    return f"🗑️ Task #{task_id} deleted successfully.", ["delete_task"]
                else:
                    return f"⚠️ {result['error']}", ["error"]
            assistant_response = f"🗑️ Task #{task_id} '{result.get('title', 'unnamed task')}' deleted successfully."
            return assistant_response, ["delete_task"]

        elif intent_type == IntentType.COMPLETE_TASK:
            # Validate that task_id is provided and is numeric
            if 'task_id' not in params:
                return "⚠️ Please specify the task by its ID number (e.g., 'mark task 2 as done')", ["error"]

            task_id = params['task_id']
            if not isinstance(task_id, int):
                task_id = int(task_id) if str(task_id).isdigit() else None

            if not task_id:
                return "⚠️ Invalid task ID provided", ["error"]

            result = await complete_task(user_id, task_id)
            if "error" in result:
                return f"⚠️ {result['error']}", ["error"]
            assistant_response = f"✅ Task #{task_id} '{result.get('title', 'unnamed task')}' marked as completed."
            return assistant_response, ["complete_task"]

        elif intent_type == IntentType.LIST_TASKS:
            result = await list_tasks(user_id)
            if "error" in result:
                return f"⚠️ {result['error']}", ["error"]

            tasks = result.get('tasks', [])
            if not tasks:
                assistant_response = "You have 0 tasks."
            else:
                pending_tasks = [t for t in tasks if not t.get('completed', False)]

                if pending_tasks:
                    response_parts = [f"You have {len(pending_tasks)} tasks:"]
                    for i, task in enumerate(pending_tasks, 1):
                        response_parts.append(f"{i}. {task['title']}")
                    assistant_response = "\n".join(response_parts)
                else:
                    assistant_response = "You have 0 tasks."
            return assistant_response, ["list_tasks"]

        elif intent_type == IntentType.UPDATE_TASK:
            # Validate that task_id is provided and is numeric
            if 'task_id' not in params:
                return "⚠️ Please specify the task by its ID number (e.g., 'update task 2 to new title')", ["error"]

            task_id = params['task_id']
            if not isinstance(task_id, int):
                task_id = int(task_id) if str(task_id).isdigit() else None

            if not task_id:
                return "⚠️ Invalid task ID provided", ["error"]

            new_title = params.get('new_title', '').strip()
            if not new_title:
                return "⚠️ New title is required for updating a task", ["error"]

            result = await update_task(user_id, task_id, title=new_title)
            if "error" in result:
                return f"⚠️ {result['error']}", ["error"]
            assistant_response = f"✅ Task #{task_id} '{result.get('title', 'unnamed task')}' updated successfully."
            return assistant_response, ["update_task"]

        else:
            # Fallback to original OpenAI agent-based approach for any other cases
            return await process_with_openai_agent(user_id, conversation_history, user_message)

    except ValueError as e:
        return f"⚠️ Invalid input: {str(e)}", ["error"]
    except Exception as e:
        print(f"Error processing user message with strict intent: {str(e)}")
        # Fallback to original approach if strict parsing fails
        return await process_with_openai_agent(user_id, conversation_history, user_message)


async def process_with_openai_agent(user_id: str, conversation_history: List[dict], user_message: str) -> Tuple[str, List[str]]:
    """
    Original OpenAI agent-based processing as fallback
    """
    # Prepare the conversation history for the agent
    messages = [
        {
            "role": "system",
            "content": "You are a helpful task management assistant. Help users manage their todo list using natural language. Always respond in a friendly, conversational way and confirm actions taken. Available tools: add_task, list_tasks, complete_task, delete_task, update_task."
        }
    ]

    # Add conversation history
    for msg in conversation_history:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    # Add the current user message
    messages.append({
        "role": "user",
        "content": user_message
    })

    # Define available tools
    tools = [
        {
            "type": "function",
            "function": {
                "name": "add_task",
                "description": "Add a new task to the user's todo list",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The user's ID"},
                        "title": {"type": "string", "description": "The task title"},
                        "description": {"type": "string", "description": "Optional task description"}
                    },
                    "required": ["user_id", "title"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "list_tasks",
                "description": "List tasks from the user's todo list",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The user's ID"},
                        "status": {"type": "string", "enum": ["all", "pending", "completed"], "description": "Filter tasks by status"}
                    },
                    "required": ["user_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "complete_task",
                "description": "Mark a task as completed",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The user's ID"},
                        "task_id": {"type": "integer", "description": "The ID of the task to complete"}
                    },
                    "required": ["user_id", "task_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "delete_task",
                "description": "Delete a task from the user's list",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The user's ID"},
                        "task_id": {"type": "integer", "description": "The ID of the task to delete"}
                    },
                    "required": ["user_id", "task_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "update_task",
                "description": "Update a task in the user's list",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The user's ID"},
                        "task_id": {"type": "integer", "description": "The ID of the task to update"},
                        "title": {"type": "string", "description": "New title for the task"},
                        "description": {"type": "string", "description": "New description for the task"}
                    },
                    "required": ["user_id", "task_id"]
                }
            }
        }
    ]

    try:
        # Call OpenAI with tools
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        # Process tool calls if any
        if tool_calls:
            tool_call_results = []
            tool_names_called = []

            for tool_call in tool_calls:
                function_name = tool_call.function.name
                tool_names_called.append(function_name)

                # Parse the function arguments safely
                import json
                try:
                    function_args = json.loads(tool_call.function.arguments)
                except json.JSONDecodeError:
                    result = {"error": f"Invalid arguments for {function_name}"}
                    continue

                # Call the already imported tool functions
                if function_name == "add_task":
                    result = await add_task(**function_args)
                elif function_name == "list_tasks":
                    result = await list_tasks(**function_args)
                elif function_name == "complete_task":
                    result = await complete_task(**function_args)
                elif function_name == "delete_task":
                    result = await delete_task(**function_args)
                elif function_name == "update_task":
                    result = await update_task(**function_args)
                else:
                    result = {"error": f"Unknown tool: {function_name}"}

                tool_call_results.append(result)

            # Generate final response based on tool results with specific, strict responses
            if function_name == "add_task" and "error" not in result:
                assistant_response = f"✅ Task '{result.get('title', 'unnamed task')}' added successfully."
            elif function_name == "complete_task" and "error" not in result:
                task_id = function_args.get('task_id', 'unknown')
                assistant_response = f"✅ Task #{task_id} '{result.get('title', 'unnamed task')}' marked as completed."
            elif function_name == "delete_task":
                task_id = function_args.get('task_id', 'unknown')
                if "error" not in result:
                    assistant_response = f"🗑️ Task #{task_id} '{result.get('title', 'unnamed task')}' deleted successfully."
                else:
                    # If the error is "Task not found", treat as successful deletion
                    if "Task not found" in result.get('error', ''):
                        assistant_response = f"🗑️ Task #{task_id} deleted successfully."
                    else:
                        assistant_response = f"⚠️ {result.get('error', 'An error occurred processing your request.')}"
            elif function_name == "update_task" and "error" not in result:
                task_id = function_args.get('task_id', 'unknown')
                assistant_response = f"✅ Task #{task_id} '{result.get('title', 'unnamed task')}' updated successfully."
            elif function_name == "list_tasks" and "error" not in result:
                tasks = result.get('tasks', [])
                pending_tasks = [t for t in tasks if not t.get('completed', False)]

                if pending_tasks:
                    response_parts = [f"You have {len(pending_tasks)} tasks:"]
                    for i, task in enumerate(pending_tasks, 1):
                        response_parts.append(f"{i}. {task['title']}")
                    assistant_response = "\n".join(response_parts)
                else:
                    assistant_response = "You have 0 tasks."
            else:
                if "error" in result:
                    assistant_response = f"⚠️ {result.get('error', 'An error occurred processing your request.')}"
                else:
                    assistant_response = "I've processed your request. Let me know if you'd like me to do anything else!"
        else:
            # If no tools were called, just return the agent's message
            assistant_response = response_message.content or "I'm here to help manage your tasks. What would you like to do?"
            tool_names_called = []

        return assistant_response, tool_names_called

    except Exception as e:
        print(f"Error processing user message: {str(e)}")
        return "Sorry, I encountered an error processing your request. Please try again.", []