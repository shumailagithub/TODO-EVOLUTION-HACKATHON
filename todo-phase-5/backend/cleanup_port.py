import subprocess
import sys
import os

def cleanup_port(port):
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

if __name__ == "__main__":
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 8001  # Default port

    cleanup_port(port)