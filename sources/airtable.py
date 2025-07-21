"""Airtable API integration for FAC CLI."""

import sys
from typing import Dict, List, Optional

try:
    import requests
except ImportError:
    print(
        "Error: requests library not installed. Run: pip install -r requirements.txt",
        file=sys.stderr,
    )
    sys.exit(1)


def auth(api_key: str) -> Dict[str, str]:
    """Create authentication headers for Airtable API."""
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def request(url: str, headers: Dict[str, str], timeout: int = 30) -> requests.Response:
    """Make HTTP request to Airtable API."""
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response
    except requests.exceptions.Timeout:
        error("Request timed out. Check your internet connection.")
    except requests.exceptions.ConnectionError:
        error("Unable to connect to Airtable. Check your internet connection.")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            error("Invalid Airtable API key. Check your credentials in .env file.")
        elif e.response.status_code == 404:
            error("Airtable view not found. Check your AIRTABLE_VIEW_URL in .env file.")
        elif e.response.status_code == 429:
            error("Airtable API rate limit exceeded. Please try again later.")
        else:
            error(f"Airtable API error: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        error(f"Unexpected error connecting to Airtable: {str(e)}")


def get(api_key: str, view_url: str) -> List[Dict]:
    """Get data from Airtable view."""
    if not api_key or not view_url:
        error("Airtable API key and view URL are required")

    # Convert user-friendly URL to API URL if needed
    api_url = convert_url(view_url)

    headers = auth(api_key)
    response = request(api_url, headers)

    try:
        data = response.json()
    except ValueError:
        error("Invalid response from Airtable API. Expected JSON.")

    if "records" not in data:
        error("Unexpected response format from Airtable. Missing 'records' field.")

    return extract(data["records"])


def convert_url(url: str) -> str:
    """Convert user-friendly Airtable URL to API URL."""
    # If already an API URL, return as-is
    if url.startswith("https://api.airtable.com/"):
        return url

    # Parse user-friendly URL format: https://airtable.com/appXXXXX/tblXXXXX/viwXXXXX
    if not url.startswith("https://airtable.com/"):
        error(
            "Invalid Airtable URL. Expected format: https://airtable.com/appXXXXX/tblXXXXX/viwXXXXX"
        )

    # Extract components from URL
    parts = url.replace("https://airtable.com/", "").split("/")

    if len(parts) < 3:
        error(
            "Invalid Airtable URL format. Expected: https://airtable.com/appXXXXX/tblXXXXX/viwXXXXX"
        )

    app_id = parts[0]  # appXXXXX
    table_id = parts[1]  # tblXXXXX
    view_id = parts[2]  # viwXXXXX

    # Validate component formats
    if not (
        app_id.startswith("app")
        and table_id.startswith("tbl")
        and view_id.startswith("viw")
    ):
        error(
            "Invalid Airtable URL components. Expected appXXXXX/tblXXXXX/viwXXXXX format"
        )

    # Convert to API URL format
    api_url = f"https://api.airtable.com/v0/{app_id}/{table_id}?view={view_id}"

    return api_url


def extract(records: List[Dict]) -> List[Dict]:
    """Extract field data from Airtable records."""
    extracted = []

    for record in records:
        if "fields" in record:
            extracted.append(record["fields"])
        else:
            # Handle records without fields gracefully
            continue

    return extracted


def error(message: str, exit_code: int = 1) -> None:
    """Print error message and exit."""
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(exit_code)
