#!/usr/bin/env python3
"""
Safe start script that removes problematic paths and handles port conflicts before starting the server.
"""

import sys
import os
import subprocess

def cleanup_port_direct(port):
    """
    Detect and kill process using the specified port on Windows
    """
    print(f"Checking for processes using port {port}...")

    try:
        # Use netstat to find the process using the port
        result = subprocess.run(
            ['netstat', '-ano', '|', 'findstr', f':{port}'],
            shell=True,
            capture_output=True,
            text=True
        )

        if result.returncode != 0 or not result.stdout.strip():
            print(f"Port {port} is free")
            return True

        lines = result.stdout.strip().split('\n')
        for line in lines:
            if f':{port}' in line:
                # Extract PID from the last column
                parts = line.split()
                if len(parts) >= 5:
                    pid = parts[4]  # PID is in the 5th column
                    print(f"Found process using port {port}: PID {pid}")

                    # Kill the process using taskkill
                    kill_result = subprocess.run(
                        ['taskkill', '/PID', pid, '/F'],
                        capture_output=True,
                        text=True
                    )

                    if kill_result.returncode == 0:
                        print(f"Successfully killed process {pid}")
                        return True
                    else:
                        print(f"Failed to kill process {pid}: {kill_result.stderr}")
                        return False

    except Exception as e:
        print(f"Error checking port {port}: {e}")
        return False

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

def start_server_with_fallback():
    """Start the server with port fallback logic."""
    import uvicorn

    # Load port configuration from environment
    port_str = os.getenv('PORT', '8001')
    fallback_ports_str = os.getenv('FALLBACK_PORTS', '8002,8003,8004')

    # Parse ports
    primary_port = int(port_str)
    fallback_ports = [int(p.strip()) for p in fallback_ports_str.split(',') if p.strip()]

    # Try primary port first
    ports_to_try = [primary_port] + fallback_ports

    for port in ports_to_try:
        print(f"Attempting to start server on port {port}...")

        # Clean up the port before attempting to use it
        if cleanup_port_direct(port):
            try:
                import main
                app = main.app
                print(f"SUCCESS: Successfully imported main application!")

                # Start the server on the available port
                print(f"STARTING: Starting backend server on http://127.0.0.1:{port}")
                print(f"INFO: Uvicorn running on http://127.0.0.1:{port}")
                uvicorn.run(app, host="127.0.0.1", port=port, reload=False)
                return  # Exit if successful
            except OSError as e:
                if e.errno == 10048:  # Port already in use (Windows error)
                    print(f"Port {port} is still in use, trying next port...")
                    continue
                else:
                    print(f"ERROR: Failed to start server on port {port}: {e}")
                    raise
            except Exception as e:
                print(f"ERROR: Unexpected error starting server on port {port}: {e}")
                raise
        else:
            print(f"Could not clean up port {port}, trying next port...")
            continue

    print("ERROR: Could not start server on any available port")
    sys.exit(1)

def main():
    print("Starting safe backend initialization...")
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

    # Start the server with port fallback logic
    start_server_with_fallback()

if __name__ == "__main__":
    main()