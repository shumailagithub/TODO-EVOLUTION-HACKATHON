"""
Task CRUD database operations.
Enforces user ownership for all task operations.
"""
from typing import Optional
from datetime import datetime
from sqlmodel import Session, select, delete
from models.task import Task


def create_task(
    session: Session,
    user_id: str,
    title: str,
    description: Optional[str] = None
) -> Task:
    """
    Create a new task for user.

    Args:
        session: Database session
        user_id: User ID (for ownership)
        title: Task title
        description: Optional task description

    Returns:
        Created Task object
    """
    task = Task(user_id=user_id, title=title, description=description)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def get_tasks(
    session: Session,
    user_id: str,
    completed: Optional[bool] = None
) -> list[Task]:
    """
    Get all tasks for a user, optionally filtered by completion status.

    Args:
        session: Database session
        user_id: User ID (CRITICAL for data isolation)
        completed: Optional filter for completion status

    Returns:
        List of tasks for the user
    """
    query = select(Task).where(Task.user_id == user_id)

    # Apply completion filter if provided
    if completed is not None:
        query = query.where(Task.completed == completed)

    results = session.exec(query)
    return list(results.all())


def get_task_by_id(
    session: Session,
    task_id: str,
    user_id: str
) -> Optional[Task]:
    """
    Get a specific task by ID, enforcing user ownership.

    Args:
        session: Database session
        task_id: Task ID
        user_id: User ID (CRITICAL for data isolation)

    Returns:
        Task if found and belongs to user, None otherwise
    """
    task = session.exec(
        select(Task)
        .where(Task.id == task_id)
        .where(Task.user_id == user_id)
    ).first()
    return task


def update_task(
    session: Session,
    task_id: str,
    user_id: str,
    data: dict
) -> Optional[Task]:
    """
    Update a task, enforcing user ownership.

    Args:
        session: Database session
        task_id: Task ID
        user_id: User ID (CRITICAL for data isolation)
        data: Dictionary of fields to update

    Returns:
        Updated Task if found, None otherwise
    """
    task = get_task_by_id(session, task_id, user_id)

    if not task:
        return None

    # Update provided fields
    for key, value in data.items():
        if hasattr(task, key):
            setattr(task, key, value)

    task.updated_at = datetime.utcnow()
    session.commit()
    session.refresh(task)
    return task


def toggle_task(
    session: Session,
    task_id: str,
    user_id: str
) -> Optional[Task]:
    """
    Toggle task completion status, enforcing user ownership.

    Args:
        session: Database session
        task_id: Task ID
        user_id: User ID (CRITICAL for data isolation)

    Returns:
        Updated Task if found, None otherwise
    """
    task = get_task_by_id(session, task_id, user_id)

    if not task:
        return None

    task.completed = not task.completed
    task.updated_at = datetime.utcnow()
    session.commit()
    session.refresh(task)
    return task


def delete_task(
    session: Session,
    task_id: str,
    user_id: str
) -> bool:
    """
    Delete a task, enforcing user ownership.

    Args:
        session: Database session
        task_id: Task ID
        user_id: User ID (CRITICAL for data isolation)

    Returns:
        True if deleted, False if not found or wrong user
    """
    task = get_task_by_id(session, task_id, user_id)

    if not task:
        return False

    session.delete(task)
    session.commit()
    return True
