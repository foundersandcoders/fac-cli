"""Gateway Recent command for FAC CLI."""

from typing import Dict, List

import config
import display
from sources import airtable


def run(args: List[str]) -> None:
    """Execute gateway recent command."""
    display.print_info("Fetching gateway recent data...")

    data = fetch()
    processed = process(data)
    display_data(processed)

    display.print_success(f"Displayed {len(processed)} records")


def fetch() -> List[Dict]:
    """Fetch data via airtable source."""
    cfg = config.validate()

    api_key = cfg["AIRTABLE_API_KEY"]
    view_url = cfg["AIRTABLE_VIEW_URL"]

    return airtable.get(api_key, view_url)


def process(data: List[Dict]) -> List[Dict]:
    """Transform raw data for display."""
    if not data:
        return []

    processed = []
    for record in data:
        processed_record = record.copy()

        # Process Family name field specifically
        if "Family name" in processed_record:
            name = flatten_array_value(processed_record["Family name"])
            processed_record["Family name"] = abbreviate_name(name)

        processed.append(processed_record)

    return processed


def flatten_array_value(value):
    """Convert array values to strings, pass through strings unchanged."""
    if isinstance(value, list):
        if len(value) > 0:
            return str(value[0])
        else:
            return ""  # Handle empty arrays
    return str(value) if value is not None else ""


def abbreviate_name(name: str) -> str:
    """Return first 4 characters of name, or full name if shorter."""
    return name[:4]


def display_data(data: List[Dict]) -> None:
    """Format and show data in terminal."""
    cfg = config.validate()

    columns = parse_columns(cfg["GR_COLUMNS"])
    headers = parse_headers(cfg["GR_HEADERS"])

    display.print_table(data, columns, headers)


def parse_columns(columns_str: str) -> List[str]:
    """Parse comma-separated column names."""
    return [col.strip() for col in columns_str.split(",") if col.strip()]


def parse_headers(headers_str: str) -> List[str]:
    """Parse comma-separated header names."""
    return [header.strip() for header in headers_str.split(",") if header.strip()]
