from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from db.task_operations import (
    create_task as sync_create_task,
    get_tasks as sync_get_tasks,
    toggle_task as sync_toggle_task,
    delete_task as sync_delete_task,
    update_task as sync_update_task
)
from db.connection import get_session
from sqlmodel import Session

# Define Pydantic models for request/response
class AddTaskRequest(BaseModel):
    user_id: str
    title: str
    description: Optional[str] = None

class AddTaskResponse(BaseModel):
    task_id: int
    status: str
    title: str

class ListTasksRequest(BaseModel):
    user_id: str
    status: Optional[str] = "all"  # "all", "pending", "completed"

class TaskItem(BaseModel):
    serial_number: int
    title: str
    completed: bool
    created_at: str

class ListTasksResponse(BaseModel):
    tasks: List[TaskItem]

class CompleteTaskRequest(BaseModel):
    user_id: str
    task_id: int

class CompleteTaskResponse(BaseModel):
    task_id: int
    status: str
    title: str

class DeleteTaskRequest(BaseModel):
    user_id: str
    task_id: int

class DeleteTaskResponse(BaseModel):
    task_id: int
    status: str
    title: str

class UpdateTaskRequest(BaseModel):
    user_id: str
    task_id: int
    title: Optional[str] = None
    description: Optional[str] = None

class UpdateTaskResponse(BaseModel):
    task_id: int
    status: str
    title: str

# MCP Tool 1: add_task
async def add_task(user_id: str, title: str, description: Optional[str] = None) -> Dict[str, Any]:
    """
    Add a new task to the user's todo list
    """
    try:
        # Use synchronous function within async context
        from db.connection import get_session
        from models.task import Task
        from db.serial_view import get_tasks_with_serial

        with next(get_session()) as session:
            task = sync_create_task(session, user_id, title, description or "")

            # Get the newly created task's serial number
            tasks_with_serial = get_tasks_with_serial(session, user_id)
            new_task_serial = None
            for t in tasks_with_serial:
                if t['id'] == task.id:
                    new_task_serial = t['serial_number']
                    break

        return {
            "task_id": new_task_serial or 0,  # Return serial number instead of UUID
            "status": "created",
            "title": task.title
        }
    except Exception as e:
        return {
            "error": f"Failed to add task: {str(e)}"
        }

# MCP Tool 2: list_tasks
async def list_tasks(user_id: str, status: str = "all") -> Dict[str, Any]:
    """
    List tasks from the user's todo list with optional filtering
    """
    try:
        # Use synchronous function within async context
        from db.connection import get_session
        from models.task import Task

        with next(get_session()) as session:
            # Map status to completed filter
            completed_filter = None
            if status == "pending":
                completed_filter = False
            elif status == "completed":
                completed_filter = True

            tasks = sync_get_tasks(session, user_id, completed_filter)

        # Get tasks with serial numbers using the view
        from db.serial_view import get_tasks_with_serial
        tasks_with_serial = get_tasks_with_serial(session, user_id)

        # Apply status filter if needed
        if status == "pending":
            tasks_with_serial = [t for t in tasks_with_serial if not t['completed']]
        elif status == "completed":
            tasks_with_serial = [t for t in tasks_with_serial if t['completed']]

        # Format the tasks to match the expected response
        formatted_tasks = [
            TaskItem(
                serial_number=task['serial_number'],
                title=task['title'],
                completed=task['completed'],
                created_at=str(task['created_at'])
            ).dict() for task in tasks_with_serial
        ]

        return {
            "tasks": formatted_tasks
        }
    except Exception as e:
        return {
            "error": f"Failed to list tasks: {str(e)}"
        }

# MCP Tool 3: complete_task
async def complete_task(user_id: str, task_id: int) -> Dict[str, Any]:
    """
    Mark a task as completed
    """
    try:
        # Use synchronous functions within async context
        from db.connection import get_session
        from models.task import Task

        with next(get_session()) as session:
            # Get the task by serial number using the view
            from db.serial_view import get_task_by_serial
            task = get_task_by_serial(session, user_id, task_id)

            if not task:
                return {
                    "error": "Task not found"
                }

            # Toggle the task completion status using the actual task UUID
            toggled_task = sync_toggle_task(session, task['id'], user_id)

        if toggled_task:
            return {
                "task_id": task_id,
                "status": "completed",
                "title": toggled_task.title  # toggled_task is an object from sync_toggle_task
            }
        else:
            return {
                "error": "Failed to complete task"
            }
    except Exception as e:
        return {
            "error": f"Failed to complete task: {str(e)}"
        }

# MCP Tool 4: delete_task
async def delete_task(user_id: str, task_id: int) -> Dict[str, Any]:
    """
    Delete a task from the user's list
    """
    try:
        # Use synchronous functions within async context
        from db.connection import get_session
        from models.task import Task

        with next(get_session()) as session:
            # Get the task by serial number using the view
            from db.serial_view import get_task_by_serial
            task = get_task_by_serial(session, user_id, task_id)

            if not task:
                return {
                    "error": "Task not found"
                }

            # Delete the task using the actual task UUID
            success = sync_delete_task(session, task['id'], user_id)

        if success:
            return {
                "task_id": task_id,
                "status": "deleted",
                "title": task['title']
            }
        else:
            return {
                "error": "Failed to delete task"
            }
    except Exception as e:
        return {
            "error": f"Failed to delete task: {str(e)}"
        }

# MCP Tool 5: update_task
async def update_task(user_id: str, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Dict[str, Any]:
    """
    Update task fields in the database
    """
    try:
        # Use synchronous functions within async context
        from db.connection import get_session
        from models.task import Task

        with next(get_session()) as session:
            # Get the task by serial number using the view
            from db.serial_view import get_task_by_serial
            task = get_task_by_serial(session, user_id, task_id)

            if not task:
                return {
                    "error": "Task not found"
                }

            # Prepare update data
            update_data = {}
            if title is not None:
                update_data["title"] = title
            if description is not None:
                update_data["description"] = description

            # Update the task using the actual task UUID
            updated_task = sync_update_task(session, task['id'], user_id, update_data)

        if updated_task:
            return {
                "task_id": task_id,
                "status": "updated",
                "title": updated_task.title  # updated_task is an object from sync_update_task
            }
        else:
            return {
                "error": "Task not found or failed to update"
            }
    except Exception as e:
        return {
            "error": f"Failed to update task: {str(e)}"
        }