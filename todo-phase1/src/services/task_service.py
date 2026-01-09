"""Business logic service for in-memory todo management."""

from typing import Dict, List, Optional

from src.models.task import Task, TaskStatus, ValidationError


class TaskService:
    """Service managing in-memory task storage and operations.

    Tasks are stored in a dictionary keyed by task ID for O(1) lookups.
    All data is lost when application exits (in-memory only).

    Attributes:
        _tasks: Dictionary mapping task IDs (integers) to Task objects
        _next_id: Counter for next available task ID
    """

    def __init__(self) -> None:
        """Initialize TaskService with empty in-memory storage.

        Storage starts empty. First task will get ID 1.
        """
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add_task(self, title: str) -> Task:
        """Add a new task with the given title.

        Task is created with unique sequential ID and PENDING status.

        Args:
            title: Human-readable task description (1-200 chars, non-empty)

        Returns:
            Newly created Task object

        Raises:
            ValidationError: If title is invalid (checked by Task.__post_init__)
        """
        task = Task(id=self._next_id, title=title, status=TaskStatus.PENDING)
        self._tasks[task.id] = task
        self._next_id += 1
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """Retrieve a task by ID.

        Args:
            task_id: Unique identifier of the task

        Returns:
            Task if found, None otherwise
        """
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks sorted by ID in ascending order.

        Returns:
            List of all tasks, sorted by ID
        """
        return sorted(self._tasks.values(), key=lambda t: t.id)

    def update_task(self, task_id: int, new_title: str) -> Task:
        """Update an existing task's title.

        Creates a new Task object with updated title, replacing the old one.

        Args:
            task_id: Unique identifier of the task
            new_title: New title for the task (1-200 chars, non-empty)

        Returns:
            Updated Task object

        Raises:
            ValueError: If task with given ID doesn't exist
            ValidationError: If new title is invalid
        """
        if task_id not in self._tasks:
            raise ValueError(f"Error: Task with ID {task_id} not found.")

        old_task = self._tasks[task_id]
        updated_task = Task(
            id=task_id, title=new_title, status=old_task.status
        )
        self._tasks[task_id] = updated_task
        return updated_task

    def set_task_status(
        self, task_id: int, new_status: TaskStatus
    ) -> Task:
        """Update a task's status.

        Creates a new Task object with updated status, replacing the old one.

        Args:
            task_id: Unique identifier of the task
            new_status: New status value from TaskStatus enum

        Returns:
            Updated Task object

        Raises:
            ValueError: If task with given ID doesn't exist
            ValidationError: If new status is invalid
        """
        if task_id not in self._tasks:
            raise ValueError(f"Error: Task with ID {task_id} not found.")

        old_task = self._tasks[task_id]
        updated_task = Task(
            id=task_id, title=old_task.title, status=new_status
        )
        self._tasks[task_id] = updated_task
        return updated_task

    def delete_task(self, task_id: int) -> None:
        """Delete a task from storage.

        Args:
            task_id: Unique identifier of the task to delete

        Raises:
            ValueError: If task with given ID doesn't exist
        """
        if task_id not in self._tasks:
            raise ValueError(f"Error: Task with ID {task_id} not found.")

        del self._tasks[task_id]

    def task_count(self) -> int:
        """Return total number of tasks in storage.

        Returns:
            Number of tasks currently stored
        """
        return len(self._tasks)
