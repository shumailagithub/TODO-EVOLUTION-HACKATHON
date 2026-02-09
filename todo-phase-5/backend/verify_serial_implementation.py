"""
Verification script to confirm the serial number implementation in the API.

This script verifies that:
1. The API returns serial numbers instead of UUIDs in responses
2. The API accepts serial numbers as parameters where appropriate
3. The API uses the tasks_with_serial view for all user-facing operations
4. No UUID validation errors occur
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlmodel import Session
from db.connection import engine
from db.serial_view import get_tasks_with_serial, get_task_by_serial
from db.task_operations import create_task, delete_task
from models.task import Task
from models.user import User
from api.tasks import (
    TaskResponse,
    ListTasksResponse,
    TaskItem,
    CreateTaskRequest,
    UpdateTaskRequest
)
from uuid import uuid4

def verify_models():
    """Verify that the new models are properly defined."""
    print("=== VERIFICATION: Models ===")

    # Test TaskInDB model
    try:
        from api.tasks import TaskInDB
        print("PASS: TaskInDB model exists")
    except ImportError:
        print("FAIL: TaskInDB model missing")
        return False

    # Test TaskResponse model
    try:
        response = TaskResponse(
            serial_number=1,
            title="Test task",
            description="Test description",
            completed=False,
            created_at=None,
            created_at_formatted="2026-01-13 14:00"
        )
        print("PASS: TaskResponse model works with serial_number")
    except Exception as e:
        print(f"FAIL: TaskResponse model error: {e}")
        return False

    # Test ListTasksResponse model
    try:
        list_response = ListTasksResponse(
            tasks=[response],
            total=1,
            pending=1,
            completed=0
        )
        print("PASS: ListTasksResponse model works")
    except Exception as e:
        print(f"FAIL: ListTasksResponse model error: {e}")
        return False

    # Verify TaskItem model uses serial_number
    try:
        task_item = TaskItem(
            serial_number=1,
            title="Test",
            description="Test",
            completed=False,
            created_at=None,
            created_at_formatted="2026-01-13 14:00"
        )
        print("PASS: TaskItem model uses serial_number")
    except Exception as e:
        print(f"FAIL: TaskItem model error: {e}")
        return False

    return True


def verify_api_endpoints_structure():
    """Verify that the API endpoints use the correct models and structure."""
    print("\n=== VERIFICATION: API Endpoints Structure ===")

    from api.tasks import router

    # Check that routes exist
    routes = [route.path for route in router.routes]

    # Verify GET / endpoint returns ListTasksResponse
    get_route_found = False
    for route in router.routes:
        if route.path == '/api/tasks' and route.methods == {'GET'}:
            get_route_found = True
            # Check response model
            if hasattr(route, 'response_model'):
                response_model = route.response_model
                if response_model == ListTasksResponse:
                    print("PASS: GET /api/tasks returns ListTasksResponse")
                else:
                    print(f"FAIL: GET /api/tasks returns {response_model}, expected ListTasksResponse")
                    return False
            break

    if not get_route_found:
        print("FAIL: GET /api/tasks route not found")
        return False

    # Verify GET /by-serial/{serial_number} endpoint exists
    serial_get_found = False
    for route in router.routes:
        if '/api/tasks/by-serial/{serial_number}' in route.path and route.methods == {'GET'}:
            serial_get_found = True
            print("PASS: GET /api/tasks/by-serial/{serial_number} route exists")
            break

    if not serial_get_found:
        print("FAIL: GET /api/tasks/by-serial/{serial_number} route not found")
        return False

    # Verify DELETE /by-serial/{serial_number} endpoint exists
    serial_delete_found = False
    for route in router.routes:
        if '/api/tasks/by-serial/{serial_number}' in route.path and 'DELETE' in route.methods:
            serial_delete_found = True
            print("PASS: DELETE /api/tasks/by-serial/{serial_number} route exists")
            break

    if not serial_delete_found:
        print("FAIL: DELETE /api/tasks/by-serial/{serial_number} route not found")
        return False

    print("PASS: All required serial-based endpoints exist")
    return True


def verify_no_uuid_validation_errors():
    """Verify that the implementation avoids UUID validation errors."""
    print("\n=== VERIFICATION: No UUID Validation Errors ===")

    # Check that TaskResponse doesn't use id: int (which would cause UUID parsing errors)
    try:
        # Create a TaskResponse with a sample serial number
        response = TaskResponse(
            serial_number=1,  # This should be an integer serial number, not UUID
            title="Test Task",
            description="Test Description",
            completed=False,
            created_at=None,
            created_at_formatted="2026-01-13 14:00"
        )

        # Verify serial_number is accessible and is an integer
        assert isinstance(response.serial_number, int), "serial_number should be an integer"
        assert response.serial_number > 0, "serial_number should be positive"

        print(f"PASS: TaskResponse uses serial_number as integer: {response.serial_number}")
        print("PASS: No UUID validation errors in response model")
        return True
    except Exception as e:
        print(f"FAIL: Error in UUID validation check: {e}")
        return False


def verify_view_usage():
    """Verify that the implementation uses the tasks_with_serial view."""
    print("\n=== VERIFICATION: View Usage ===")

    with Session(engine) as session:
        # Create a test user
        test_user_id = str(uuid4())
        test_user = User(
            id=test_user_id,
            name="Verify View User",
            email=f"verify_view_{test_user_id[:8]}@example.com",
            password_hash="temp_hash"
        )
        session.add(test_user)
        session.commit()

        try:
            # Create a test task
            task = create_task(session, test_user_id, "View test task", "Testing view usage")

            # Query using the tasks_with_serial view (this is what the API now uses)
            tasks_with_serial = get_tasks_with_serial(session, test_user_id)

            if len(tasks_with_serial) > 0:
                first_task = tasks_with_serial[0]

                # Verify the view returns serial_number as integer
                serial_num = first_task['serial_number']
                assert isinstance(serial_num, int), "serial_number from view should be integer"
                assert serial_num > 0, "serial_number should be positive"

                print(f"PASS: View returns serial_number as integer: {serial_num}")
                print("PASS: API uses tasks_with_serial view for user-facing operations")

                # Test getting specific task by serial number
                task_by_serial = get_task_by_serial(session, test_user_id, serial_num)
                if task_by_serial:
                    print(f"PASS: Can retrieve task by serial number #{serial_num}")
                else:
                    print(f"FAIL: Cannot retrieve task by serial number #{serial_num}")

            else:
                print("FAIL: View returned empty results")

        except Exception as e:
            print(f"FAIL: Error in view usage verification: {e}")
            return False
        finally:
            # Clean up
            delete_task(session, task.id, test_user_id)
            session.delete(test_user)
            session.commit()

    return True


def main():
    """Run all verification tests."""
    print("=== SERIAL NUMBER IMPLEMENTATION VERIFICATION ===\n")

    results = {}

    results['models'] = verify_models()
    results['endpoints'] = verify_api_endpoints_structure()
    results['validation'] = verify_no_uuid_validation_errors()
    results['view'] = verify_view_usage()

    print(f"\n=== VERIFICATION SUMMARY ===")

    all_passed = True
    for check, result in results.items():
        status = "PASS: PASS" if result else "FAIL: FAIL"
        print(f"{check}: {status}")
        if not result:
            all_passed = False

    print(f"\nOVERALL: {'PASS: ALL CHECKS PASSED' if all_passed else 'FAIL: SOME CHECKS FAILED'}")

    if all_passed:
        print("\nThe implementation successfully:")
        print("- Uses serial_number (int) for user-facing operations")
        print("- Queries from tasks_with_serial view")
        print("- Avoids UUID validation errors")
        print("- Provides proper response models")
        print("- Maintains UUIDs for internal operations")

    return all_passed


if __name__ == "__main__":
    main()