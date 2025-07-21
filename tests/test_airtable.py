"""Tests for Airtable integration module."""

import pytest
import sys
from unittest.mock import Mock, patch

# Add parent directory to path for imports
sys.path.insert(0, "..")

from sources import airtable


class TestAirtableURLConversion:
    """Test URL conversion functionality."""

    def test_should_return_api_url_unchanged_when_already_api_format(self):
        """Test that API URLs are returned unchanged."""
        api_url = "https://api.airtable.com/v0/app123/tbl456?view=viw789"
        result = airtable.convert_url(api_url)
        assert result == api_url

    def test_should_convert_user_friendly_url_to_api_format(self):
        """Test conversion of user-friendly URLs to API format."""
        user_url = (
            "https://airtable.com/appEXAMPLE123456/tblEXAMPLE789012/viwEXAMPLE345678"
        )
        expected = "https://api.airtable.com/v0/appEXAMPLE123456/tblEXAMPLE789012?view=viwEXAMPLE345678"
        result = airtable.convert_url(user_url)
        assert result == expected

    def test_should_handle_urls_with_trailing_slash(self):
        """Test URL conversion with trailing slash."""
        user_url = "https://airtable.com/appEXAMPLE123456/tblEXAMPLE789012/viwEXAMPLE345678/"
        expected = "https://api.airtable.com/v0/appEXAMPLE123456/tblEXAMPLE789012?view=viwEXAMPLE345678"
        result = airtable.convert_url(
            user_url.rstrip("/")
        )  # Function should handle this
        assert result == expected

    def test_should_raise_error_for_invalid_url_format(self):
        """Test error handling for invalid URL formats."""
        with pytest.raises(SystemExit):
            airtable.convert_url("https://example.com/invalid")

    def test_should_raise_error_for_incomplete_url_parts(self):
        """Test error handling for URLs with missing parts."""
        with pytest.raises(SystemExit):
            airtable.convert_url("https://airtable.com/app123/tbl456")

    def test_should_raise_error_for_invalid_component_prefixes(self):
        """Test error handling for invalid component prefixes."""
        with pytest.raises(SystemExit):
            airtable.convert_url("https://airtable.com/xyz123/tblABC/viwDEF")


class TestAirtableAuth:
    """Test authentication header creation."""

    def test_should_create_correct_auth_headers(self):
        """Test that auth headers are created correctly."""
        api_key = "test_key_123"
        headers = airtable.auth(api_key)

        expected_headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        assert headers == expected_headers


class TestAirtableExtract:
    """Test data extraction from Airtable records."""

    def test_should_extract_fields_from_records(self):
        """Test extraction of field data from Airtable records."""
        records = [
            {"fields": {"Name": "John", "Email": "john@example.com"}},
            {"fields": {"Name": "Jane", "Email": "jane@example.com"}},
        ]

        result = airtable.extract(records)

        expected = [
            {"Name": "John", "Email": "john@example.com"},
            {"Name": "Jane", "Email": "jane@example.com"},
        ]

        assert result == expected

    def test_should_skip_records_without_fields(self):
        """Test that records without fields are skipped."""
        records = [
            {"fields": {"Name": "John", "Email": "john@example.com"}},
            {"id": "rec123"},  # No fields
            {"fields": {"Name": "Jane", "Email": "jane@example.com"}},
        ]

        result = airtable.extract(records)

        expected = [
            {"Name": "John", "Email": "john@example.com"},
            {"Name": "Jane", "Email": "jane@example.com"},
        ]

        assert result == expected

    def test_should_handle_empty_records_list(self):
        """Test handling of empty records list."""
        result = airtable.extract([])
        assert result == []
