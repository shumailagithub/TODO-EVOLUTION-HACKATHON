# backend\main.py
"""
Main FastAPI application.
Registers API routers and configures CORS middleware.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.auth import router as auth_router
from api.tasks import router as tasks_router
from api.chat import router as chat_router
from db.connection import get_session
from db.serial_view import create_tasks_with_serial_view

# Create FastAPI app
app = FastAPI(title="Todo API Phase-2", version="0.1.0")

# Configure CORS
# Allow origins from environment variable, with default for local development
import os
allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:3001,http://localhost:3002,http://localhost:3003,http://localhost:3004,http://localhost:3005,http://localhost:3006")
allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# Register API routers
app.include_router(auth_router)
app.include_router(tasks_router)
app.include_router(chat_router)


@app.on_event("startup")
def startup_event():
    """Initialize the tasks_with_serial view when the application starts."""
    print("Initializing tasks_with_serial view...")
    with next(get_session()) as session:
        success = create_tasks_with_serial_view(session)
        if success:
            print("Successfully created/updated tasks_with_serial view")
        else:
            print("Failed to create/update tasks_with_serial view")


@app.get("/")
async def root():
    """Root endpoint for health check."""
    return {
        "message": "Todo API Phase-2",
        "status": "running",
        "endpoints": {
            "auth": "/api/auth",
            "tasks": "/api/tasks",
            "chat": "/api/{user_id}/chat"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True
    )
