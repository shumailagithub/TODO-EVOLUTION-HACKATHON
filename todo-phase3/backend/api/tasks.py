"""
Task API endpoints.
Handles task CRUD operations with user ownership enforcement.
Uses serial_number for user-facing operations, UUIDs internally.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from db.connection import get_session
from auth.dependencies import get_current_user
from db.task_operations import (
    create_task,
    get_tasks,
    get_task_by_id,
    update_task,
    toggle_task,
    delete_task
)
from db.serial_view import get_tasks_with_serial, get_task_by_serial as db_get_task_by_serial


def resolve_serial_number_to_uuid(session: Session, user_id: str, serial_number: int) -> Optional[str]:
    """
    Helper function to resolve serial_number to UUID.

    Args:
        session: Database session
        user_id: User ID
        serial_number: Task serial number

    Returns:
        UUID string if task found, None otherwise
    """
    task_with_serial = db_get_task_by_serial(session, user_id, serial_number)
    if task_with_serial:
        return task_with_serial['id']
    return None


# Internal/Database Models
class TaskInDB(BaseModel):
    """Internal model with UUID for database operations."""
    id: str  # UUID as string
    user_id: str  # UUID as string
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime
    updated_at: datetime


# Request/Response Models
class CreateTaskRequest(BaseModel):
    """Request model for creating a task."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)


class UpdateTaskRequest(BaseModel):
    """Request model for updating a task."""
    serial_number: int = Field(..., ge=1, description="Task serial number")
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = None


class TaskResponse(BaseModel):
    """Response model with task data using serial_number for user-facing."""
    serial_number: int
    id: str  # Use serial number as string ID for frontend compatibility
    title: str
    description: Optional[str] = None
    completed: bool = False  # Ensure default value is provided
    created_at: Optional[datetime] = None
    created_at_formatted: str = ""  # Ensure default value is provided


class ListTasksResponse(BaseModel):
    """Response model for listing tasks."""
    tasks: List[TaskResponse]
    total: int
    pending: int
    completed: int


class TaskItem(BaseModel):
    """User-facing task item with serial_number."""
    serial_number: int
    title: str
    description: Optional[str] = None
    completed: bool
    created_at: Optional[datetime] = None
    created_at_formatted: str


class CreateTaskResponse(BaseModel):
    """Response model for creating a task."""
    serial_number: int
    title: str
    description: Optional[str] = None
    completed: bool
    created_at: Optional[datetime] = None
    created_at_formatted: str


class UpdateTaskResponse(BaseModel):
    """Response model for updating a task."""
    success: bool
    previous_title: Optional[str] = None
    updated_title: Optional[str] = None
    serial_number: int
    created_at: Optional[datetime] = None
    created_at_formatted: str
    chatbot_response: str


# API Router
router = APIRouter(prefix="/api/tasks", tags=["Tasks"])


@router.get("", response_model=ListTasksResponse)
async def get_all_tasks(
    completed: Optional[bool] = None,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> ListTasksResponse:
    """
    Get all tasks for authenticated user using serial numbers.

    Args:
        completed: Optional filter for completion status
        current_user: Authenticated user
        session: Database session

    Returns:
        List of tasks for user with serial numbers
    """
    user_id = current_user.id

    # Query ONLY from tasks_with_serial VIEW
    tasks_with_serial = get_tasks_with_serial(session, user_id)

    # Apply completed filter if specified
    if completed is not None:
        tasks_with_serial = [t for t in tasks_with_serial if t['completed'] == completed]

    # Format tasks using TaskResponse model
    formatted_tasks = []
    for task in tasks_with_serial:
        # Format the created_at datetime
        created_at_dt = task['created_at']
        if isinstance(created_at_dt, str):
            from datetime import datetime
            created_at_dt = datetime.fromisoformat(created_at_dt.replace('Z', '+00:00'))

        formatted_task = TaskResponse(
            serial_number=task['serial_number'],
            id=str(task['serial_number']),  # Use serial number as id for frontend compatibility
            title=task['title'],
            description=task['description'],
            completed=task['completed'],
            created_at=created_at_dt,
            created_at_formatted=created_at_dt.strftime("%Y-%m-%d %H:%M")
        )
        formatted_tasks.append(formatted_task)

    # Calculate statistics
    total = len(formatted_tasks)
    completed_count = sum(1 for t in formatted_tasks if t.completed)
    pending_count = total - completed_count

    return ListTasksResponse(
        tasks=formatted_tasks,
        total=total,
        pending=pending_count,
        completed=completed_count
    )


@router.get("/by-serial/{serial_number}", response_model=TaskResponse)
async def get_task_by_serial(
    serial_number: int,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """
    Get a specific task by serial number.

    Args:
        serial_number: Task serial number
        current_user: Authenticated user
        session: Database session

    Returns:
        Task data if found and belongs to user

    Raises:
        HTTPException: 404 if task not found
        HTTPException: 403 if task belongs to different user
    """
    user_id = current_user.id

    task = db_get_task_by_serial(session, user_id, serial_number)

    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Task with serial number {serial_number} not found"
        )

    # Format the created_at datetime
    created_at_dt = task['created_at']
    if isinstance(created_at_dt, str):
        from datetime import datetime
        created_at_dt = datetime.fromisoformat(created_at_dt.replace('Z', '+00:00'))

    return TaskResponse(
        serial_number=task['serial_number'],
        id=str(task['serial_number']),  # Use serial number as id for frontend compatibility
        title=task['title'],
        description=task['description'],
        completed=task['completed'],
        created_at=created_at_dt,
        created_at_formatted=created_at_dt.strftime("%Y-%m-%d %H:%M")
    )


@router.post("", status_code=status.HTTP_201_CREATED, response_model=TaskResponse)
async def create_task_endpoint(
    request: CreateTaskRequest,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """
    Create a new task for authenticated user.

    Args:
        request: Task data (title, optional description)
        current_user: Authenticated user
        session: Database session

    Returns:
        Created task

    Raises:
        HTTPException: 400 for invalid input
    """
    user_id = current_user.id

    task = create_task(
        session,
        user_id=user_id,
        title=request.title,
        description=request.description
    )

    # Since we just created the task, we need to get all tasks to find the serial number
    all_tasks_with_serial = get_tasks_with_serial(session, user_id)

    # Find the newly created task by matching the ID
    new_task_serial = None
    for t in all_tasks_with_serial:
        if t['id'] == task.id:
            new_task_serial = t['serial_number']
            break

    # If we still don't have a serial number, we need to handle this appropriately
    # The serial number should exist since the view assigns one based on the order of creation
    if new_task_serial is None:
        # As a fallback, we'll get the highest serial number for this user and add 1
        # This shouldn't happen in normal circumstances, but we handle it just in case
        all_user_tasks = get_tasks_with_serial(session, user_id)
        if all_user_tasks:
            # Sort by serial number and get the highest one
            highest_serial = max(t['serial_number'] for t in all_user_tasks)
            new_task_serial = highest_serial + 1
        else:
            # If no tasks exist, this should be serial number 1
            new_task_serial = 1

    # Format the created_at datetime
    created_at_dt = task.created_at
    if isinstance(created_at_dt, str):
        from datetime import datetime
        created_at_dt = datetime.fromisoformat(created_at_dt.replace('Z', '+00:00'))

    return TaskResponse(
        serial_number=new_task_serial,
        id=str(new_task_serial),  # Use serial number as id for frontend compatibility
        title=task.title,
        description=task.description,
        completed=task.completed,
        created_at=created_at_dt,
        created_at_formatted=created_at_dt.strftime("%Y-%m-%d %H:%M")
    )


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task_endpoint(
    task_id: str,
    request: UpdateTaskRequest,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """
    Update an existing task.

    Args:
        task_id: Task UUID
        request: Update data (title, description, completed)
        current_user: Authenticated user
        session: Database session

    Returns:
        Updated task

    Raises:
        HTTPException: 400 for no fields or invalid input
        HTTPException: 404 if task not found
        HTTPException: 403 if task belongs to different user
    """
    user_id = current_user.id

    # Validate at least one field is provided
    if request.title is None and request.description is None and request.completed is None:
        raise HTTPException(
            status_code=400,
            detail="At least one field must be provided"
        )

    # Build update data
    update_data = {}
    if request.title is not None:
        update_data["title"] = request.title
    if request.description is not None:
        update_data["description"] = request.description
    if request.completed is not None:
        update_data["completed"] = request.completed

    # Check if task_id is a serial number (integer) or UUID
    actual_task_id = None

    # Try to interpret as serial number if it's numeric
    if task_id.isdigit():
        serial_num = int(task_id)
        actual_task_id = resolve_serial_number_to_uuid(session, user_id, serial_num)

        if not actual_task_id:
            raise HTTPException(
                status_code=404,
                detail=f"Task with serial number {serial_num} not found"
            )
    else:
        # It's a UUID, verify it exists for this user
        task_check = get_task_by_id(session, task_id, user_id)
        if not task_check:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )
        actual_task_id = task_id

    task = update_task(session, actual_task_id, user_id, update_data)

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    # Get the updated task with its serial number from the view
    all_tasks_with_serial = get_tasks_with_serial(session, user_id)

    # Find the updated task by matching the ID
    updated_task_serial = None
    for t in all_tasks_with_serial:
        if t['id'] == task.id:
            updated_task_serial = t['serial_number']
            break

    # If we still don't have a serial number, we need to handle this appropriately
    # The serial number should exist since the view assigns one based on the order of creation
    if updated_task_serial is None:
        # As a fallback, we'll get the highest serial number for this user and add 1
        # This shouldn't happen in normal circumstances, but we handle it just in case
        all_user_tasks = get_tasks_with_serial(session, user_id)
        if all_user_tasks:
            # Sort by serial number and get the highest one
            highest_serial = max(t['serial_number'] for t in all_user_tasks)
            updated_task_serial = highest_serial + 1
        else:
            # If no tasks exist, this should be serial number 1
            updated_task_serial = 1

    # Format the created_at datetime
    created_at_dt = task.created_at
    if isinstance(created_at_dt, str):
        from datetime import datetime
        created_at_dt = datetime.fromisoformat(created_at_dt.replace('Z', '+00:00'))

    return TaskResponse(
        serial_number=updated_task_serial,
        id=str(updated_task_serial),  # Use serial number as id for frontend compatibility
        title=task.title,
        description=task.description,
        completed=task.completed,
        created_at=created_at_dt,
        created_at_formatted=created_at_dt.strftime("%Y-%m-%d %H:%M")
    )


@router.put("/by-serial/{serial_number}", response_model=UpdateTaskResponse)
async def update_task_by_serial_endpoint(
    serial_number: int,
    request: UpdateTaskRequest,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> UpdateTaskResponse:
    """
    Update an existing task by serial number.

    Args:
        serial_number: Task serial number
        request: Update data (title, description, completed)
        current_user: Authenticated user
        session: Database session

    Returns:
        Updated task with serial number

    Raises:
        HTTPException: 400 for no fields or invalid input
        HTTPException: 404 if task not found
        HTTPException: 403 if task belongs to different user
    """
    user_id = current_user.id

    # Validate that serial number matches the path parameter
    if serial_number != request.serial_number:
        raise HTTPException(
            status_code=400,
            detail="Serial number in path does not match serial number in request"
        )

    # Validate at least one field is provided
    if request.title is None and request.description is None and request.completed is None:
        raise HTTPException(
            status_code=400,
            detail="At least one field (title, description, or completed) must be provided"
        )

    # Validate serial number >= 1
    if serial_number < 1:
        raise HTTPException(
            status_code=400,
            detail="Serial number must be greater than or equal to 1"
        )

    # Resolve serial number to UUID
    task_uuid = resolve_serial_number_to_uuid(session, user_id, serial_number)
    if not task_uuid:
        raise HTTPException(
            status_code=404,
            detail=f"Task with serial number {serial_number} not found"
        )

    # Get the current task to capture previous values
    current_task = get_task_by_id(session, task_uuid, user_id)
    if not current_task:
        raise HTTPException(
            status_code=404,
            detail=f"Task with serial number {serial_number} not found"
        )

    # Build update data
    update_data = {}
    if request.title is not None:
        update_data["title"] = request.title
    if request.description is not None:
        update_data["description"] = request.description
    if request.completed is not None:
        update_data["completed"] = request.completed

    # Update the task using UUID
    updated_task = update_task(session, task_uuid, user_id, update_data)

    if not updated_task:
        raise HTTPException(
            status_code=404,
            detail=f"Task with serial number {serial_number} not found"
        )

    # Format the created_at datetime
    created_at_dt = updated_task.created_at
    if isinstance(created_at_dt, str):
        from datetime import datetime
        created_at_dt = datetime.fromisoformat(created_at_dt.replace('Z', '+00:00'))

    # Create chatbot response
    chatbot_response = f"✏️ Task updated successfully!\nTask #{serial_number}: {updated_task.title}"
    if current_task.title != updated_task.title:
        chatbot_response += f"\nPrevious: {current_task.title}"

    return UpdateTaskResponse(
        success=True,
        previous_title=current_task.title,
        updated_title=updated_task.title,
        serial_number=serial_number,
        created_at=created_at_dt,
        created_at_formatted=created_at_dt.strftime("%Y-%m-%d %H:%M"),
        chatbot_response=chatbot_response
    )


@router.patch("/{task_id}/toggle", response_model=TaskResponse)
async def toggle_task_endpoint(
    task_id: str,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """
    Toggle task completion status. Handles both UUID and serial number.

    Args:
        task_id: Task UUID or serial number
        current_user: Authenticated user
        session: Database session

    Returns:
        Updated task

    Raises:
        HTTPException: 404 if task not found
        HTTPException: 403 if task belongs to different user
    """
    user_id = current_user.id

    # Check if task_id is a serial number (integer) or UUID
    task_uuid = None

    # Try to interpret as serial number if it's numeric
    if task_id.isdigit():
        serial_num = int(task_id)
        task_uuid = resolve_serial_number_to_uuid(session, user_id, serial_num)

        if not task_uuid:
            raise HTTPException(
                status_code=404,
                detail=f"Task with serial number {serial_num} not found"
            )
    else:
        # It's a UUID, verify it exists for this user
        # We need to check if this UUID belongs to this user
        task_check = get_task_by_id(session, task_id, user_id)
        if not task_check:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )
        task_uuid = task_id

    # Toggle the task using the UUID
    task = toggle_task(session, task_uuid, user_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    # Get the toggled task with its serial number from the view
    all_tasks_with_serial = get_tasks_with_serial(session, user_id)

    # Find the toggled task by matching the ID
    toggled_task_serial = None
    for t in all_tasks_with_serial:
        if t['id'] == task.id:
            toggled_task_serial = t['serial_number']
            break

    # If we still don't have a serial number, we need to handle this appropriately
    # The serial number should exist since the view assigns one based on the order of creation
    if toggled_task_serial is None:
        # As a fallback, we'll get the highest serial number for this user and add 1
        # This shouldn't happen in normal circumstances, but we handle it just in case
        all_user_tasks = get_tasks_with_serial(session, user_id)
        if all_user_tasks:
            # Sort by serial number and get the highest one
            highest_serial = max(t['serial_number'] for t in all_user_tasks)
            toggled_task_serial = highest_serial + 1
        else:
            # If no tasks exist, this should be serial number 1
            toggled_task_serial = 1

    # Format the created_at datetime
    created_at_dt = task.created_at
    if isinstance(created_at_dt, str):
        from datetime import datetime
        created_at_dt = datetime.fromisoformat(created_at_dt.replace('Z', '+00:00'))

    return TaskResponse(
        serial_number=toggled_task_serial,
        id=str(toggled_task_serial),  # Use serial number as id for frontend compatibility
        title=task.title,
        description=task.description,
        completed=task.completed,
        created_at=created_at_dt,
        created_at_formatted=created_at_dt.strftime("%Y-%m-%d %H:%M")
    )


@router.patch("/by-serial/{serial_number}/toggle", response_model=TaskResponse)
async def toggle_task_by_serial_endpoint(
    serial_number: int,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """
    Toggle task completion status by serial number.

    Args:
        serial_number: Task serial number
        current_user: Authenticated user
        session: Database session

    Returns:
        Updated task with serial number

    Raises:
        HTTPException: 404 if task not found
        HTTPException: 403 if task belongs to different user
    """
    user_id = current_user.id

    # Resolve serial number to UUID
    task_uuid = resolve_serial_number_to_uuid(session, user_id, serial_number)
    if not task_uuid:
        raise HTTPException(
            status_code=404,
            detail=f"Task with serial number {serial_number} not found"
        )

    # Toggle the task using UUID
    task = toggle_task(session, task_uuid, user_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Task with serial number {serial_number} not found"
        )

    # Get the toggled task with its serial number from the view
    all_tasks_with_serial = get_tasks_with_serial(session, user_id)

    # Find the toggled task by matching the ID
    toggled_task_serial = None
    for t in all_tasks_with_serial:
        if t['id'] == task.id:
            toggled_task_serial = t['serial_number']
            break

    # If we still don't have a serial number, we need to handle this appropriately
    # The serial number should exist since the view assigns one based on the order of creation
    if toggled_task_serial is None:
        # As a fallback, we'll get the highest serial number for this user and add 1
        # This shouldn't happen in normal circumstances, but we handle it just in case
        all_user_tasks = get_tasks_with_serial(session, user_id)
        if all_user_tasks:
            # Sort by serial number and get the highest one
            highest_serial = max(t['serial_number'] for t in all_user_tasks)
            toggled_task_serial = highest_serial + 1
        else:
            # If no tasks exist, this should be serial number 1
            toggled_task_serial = 1

    # Format the created_at datetime
    created_at_dt = task.created_at
    if isinstance(created_at_dt, str):
        from datetime import datetime
        created_at_dt = datetime.fromisoformat(created_at_dt.replace('Z', '+00:00'))

    return TaskResponse(
        serial_number=toggled_task_serial,
        id=str(toggled_task_serial),  # Use serial number as id for frontend compatibility
        title=task.title,
        description=task.description,
        completed=task.completed,
        created_at=created_at_dt,
        created_at_formatted=created_at_dt.strftime("%Y-%m-%d %H:%M")
    )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_endpoint(
    task_id: str,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> None:
    """
    Delete a task.

    Args:
        task_id: Task UUID
        current_user: Authenticated user
        session: Database session

    Returns:
        None (204 No Content)

    Raises:
        HTTPException: 404 if task not found
        HTTPException: 403 if task belongs to different user
    """
    user_id = current_user.id

    # Check if task_id is a serial number (integer) or UUID
    actual_task_id = None

    # Try to interpret as serial number if it's numeric
    if task_id.isdigit():
        serial_num = int(task_id)
        actual_task_id = resolve_serial_number_to_uuid(session, user_id, serial_num)

        if not actual_task_id:
            raise HTTPException(
                status_code=404,
                detail=f"Task with serial number {serial_num} not found"
            )
    else:
        # It's a UUID, verify it exists for this user
        task_check = get_task_by_id(session, task_id, user_id)
        if not task_check:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )
        actual_task_id = task_id

    deleted = delete_task(session, actual_task_id, user_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return None


@router.delete("/by-serial/{serial_number}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_by_serial_endpoint(
    serial_number: int,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> None:
    """
    Delete a task by serial number.

    Args:
        serial_number: Task serial number
        current_user: Authenticated user
        session: Database session

    Returns:
        None (204 No Content)

    Raises:
        HTTPException: 404 if task not found
        HTTPException: 403 if task belongs to different user
    """
    user_id = current_user.id

    # First get the task by serial number to get its UUID
    task_with_serial = get_task_by_serial(session, user_id, serial_number)

    if not task_with_serial:
        raise HTTPException(
            status_code=404,
            detail=f"Task with serial number {serial_number} not found"
        )

    # Now delete using the actual task ID
    deleted = delete_task(session, task_with_serial['id'], user_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Task with serial number {serial_number} not found"
        )

    return None
