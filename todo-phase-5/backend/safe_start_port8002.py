#!/usr/bin/env python3
"""
Safe start script that removes problematic paths before importing the application.
Runs on port 8002 instead of 8001 to avoid conflicts.
"""
import sys
import os

def remove_problematic_paths():
    """Remove problematic paths from sys.path."""
    problematic_path = r"D:\hackathons-piaic\Hackathon-2\todo-evolution\src"

    # Remove the problematic path if it exists
    if problematic_path in sys.path:
        sys.path.remove(problematic_path)
        print(f"REMOVED: {problematic_path}")

    # Also check for similar patterns
    paths_to_remove = []
    for path in sys.path:
        if "todo-evolution" in path and "src" in path.split(os.sep)[-1:]:
            if path != os.path.join(os.getcwd(), "src"):  # Don't remove local src
                paths_to_remove.append(path)

    for path in paths_to_remove:
        sys.path.remove(path)
        print(f"REMOVED: {path}")

    return len(paths_to_remove) > 0 or problematic_path in sys.path

def main():
    print("Starting safe backend initialization on port 8002...")
    print(f"Current working directory: {os.getcwd()}")

    # Clean up problematic paths
    removed_any = remove_problematic_paths()

    if removed_any:
        print("Problematic paths have been removed from sys.path")
    else:
        print("No problematic paths found")

    print("\nUpdated sys.path:")
    for i, path in enumerate(sys.path[:10]):  # Show first 10 paths
        print(f"  {i}: {path}")
    if len(sys.path) > 10:
        print(f"  ... and {len(sys.path) - 10} more")

    # Now try to import and run the main application
    try:
        import main
        app = main.app
        print("\nSUCCESS: Successfully imported main application!")

        # Start the server on port 8002 instead of 8001
        import uvicorn
        print("STARTING: Starting backend server on http://127.0.0.1:8002")
        uvicorn.run(app, host="127.0.0.1", port=8002, reload=False)

    except ImportError as e:
        print(f"\nERROR: Import error: {e}")
        print("This indicates there are still import issues to resolve.")
        raise
    except Exception as e:
        print(f"\nERROR: Unexpected error: {e}")
        raise

if __name__ == "__main__":
    main()