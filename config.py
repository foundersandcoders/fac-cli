"""Configuration management for FAC CLI."""

import os
import sys
from typing import Dict, Optional

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


def load() -> None:
    """Load environment variables from .env file if available."""
    if load_dotenv:
        load_dotenv()


def get(key: str, default: Optional[str] = None) -> Optional[str]:
    """Get environment variable value."""
    return os.getenv(key, default)


def require(key: str) -> str:
    """Get required environment variable or exit with error."""
    value = get(key)
    if not value:
        error(f"Required environment variable {key} not set")
    return value


def validate() -> Dict[str, str]:
    """Validate required configuration and return config dict."""
    load()

    config = {}
    required_vars = ["AIRTABLE_API_KEY", "AIRTABLE_VIEW_URL"]

    for var in required_vars:
        config[var] = require(var)

    # Optional configuration
    config["GR_COLUMNS"] = get("GR_COLUMNS", "Name,Email,Status,Date")
    config["GR_HEADERS"] = get(
        "GR_HEADERS", "Student Name,Email Address,Current Status,Last Updated"
    )
    config["FAC_CLI_DEBUG"] = get("FAC_CLI_DEBUG", "false").lower() == "true"

    return config


def error(message: str, exit_code: int = 1) -> None:
    """Print error message and exit."""
    print(f"Error: {message}", file=sys.stderr)
    print("Tip: Copy .env.example to .env and add your credentials", file=sys.stderr)
    sys.exit(exit_code)
