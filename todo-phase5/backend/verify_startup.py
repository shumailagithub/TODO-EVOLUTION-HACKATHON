import requests
import sys
import os
import time

def verify_server_running(port=8001):
    """
    Test if server is running on the specified port
    """
    base_url = f"http://127.0.0.1:{port}"

    print(f"Verifying server on {base_url}...")

    checks = [
        {"name": "Health Check (/)", "endpoint": "/", "method": "GET", "expected_status": 200, "data": None},
        {"name": "Docs Endpoint (/docs)", "endpoint": "/docs", "method": "GET", "expected_status": 200, "data": None},
        {"name": "API Todos Endpoint (OPTIONS)", "endpoint": "/api/todos", "method": "OPTIONS", "expected_status": 200, "data": None},
        {"name": "Chat Endpoint (OPTIONS)", "endpoint": "/api/chat", "method": "OPTIONS", "expected_status": 200, "data": None},
    ]

    all_passed = True

    for check in checks:
        try:
            url = base_url + check["endpoint"]
            if check["method"] == "GET":
                response = requests.get(url, timeout=10)
            elif check["method"] == "POST":
                response = requests.post(url, timeout=10, json=check.get("data", {}))
            elif check["method"] == "OPTIONS":
                response = requests.options(url, timeout=10)

            if response.status_code == check["expected_status"]:
                print(f"[PASS] {check['name']}: {response.status_code}")
            else:
                print(f"[FAIL] {check['name']}: Expected {check['expected_status']}, got {response.status_code}")
                all_passed = False

        except requests.exceptions.ConnectionError:
            print(f"[FAIL] {check['name']}: Connection refused")
            all_passed = False
        except requests.exceptions.Timeout:
            print(f"[FAIL] {check['name']}: Request timed out")
            all_passed = False
        except Exception as e:
            print(f"[FAIL] {check['name']}: Error - {e}")
            all_passed = False

    return all_passed

def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8001

    print(f"Server startup verification for port {port}")
    print("=" * 50)

    # Give the server a moment to start if it was just launched
    time.sleep(2)

    success = verify_server_running(port)

    print("=" * 50)
    if success:
        print("[PASS] All checks passed! Server is running correctly.")
        sys.exit(0)
    else:
        print("[FAIL] Some checks failed! Server may not be running correctly.")
        sys.exit(1)

if __name__ == "__main__":
    main()