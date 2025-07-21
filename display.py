"""Terminal display formatting for FAC CLI."""

import sys
from typing import Dict, List, Optional

try:
    from tabulate import tabulate
except ImportError:
    print(
        "Error: tabulate library not installed. Run: pip install -r requirements.txt",
        file=sys.stderr,
    )
    sys.exit(1)


def format(data: List[Dict], columns: List[str], headers: List[str]) -> List[List[str]]:
    """Format data for display by selecting columns."""
    if len(columns) != len(headers):
        error(f"Columns ({len(columns)}) and headers ({len(headers)}) count mismatch")

    formatted = []
    for row in data:
        formatted_row = []
        for column in columns:
            value = row.get(column, "")
            # Convert to string and handle None values
            str_value = str(value) if value is not None else ""
            # Truncate long values for better display
            if len(str_value) > 50:
                str_value = str_value[:47] + "..."
            formatted_row.append(str_value)
        formatted.append(formatted_row)

    return formatted


def table(data: List[List[str]], headers: List[str], style: str = "grid") -> str:
    """Create formatted table string."""
    if not data:
        return "No data to display"

    try:
        return tabulate(data, headers=headers, tablefmt=style)
    except Exception as e:
        error(f"Error formatting table: {str(e)}")


def print_table(data: List[Dict], columns: List[str], headers: List[str]) -> None:
    """Print formatted table to terminal."""
    if not data:
        print("No data available")
        return

    formatted_data = format(data, columns, headers)
    table_output = table(formatted_data, headers)
    print(table_output)


def print_success(message: str) -> None:
    """Print success message."""
    print(f"✓ {message}")


def print_info(message: str) -> None:
    """Print informational message."""
    print(f"ℹ {message}")


def print_warning(message: str) -> None:
    """Print warning message to stderr."""
    print(f"⚠ {message}", file=sys.stderr)


def print_error(message: str) -> None:
    """Print error message to stderr."""
    print(f"✗ {message}", file=sys.stderr)


def error(message: str, exit_code: int = 1) -> None:
    """Print error message and exit."""
    print_error(message)
    sys.exit(exit_code)
