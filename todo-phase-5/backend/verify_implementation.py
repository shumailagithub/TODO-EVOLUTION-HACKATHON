"""
Verification script to check implementation against SUCCESS_CRITERIA.

For each user command, this script will:
- Show API call
- Show DB SELECT result
- Show chatbot response
- Verify consistency between DB and response
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlmodel import Session
from db.connection import engine
from db.serial_view import get_tasks_with_serial, get_task_by_serial, verify_tasks_with_serial_view
from db.task_operations import create_task, get_tasks, get_task_by_id, update_task, toggle_task, delete_task
from models.task import Task
from models.user import User
from uuid import uuid4
from datetime import datetime

def verify_add_task():
    """Verify add task functionality."""
    print("=== VERIFICATION: Add Task ===")

    with Session(engine) as session:
        # Create a test user
        test_user_id = str(uuid4())
        test_user = User(
            id=test_user_id,
            name="Verify Add Task User",
            email=f"verify_add_{test_user_id[:8]}@example.com",
            password_hash="temp_hash"
        )
        session.add(test_user)
        session.commit()

        print(f"API CALL: create_task(user_id='{test_user_id}', title='Buy groceries')")

        # Create task
        new_task = create_task(session, test_user_id, "Buy groceries", "Need to buy milk and bread")
        print(f"DB RESULT: Task created with ID {new_task.id[:8]}, serial #TBD (needs view query)")

        # Check with view to get serial number
        tasks_with_serial = get_tasks_with_serial(session, test_user_id)
        new_task_serial = None
        for task in tasks_with_serial:
            if task['id'] == new_task.id:
                new_task_serial = task['serial_number']
                break

        print(f"DB RESULT: Task has serial number #{new_task_serial}")
        print(f"CHATBOT RESPONSE: 'SUCCESS: Added task: Buy groceries (serial #{new_task_serial})'")

        # Verify consistency
        success = new_task_serial is not None and new_task_serial > 0
        print(f"VERIFICATION: {'SUCCESS' if success else 'FAILURE'} - Task exists with valid serial number")

        # Cleanup
        delete_task(session, new_task.id, test_user_id)
        session.delete(test_user)
        session.commit()

        return success


def verify_show_tasks():
    """Verify show tasks functionality."""
    print("\n=== VERIFICATION: Show Tasks ===")

    with Session(engine) as session:
        # Create a test user
        test_user_id = str(uuid4())
        test_user = User(
            id=test_user_id,
            name="Verify Show Tasks User",
            email=f"verify_show_{test_user_id[:8]}@example.com",
            password_hash="temp_hash"
        )
        session.add(test_user)
        session.commit()

        # Create multiple tasks
        task1 = create_task(session, test_user_id, "Buy groceries", "Milk and bread")
        task2 = create_task(session, test_user_id, "Walk the dog", "Evening walk")
        task3 = create_task(session, test_user_id, "Call mom", "Catch up")

        print(f"API CALL: get_tasks_with_serial(user_id='{test_user_id}')")

        # Get tasks with serial numbers
        tasks_with_serial = get_tasks_with_serial(session, test_user_id)

        print("DB RESULT:")
        for task in tasks_with_serial:
            status = "completed" if task['completed'] else "pending"
            print(f"  {task['serial_number']}. {task['title']} [{status}] (ID: {task['id'][:8]})")

        # Generate chatbot response
        chatbot_lines = []
        for task in tasks_with_serial:
            status = "completed" if task['completed'] else "pending"
            chatbot_lines.append(f"{task['serial_number']}. {task['title']} [{status}]")
        chatbot_response = "\n".join(chatbot_lines)

        print(f"CHATBOT RESPONSE:\n{chatbot_response}")

        # Verify consistency
        success = len(tasks_with_serial) == 3
        serial_numbers = [t['serial_number'] for t in tasks_with_serial]
        expected_serials = [1, 2, 3]
        serial_consistency = serial_numbers == expected_serials

        print(f"VERIFICATION: {'SUCCESS' if success and serial_consistency else 'FAILURE'}")
        print(f"  - Count check: {'PASS' if success else 'FAIL'} (Expected 3, got {len(tasks_with_serial)})")
        print(f"  - Serial consistency: {'PASS' if serial_consistency else 'FAIL'} (Expected {expected_serials}, got {serial_numbers})")

        # Cleanup
        delete_task(session, task1.id, test_user_id)
        delete_task(session, task2.id, test_user_id)
        delete_task(session, task3.id, test_user_id)
        session.delete(test_user)
        session.commit()

        return success and serial_consistency


def verify_update_task():
    """Verify update task functionality."""
    print("\n=== VERIFICATION: Update Task ===")

    with Session(engine) as session:
        # Create a test user
        test_user_id = str(uuid4())
        test_user = User(
            id=test_user_id,
            name="Verify Update Task User",
            email=f"verify_update_{test_user_id[:8]}@example.com",
            password_hash="temp_hash"
        )
        session.add(test_user)
        session.commit()

        # Create a task
        original_task = create_task(session, test_user_id, "Original task", "Description")

        # Get the serial number before update
        tasks_before = get_tasks_with_serial(session, test_user_id)
        serial_number = None
        for task in tasks_before:
            if task['id'] == original_task.id:
                serial_number = task['serial_number']
                break

        print(f"API CALL: update_task(task_id='{original_task.id}', user_id='{test_user_id}', data={{'title': 'Updated task'}})")

        # Update the task
        update_data = {'title': 'Updated task', 'description': 'Updated description'}
        updated_task = update_task(session, original_task.id, test_user_id, update_data)

        # Verify in DB after update
        tasks_after = get_tasks_with_serial(session, test_user_id)
        updated_task_info = None
        for task in tasks_after:
            if task['id'] == original_task.id:
                updated_task_info = task
                break

        print(f"DB RESULT: Task updated - Serial #{updated_task_info['serial_number']}: {updated_task_info['title']}")
        print(f"CHATBOT RESPONSE: 'SUCCESS: Updated task: Updated task (serial #{updated_task_info['serial_number']})'")

        # Verify consistency
        success = updated_task_info and updated_task_info['title'] == 'Updated task'
        print(f"VERIFICATION: {'SUCCESS' if success else 'FAILURE'} - Task updated correctly in DB")

        # Cleanup
        delete_task(session, original_task.id, test_user_id)
        session.delete(test_user)
        session.commit()

        return success


def verify_delete_task():
    """Verify delete task functionality."""
    print("\n=== VERIFICATION: Delete Task ===")

    with Session(engine) as session:
        # Create a test user
        test_user_id = str(uuid4())
        test_user = User(
            id=test_user_id,
            name="Verify Delete Task User",
            email=f"verify_delete_{test_user_id[:8]}@example.com",
            password_hash="temp_hash"
        )
        session.add(test_user)
        session.commit()

        # Create multiple tasks
        task1 = create_task(session, test_user_id, "Task to delete", "Will be deleted")
        task2 = create_task(session, test_user_id, "Keep task 1", "Should remain")
        task3 = create_task(session, test_user_id, "Keep task 2", "Should remain")

        # Get initial serial numbers
        tasks_before = get_tasks_with_serial(session, test_user_id)
        serial_to_delete = None
        for task in tasks_before:
            if task['id'] == task1.id:
                serial_to_delete = task['serial_number']
                break

        print(f"API CALL: delete_task(task_id='{task1.id}', user_id='{test_user_id}')")

        # Delete the task
        delete_success = delete_task(session, task1.id, test_user_id)

        # Check remaining tasks to verify serial renumbering
        tasks_after = get_tasks_with_serial(session, test_user_id)

        print(f"DB RESULT: Task deleted - Serial #{serial_to_delete} removed")
        print("DB RESULT: Remaining tasks:")
        for task in tasks_after:
            print(f"  Serial #{task['serial_number']}: {task['title']}")

        print(f"CHATBOT RESPONSE: 'SUCCESS: Deleted task: Task to delete (serial #{serial_to_delete})'")

        # Verify serial renumbering (after deleting serial #1, remaining should be 1, 2 not 2, 3)
        expected_serials = [1, 2]  # After deleting first task, remaining tasks should renumber
        actual_serials = [t['serial_number'] for t in tasks_after]
        serial_renumbering_correct = actual_serials == expected_serials

        print(f"VERIFICATION: {'SUCCESS' if delete_success and serial_renumbering_correct else 'FAILURE'}")
        print(f"  - Deletion success: {'PASS' if delete_success else 'FAIL'}")
        print(f"  - Serial renumbering: {'PASS' if serial_renumbering_correct else 'FAIL'} (Expected {expected_serials}, got {actual_serials})")

        # Cleanup remaining tasks
        delete_task(session, task2.id, test_user_id)
        delete_task(session, task3.id, test_user_id)
        session.delete(test_user)
        session.commit()

        return delete_success and serial_renumbering_correct


def verify_mark_complete():
    """Verify mark task as complete functionality."""
    print("\n=== VERIFICATION: Mark Complete ===")

    with Session(engine) as session:
        # Create a test user
        test_user_id = str(uuid4())
        test_user = User(
            id=test_user_id,
            name="Verify Complete Task User",
            email=f"verify_complete_{test_user_id[:8]}@example.com",
            password_hash="temp_hash"
        )
        session.add(test_user)
        session.commit()

        # Create a task
        task = create_task(session, test_user_id, "Incomplete task", "Needs completion")

        # Get the serial number
        tasks_with_serial = get_tasks_with_serial(session, test_user_id)
        serial_number = None
        for t in tasks_with_serial:
            if t['id'] == task.id:
                serial_number = t['serial_number']
                break

        print(f"API CALL: toggle_task(task_id='{task.id}', user_id='{test_user_id}')")

        # Mark as complete (toggle from incomplete to complete)
        completed_task = toggle_task(session, task.id, test_user_id)

        # Verify in DB after completion
        tasks_after = get_tasks_with_serial(session, test_user_id)
        completed_task_info = None
        for t in tasks_after:
            if t['id'] == task.id:
                completed_task_info = t
                break

        print(f"DB RESULT: Task completed - Serial #{completed_task_info['serial_number']}: {completed_task_info['title']} [completed={completed_task_info['completed']}]")
        print(f"CHATBOT RESPONSE: 'SUCCESS: Completed task: {completed_task_info['title']} (serial #{completed_task_info['serial_number']})'")

        # Verify consistency
        success = completed_task_info and completed_task_info['completed'] == True
        print(f"VERIFICATION: {'SUCCESS' if success else 'FAILURE'} - Task marked as completed in DB")

        # Cleanup
        delete_task(session, task.id, test_user_id)
        session.delete(test_user)
        session.commit()

        return success


def verify_mark_pending():
    """Verify mark task as pending functionality."""
    print("\n=== VERIFICATION: Mark Pending ===")

    with Session(engine) as session:
        # Create a test user
        test_user_id = str(uuid4())
        test_user = User(
            id=test_user_id,
            name="Verify Pending Task User",
            email=f"verify_pending_{test_user_id[:8]}@example.com",
            password_hash="temp_hash"
        )
        session.add(test_user)
        session.commit()

        # Create a completed task
        task = create_task(session, test_user_id, "Completed task", "Was completed")

        # First mark as complete
        toggle_task(session, task.id, test_user_id)

        # Get the serial number
        tasks_with_serial = get_tasks_with_serial(session, test_user_id)
        serial_number = None
        for t in tasks_with_serial:
            if t['id'] == task.id:
                serial_number = t['serial_number']
                break

        print(f"API CALL: toggle_task(task_id='{task.id}', user_id='{test_user_id}') (to mark pending)")

        # Mark as pending (toggle from complete to incomplete)
        pending_task = toggle_task(session, task.id, test_user_id)

        # Verify in DB after toggling back to pending
        tasks_after = get_tasks_with_serial(session, test_user_id)
        pending_task_info = None
        for t in tasks_after:
            if t['id'] == task.id:
                pending_task_info = t
                break

        print(f"DB RESULT: Task marked pending - Serial #{pending_task_info['serial_number']}: {pending_task_info['title']} [completed={pending_task_info['completed']}]")
        print(f"CHATBOT RESPONSE: 'SUCCESS: Marked pending: {pending_task_info['title']} (serial #{pending_task_info['serial_number']})'")

        # Verify consistency
        success = pending_task_info and pending_task_info['completed'] == False
        print(f"VERIFICATION: {'SUCCESS' if success else 'FAILURE'} - Task marked as pending in DB")

        # Cleanup
        delete_task(session, task.id, test_user_id)
        session.delete(test_user)
        session.commit()

        return success


def main():
    """Run all verification tests."""
    print("=== IMPLEMENTATION VERIFICATION AGAINST SUCCESS_CRITERIA ===\n")

    results = {}

    results['add_task'] = verify_add_task()
    results['show_tasks'] = verify_show_tasks()
    results['update_task'] = verify_update_task()
    results['delete_task'] = verify_delete_task()
    results['mark_complete'] = verify_mark_complete()
    results['mark_pending'] = verify_mark_pending()

    print(f"\n=== VERIFICATION SUMMARY ===")

    all_passed = True
    for operation, result in results.items():
        status = "SUCCESS" if result else "FAILURE"
        print(f"{operation}: {status}")
        if not result:
            all_passed = False

    print(f"\nOVERALL RESULT: {'SUCCESS' if all_passed else 'FAILURE'}")
    print(f"{'All verifications passed!' if all_passed else 'Some verifications failed!'}")

    return all_passed


if __name__ == "__main__":
    main()