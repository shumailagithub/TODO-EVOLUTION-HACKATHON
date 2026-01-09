"""
Backend configuration module.
Loads environment variables and provides configuration values.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Required configuration values
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

JWT_SECRET = os.getenv("JWT_SECRET")
if not JWT_SECRET:
    raise ValueError("JWT_SECRET environment variable is required")

# Optional configuration values with defaults
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
BCRYPT_ROUNDS = int(os.getenv("BCRYPT_ROUNDS", "12"))

# Configuration validation
if len(JWT_SECRET) < 32:
    raise ValueError("JWT_SECRET must be at least 32 characters long")
