import sys
import os

# Remove the problematic path if it exists in sys.path
problematic_path = r"D:\hackathons-piaic\Hackathon-2\todo-evolution\src"
if problematic_path in sys.path:
    sys.path.remove(problematic_path)
    print(f"Removed problematic path: {problematic_path}")

# Add the current directory to the beginning of the path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
    print(f"Added current directory to path: {current_dir}")

print("Updated Python path:")
for i, path in enumerate(sys.path):
    print(f"  {i}: {path}")

# Now run the main application
if __name__ == "__main__":
    import uvicorn

    print("Starting backend server on port 8001...")
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)