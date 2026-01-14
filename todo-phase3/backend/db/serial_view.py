"""
Database view for serial number generation.

This module defines the tasks_with_serial view that provides sequential
serial numbers for tasks using ROW_NUMBER() function.
"""
from sqlmodel import Session, select, text
from models.task import Task
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

def create_tasks_with_serial_view(session: Session) -> bool:
    """
    Create the tasks_with_serial view that generates sequential serial numbers
    for tasks using ROW_NUMBER() function.

    Args:
        session: Database session

    Returns:
        True if view was created successfully, False otherwise
    """
    try:
        # Drop view if it exists (to handle updates)
        drop_view_sql = """
        DROP VIEW IF EXISTS tasks_with_serial;
        """
        session.exec(text(drop_view_sql))
        session.commit()

        # Create the view that assigns serial numbers using ROW_NUMBER()
        create_view_sql = """
        CREATE VIEW tasks_with_serial AS
        SELECT
            ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at) AS serial_number,
            id,
            user_id,
            title,
            description,
            completed,
            created_at,
            updated_at
        FROM tasks
        ORDER BY user_id, created_at;
        """
        session.exec(text(create_view_sql))
        session.commit()

        logger.info("Successfully created tasks_with_serial view")
        return True
    except Exception as e:
        logger.error(f"Error creating tasks_with_serial view: {str(e)}")
        session.rollback()
        return False


def verify_tasks_with_serial_view(session: Session) -> bool:
    """
    Verify that the tasks_with_serial view exists and functions correctly.

    Args:
        session: Database session

    Returns:
        True if view exists and works correctly, False otherwise
    """
    try:
        # Test query to verify the view works
        test_query = """
        SELECT serial_number, id, user_id, title, completed
        FROM tasks_with_serial
        LIMIT 1;
        """
        result = session.exec(text(test_query))
        # Try to fetch one row to verify the view works
        rows = result.fetchall()

        # The query should execute without error
        # Even if no tasks exist, the view structure should be valid
        return True
    except Exception as e:
        logger.error(f"Error verifying tasks_with_serial view: {str(e)}")
        return False


def get_tasks_with_serial(session: Session, user_id: str) -> List[dict]:
    """
    Get all tasks for a user with their serial numbers from the view.

    Args:
        session: Database session
        user_id: User ID to get tasks for

    Returns:
        List of tasks with serial numbers
    """
    # Use SQLAlchemy core with the session's connection
    from sqlalchemy import text
    # Execute the raw SQL using the session's connection
    result_proxy = session.exec(text("""
        SELECT
            serial_number,
            id,
            title,
            description,
            completed,
            created_at,
            updated_at
        FROM tasks_with_serial
        WHERE user_id = :user_id
        ORDER BY serial_number;
    """), params={"user_id": user_id})

    # Since we can't use params directly with session.exec for raw SQL, let's do it differently
    # We'll execute the raw query using the underlying connection
    from sqlalchemy import create_engine, text as sa_text
    from db.connection import engine

    with engine.connect() as conn:
        # Execute with autocommit for read-only queries
        result = conn.execute(sa_text("""
            SELECT
                serial_number,
                id,
                title,
                description,
                completed,
                created_at,
                updated_at
            FROM tasks_with_serial
            WHERE user_id = :user_id
            ORDER BY serial_number;
        """), {"user_id": user_id})

        # Convert Row objects to dictionaries
        rows = result.fetchall()
        return [{key: value for key, value in row._mapping.items()} for row in rows]


def get_task_by_serial(session: Session, user_id: str, serial_number: int) -> Optional[dict]:
    """
    Get a specific task by its serial number for a user.

    Args:
        session: Database session
        user_id: User ID
        serial_number: Serial number of the task

    Returns:
        Task dictionary if found, None otherwise
    """
    from sqlalchemy import text as sa_text
    from db.connection import engine

    with engine.connect() as conn:
        result = conn.execute(sa_text("""
            SELECT
                serial_number,
                id,
                title,
                description,
                completed,
                created_at,
                updated_at
            FROM tasks_with_serial
            WHERE user_id = :user_id AND serial_number = :serial_number;
        """), {"user_id": user_id, "serial_number": serial_number})
        row = result.first()
        return {key: value for key, value in row._mapping.items()} if row else None