from dotenv import load_dotenv, find_dotenv
import os

def load_env():
    """Load environment variables from .env file."""
    _ = load_dotenv(find_dotenv())

def get_env_var(key: str, fallback: str = None):
    """Safely fetch an environment variable."""
    value = os.getenv(key)
    if not value and fallback:
        return fallback
    if not value:
        raise ValueError(f"Missing required environment variable: {key}")
    return value
