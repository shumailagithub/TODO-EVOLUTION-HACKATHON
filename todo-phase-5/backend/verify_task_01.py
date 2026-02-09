"""
Verification script for TASK-01: Verify Database Schema & Views

This script tests that:
1. The tasks_with_serial view exists and functions correctly
2. Serial numbers are generated sequentially using ROW_NUMBER()
3. Serial numbers renumber automatically after deletions
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlmodel import Session
from db.connection import engine
from db.serial_view import verify_tasks_with_serial_view, get_tasks_with_serial, get_task_by_serial
from db.task_operations import create_task, get_tasks, delete_task
from models.task import Task
from models.user import User
from uuid import uuid4
from datetime import datetime

def test_serial_view_creation():
    """Test that the tasks_with_serial view was created and functions correctly."""
    print("=== TASK-01: Testing Database Schema & Views ===")

    with Session(engine) as session:
        # Verify the view exists and works
        print("1. Verifying tasks_with_serial view...")
        view_exists = verify_tasks_with_serial_view(session)
        if view_exists:
            print("   [PASS] View exists and is accessible")
        else:
            print("   [FAIL] View verification failed")
            return False

    return True


def test_serial_number_generation():
    """Test that serial numbers are generated correctly."""
    print("\n2. Testing serial number generation...")

    with Session(engine) as session:
        # Create a test user first
        test_user_id = str(uuid4())
        test_user = User(
            id=test_user_id,
            name="Test User",  # Changed from full_name to name
            email=f"test_{test_user_id[:8]}@example.com",
            password_hash="test_password_hash"  # Changed from hashed_password to password_hash
        )
        session.add(test_user)
        session.commit()
        session.refresh(test_user)

        print(f"   Created test user: {test_user.email}")

        # Create test tasks
        print(f"   Creating test tasks for user: {test_user_id[:8]}...")

        task1 = create_task(session, test_user_id, "First task", "Description for first task")
        task2 = create_task(session, test_user_id, "Second task", "Description for second task")
        task3 = create_task(session, test_user_id, "Third task", "Description for third task")

        print(f"   Created tasks: {task1.id[:8]}, {task2.id[:8]}, {task3.id[:8]}")

        # Get tasks using the serial view
        tasks_with_serial = get_tasks_with_serial(session, test_user_id)

        print(f"   Retrieved {len(tasks_with_serial)} tasks with serial numbers:")
        for task in tasks_with_serial:
            print(f"     Serial #{task['serial_number']}: {task['title']} (ID: {task['id'][:8]})")

        # Verify serial numbers are sequential (1, 2, 3)
        expected_serials = [1, 2, 3]
        actual_serials = [task['serial_number'] for task in tasks_with_serial]

        if actual_serials == expected_serials:
            print("   [PASS] Serial numbers are correctly sequential (1, 2, 3)")
        else:
            print(f"   [FAIL] Expected {expected_serials}, got {actual_serials}")
            return False

        # Test getting a specific task by serial number
        task_by_serial = get_task_by_serial(session, test_user_id, 2)
        if task_by_serial and task_by_serial['serial_number'] == 2:
            print(f"   [PASS] Can retrieve task by serial number (Serial #2: {task_by_serial['title']})")
        else:
            print("   [FAIL] Failed to retrieve task by serial number")
            return False

        # Clean up: delete test tasks
        delete_task(session, task1.id, test_user_id)
        delete_task(session, task2.id, test_user_id)
        delete_task(session, task3.id, test_user_id)

        # Delete the test user
        session.delete(test_user)
        session.commit()

        print("   [PASS] Test tasks and user cleaned up")

    return True


def test_serial_renumbering_after_delete():
    """Test that serial numbers renumber automatically after deletions."""
    print("\n3. Testing serial renumbering after deletion...")

    with Session(engine) as session:
        # Create a test user first
        test_user_id = str(uuid4())
        test_user = User(
            id=test_user_id,
            email=f"test_{test_user_id[:8]}@example.com",
            full_name="Test User 2",
            hashed_password="test_password_hash",  # This is just for testing
            email_verified=True
        )
        session.add(test_user)
        session.commit()
        session.refresh(test_user)

        print(f"   Created test user: {test_user.email}")

        # Create test tasks
        print(f"   Creating test tasks for user: {test_user_id[:8]}...")

        task1 = create_task(session, test_user_id, "First task", "Description for first task")
        task2 = create_task(session, test_user_id, "Second task", "Description for second task")
        task3 = create_task(session, test_user_id, "Third task", "Description for third task")

        print("   Initial state: 3 tasks (serials 1, 2, 3)")

        # Verify initial serial numbers
        tasks_before = get_tasks_with_serial(session, test_user_id)
        initial_serials = [t['serial_number'] for t in tasks_before]
        print(f"   Serial numbers before deletion: {initial_serials}")

        # Delete the middle task (serial #2)
        print("   Deleting task with serial #2...")
        delete_success = delete_task(session, task2.id, test_user_id)

        if delete_success:
            print("   [PASS] Task deletion successful")
        else:
            print("   [FAIL] Task deletion failed")
            return False

        # Check serial numbers after deletion
        tasks_after = get_tasks_with_serial(session, test_user_id)
        final_serials = [t['serial_number'] for t in tasks_after]
        print(f"   Serial numbers after deletion: {final_serials}")

        # After deleting serial #2, remaining tasks should be renumbered to 1, 2 (not 1, 3)
        expected_final_serials = [1, 2]
        if final_serials == expected_final_serials:
            print("   [PASS] Serial numbers correctly renumbered after deletion (1, 2, not 1, 3)")
        else:
            print(f"   [FAIL] Expected {expected_final_serials}, got {final_serials}")
            return False

        # Clean up remaining tasks
        delete_task(session, task1.id, test_user_id)
        delete_task(session, task3.id, test_user_id)

        # Delete the test user
        session.delete(test_user)
        session.commit()

        print("   [PASS] Remaining test tasks and user cleaned up")

    return True


def main():
    """Run all verification tests for TASK-01."""
    print("Starting TASK-01 verification...\n")

    success = True

    # Test 1: View creation
    success &= test_serial_view_creation()

    # Test 2: Serial number generation
    success &= test_serial_number_generation()

    # Test 3: Serial renumbering after deletion
    success &= test_serial_renumbering_after_delete()

    print(f"\n=== TASK-01 VERIFICATION {'PASSED' if success else 'FAILED'} ===")

    if success:
        print("[PASS] All database schema and view verification tests passed")
        print("[PASS] tasks_with_serial view exists and functions correctly")
        print("[PASS] Serial numbers are generated sequentially using ROW_NUMBER()")
        print("[PASS] Serial numbers renumber automatically after deletions")
    else:
        print("[FAIL] Some verification tests failed")

    return success


if __name__ == "__main__":
    main()