"""Task model and validation for in-memory todo application."""

from dataclasses import dataclass, field
from enum import Enum
from typing import final


class TaskStatus(Enum):
    """Enum for task status values.

    Defines three valid states for a task lifecycle:
    - pending: Task not yet started
    - in_progress: Task currently being worked on
    - completed: Task has been finished
    """

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class ValidationError(Exception):
    """Custom exception for validation errors.

    Raised when task attributes fail validation checks.
    Provides a clear, user-friendly error message.
    """

    def __init__(self, message: str) -> None:
        """Initialize ValidationError with message.

        Args:
            message: Human-readable error description
        """
        super().__init__(message)
        self.message = message


@final
@dataclass(frozen=True)
class Task:
    """Represents a single todo item.

    Task is immutable - once created, its attributes cannot change directly.
    To modify a task, create a new Task with updated values.

    Attributes:
        id: Unique integer identifier (sequential, auto-incrementing)
        title: Human-readable task description (1-200 characters, non-empty)
        status: Current state of the task (defaults to PENDING)
    """

    id: int
    title: str
    status: TaskStatus = field(default=TaskStatus.PENDING)

    def __post_init__(self) -> None:
        """Validate task attributes after initialization.

        Raises:
            ValidationError: If title or status is invalid
        """
        self._validate_title(self.title)
        self._validate_status(self.status)

    @staticmethod
    def _validate_title(title: str) -> None:
        """Validate title meets constraints.

        Args:
            title: Task title to validate

        Raises:
            ValidationError: If title is empty, only whitespace, or exceeds 200 characters
        """
        if not title:
            raise ValidationError("Error: Task title cannot be empty.")

        if title.strip() == "":
            raise ValidationError("Error: Task title cannot be only whitespace.")

        if len(title) < 1 or len(title) > 200:
            raise ValidationError(
                "Error: Task title must be between 1 and 200 characters."
            )

    @staticmethod
    def _validate_status(status: TaskStatus) -> None:
        """Validate status is a valid TaskStatus enum value.

        Args:
            status: TaskStatus to validate

        Raises:
            ValidationError: If status is not a valid TaskStatus
        """
        if status not in TaskStatus:
            raise ValidationError(
                f"Error: Invalid task status. Must be one of: "
                f"{', '.join([s.value for s in TaskStatus])}"
            )

    def __repr__(self) -> str:
        """Return string representation showing id, title, and status.

        Returns:
            String in format: Task(id=..., title=..., status=...)
        """
        return f"Task(id={self.id}, title={self.title}, status={self.status.value})"

    def __str__(self) -> str:
        """Return string representation for display.

        Format: [status] title
        Example: [P] Buy groceries
        """
        status_map = {
            TaskStatus.PENDING: "[P]",
            TaskStatus.IN_PROGRESS: "[IP]",
            TaskStatus.COMPLETED: "[C]",
        }
        return f"{status_map[self.status]} {self.title}"
