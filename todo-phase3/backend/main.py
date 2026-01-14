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

# Create FastAPI app
app = FastAPI(title="Todo API Phase-2", version="0.1.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002", "http://localhost:3003", "http://localhost:3004", "http://localhost:3005", "http://localhost:3006"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# Register API routers
app.include_router(auth_router)
app.include_router(tasks_router)
app.include_router(chat_router)


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
