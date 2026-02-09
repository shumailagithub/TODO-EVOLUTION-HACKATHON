"""
Task API endpoints.
Handles task CRUD operations with user ownership enforcement.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
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


# Request/Response Models
class CreateTaskRequest(BaseModel):
    """Request model for creating a task."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)


class UpdateTaskRequest(BaseModel):
    """Request model for updating a task."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = None


class TaskResponse(BaseModel):
    """Response model with task data."""
    task: dict


class TasksResponse(BaseModel):
    """Response model with tasks list."""
    tasks: list[dict]
    count: int


# API Router
router = APIRouter(prefix="/api/tasks", tags=["Tasks"])


@router.get("", response_model=TasksResponse)
async def get_all_tasks(
    completed: Optional[bool] = None,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> TasksResponse:
    """
    Get all tasks for authenticated user.

    Args:
        completed: Optional filter for completion status
        current_user: Authenticated user
        session: Database session

    Returns:
        List of tasks for user
    """
    user_id = current_user.id

    tasks = get_tasks(session, user_id, completed)

    return TasksResponse(
        tasks=[task.dict() for task in tasks],
        count=len(tasks)
    )


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: str,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """
    Get a specific task by ID.

    Args:
        task_id: Task UUID
        current_user: Authenticated user
        session: Database session

    Returns:
        Task data if found and belongs to user

    Raises:
        HTTPException: 404 if task not found
        HTTPException: 403 if task belongs to different user
    """
    user_id = current_user.id

    task = get_task_by_id(session, task_id, user_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return TaskResponse(task=task.dict())


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

    return TaskResponse(task=task.dict())


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

    task = update_task(session, task_id, user_id, update_data)

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return TaskResponse(task=task.dict())


@router.patch("/{task_id}/toggle", response_model=TaskResponse)
async def toggle_task_endpoint(
    task_id: str,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """
    Toggle task completion status.

    Args:
        task_id: Task UUID
        current_user: Authenticated user
        session: Database session

    Returns:
        Updated task

    Raises:
        HTTPException: 404 if task not found
        HTTPException: 403 if task belongs to different user
    """
    user_id = current_user.id

    task = toggle_task(session, task_id, user_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return TaskResponse(task=task.dict())


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

    deleted = delete_task(session, task_id, user_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return None
