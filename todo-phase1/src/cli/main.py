"""CLI interface for in-memory todo application.

This module provides the command-line interface for the todo application.
It uses argparse for command parsing and implements an interactive REPL loop
that continues until the user types 'exit'.
"""

import sys
import os

# Add project root to path to allow absolute imports from src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse

from src.models.task import TaskStatus, ValidationError
from src.services.task_service import TaskService


def cmd_add(args, service: TaskService) -> None:
    """Handle 'add' command - create a new task.

    Args:
        args: Parsed arguments containing 'title' attribute
        service: TaskService instance
    """
    try:
        task = service.add_task(args.title)
        print(f"Task added: {task.id} {task.title}")
    except ValidationError as e:
        print(e.message)


def cmd_list(args, service: TaskService) -> None:
    """Handle 'list' command - display all tasks.

    Args:
        args: Parsed arguments (no arguments for list command)
        service: TaskService instance
    """
    tasks = service.get_all_tasks()

    if not tasks:
        print("No tasks found.")
        return

    print("Tasks:")
    for task in tasks:
        print(f"{task.id} {task}")


def cmd_update(args, service: TaskService) -> None:
    """Handle 'update' command - change task title.

    Args:
        args: Parsed arguments containing 'id' and 'new_title' attributes
        service: TaskService instance
    """
    try:
        task_id = int(args.id)
        updated_task = service.update_task(task_id, args.new_title)
        print(f"Task {updated_task.id} updated: {updated_task.title}")
    except ValueError as e:
        print(e)
    except ValidationError as e:
        print(e.message)


def cmd_complete(args, service: TaskService) -> None:
    """Handle 'complete' command - mark task as completed.

    Args:
        args: Parsed arguments containing 'id' attribute
        service: TaskService instance
    """
    try:
        task_id = int(args.id)
        updated_task = service.set_task_status(task_id, TaskStatus.COMPLETED)
        print(f"Task {updated_task.id} marked as completed")
    except ValueError as e:
        print(e)


def cmd_in_progress(args, service: TaskService) -> None:
    """Handle 'in_progress' command - mark task as in progress.

    Args:
        args: Parsed arguments containing 'id' attribute
        service: TaskService instance
    """
    try:
        task_id = int(args.id)
        updated_task = service.set_task_status(task_id, TaskStatus.IN_PROGRESS)
        print(f"Task {updated_task.id} marked as in progress")
    except ValueError as e:
        print(e)


def cmd_pending(args, service: TaskService) -> None:
    """Handle 'pending' command - mark task as pending.

    Args:
        args: Parsed arguments containing 'id' attribute
        service: TaskService instance
    """
    try:
        task_id = int(args.id)
        updated_task = service.set_task_status(task_id, TaskStatus.PENDING)
        print(f"Task {updated_task.id} marked as pending")
    except ValueError as e:
        print(e)


def cmd_delete(args, service: TaskService) -> None:
    """Handle 'delete' command - remove a task.

    Args:
        args: Parsed arguments containing 'id' attribute
        service: TaskService instance
    """
    try:
        task_id = int(args.id)
        service.delete_task(task_id)
        print(f"Task {task_id} deleted")
    except ValueError as e:
        print(e)


def cmd_help(args, service: TaskService) -> None:
    """Handle 'help' command - display usage information.

    Args:
        args: Parsed arguments (no arguments for help command)
        service: TaskService instance (unused but required for consistency)
    """
    print("Available commands:")
    print("  add <title>          Add a new task")
    print("  list                  List all tasks")
    print("  update <id> <title>   Update a task title")
    print("  complete <id>         Mark task as completed")
    print("  in_progress <id>       Mark task as in progress")
    print("  pending <id>           Mark task as pending")
    print("  delete <id>            Delete a task")
    print("  help                  Show this help message")
    print("  exit                  Exit of application")


def create_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser.

    Returns:
        Configured ArgumentParser with all command subparsers
    """
    parser = argparse.ArgumentParser(
        description="In-Memory Todo Console Application - Phase I",
        add_help=False,
    )

    subparsers = parser.add_subparsers(dest="command", help="command help")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", nargs="+", help="Task title")
    add_parser.set_defaults(func=cmd_add)

    # List command
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.set_defaults(func=cmd_list)

    # Update command
    update_parser = subparsers.add_parser("update", help="Update a task title")
    update_parser.add_argument("id", help="Task ID")
    update_parser.add_argument("new_title", nargs="+", help="New title")
    update_parser.set_defaults(func=cmd_update)

    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Mark task as completed")
    complete_parser.add_argument("id", help="Task ID")
    complete_parser.set_defaults(func=cmd_complete)

    # In progress command
    in_progress_parser = subparsers.add_parser(
        "in_progress", help="Mark task as in progress"
    )
    in_progress_parser.add_argument("id", help="Task ID")
    in_progress_parser.set_defaults(func=cmd_in_progress)

    # Pending command
    pending_parser = subparsers.add_parser("pending", help="Mark task as pending")
    pending_parser.add_argument("id", help="Task ID")
    pending_parser.set_defaults(func=cmd_pending)

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", help="Task ID")
    delete_parser.set_defaults(func=cmd_delete)

    # Help command
    help_parser = subparsers.add_parser("help", help="Show this help message")
    help_parser.set_defaults(func=cmd_help)

    # Exit command
    exit_parser = subparsers.add_parser("exit", help="Exit the application")
    exit_parser.set_defaults(func=lambda args, _: None)

    return parser


def main() -> None:
    """Main entry point for CLI application.

    Runs interactive REPL loop that:
    1. Displays command prompt '>'
    2. Reads user input
    3. Parses command and arguments
    4. Validates input
    5. Executes command
    6. Displays result or error
    7. Loops back (unless 'exit' command)

    Application terminates on 'exit' command. All data is lost.
    """
    service = TaskService()
    parser = create_parser()

    print("In-Memory Todo Console Application")
    print("Type 'help' for available commands, 'exit' to quit.")
    print()

    while True:
        try:
            user_input = input("> ").strip()

            if not user_input:
                continue

            args = parser.parse_args(user_input.split())

            if args.command == "exit":
                print("Goodbye!")
                break

            if args.func:
                # Process multi-word titles
                if hasattr(args, "title") and args.title:
                    args.title = " ".join(args.title)
                if hasattr(args, "new_title") and args.new_title:
                    args.new_title = " ".join(args.new_title)

                args.func(args, service)
            else:
                parser.print_help()

        except SystemExit:
            pass
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception:
            # Gracefully handle any unexpected errors
            pass


if __name__ == "__main__":
    main()
