"""Tests for config module."""

import os
import pytest
from unittest.mock import patch, mock_open
import sys
import tempfile

# Add parent directory to path for imports
sys.path.insert(0, "..")

import config


class TestConfigLoad:
    """Test configuration loading functionality."""

    @patch("config.load_dotenv")
    def test_should_load_dotenv_when_available(self, mock_load_dotenv):
        """Test that load_dotenv is called when available."""
        # Act
        config.load()

        # Assert
        mock_load_dotenv.assert_called_once()

    @patch("config.load_dotenv", None)
    def test_should_handle_missing_dotenv_gracefully(self):
        """Test that missing dotenv doesn't crash the system."""
        # Act & Assert - should not raise exception
        config.load()


class TestConfigGet:
    """Test environment variable retrieval."""

    @patch.dict(os.environ, {"TEST_VAR": "test_value"})
    def test_should_return_environment_variable_when_exists(self):
        """Test retrieval of existing environment variable."""
        # Act
        result = config.get("TEST_VAR")

        # Assert
        assert result == "test_value"

    @patch.dict(os.environ, {}, clear=True)
    def test_should_return_default_when_variable_missing(self):
        """Test default value returned for missing variable."""
        # Act
        result = config.get("MISSING_VAR", "default_value")

        # Assert
        assert result == "default_value"

    @patch.dict(os.environ, {}, clear=True)
    def test_should_return_none_when_variable_missing_and_no_default(self):
        """Test None returned when variable missing and no default."""
        # Act
        result = config.get("MISSING_VAR")

        # Assert
        assert result is None


class TestConfigRequire:
    """Test required environment variable functionality."""

    @patch.dict(os.environ, {"REQUIRED_VAR": "required_value"})
    def test_should_return_value_when_required_variable_exists(self):
        """Test that required variable returns correct value."""
        # Act
        result = config.require("REQUIRED_VAR")

        # Assert
        assert result == "required_value"

    @patch.dict(os.environ, {}, clear=True)
    def test_should_exit_when_required_variable_missing(self):
        """Test system exit when required variable is missing."""
        # Act & Assert
        with pytest.raises(SystemExit) as exit_info:
            config.require("MISSING_REQUIRED_VAR")

        assert exit_info.value.code == 1

    @patch.dict(os.environ, {"EMPTY_VAR": ""}, clear=True)
    def test_should_exit_when_required_variable_empty(self):
        """Test system exit when required variable is empty string."""
        # Act & Assert
        with pytest.raises(SystemExit) as exit_info:
            config.require("EMPTY_VAR")

        assert exit_info.value.code == 1


class TestConfigValidate:
    """Test configuration validation functionality."""

    @patch.dict(
        os.environ,
        {
            "AIRTABLE_API_KEY": "test_api_key",
            "AIRTABLE_VIEW_URL": "https://airtable.com/app123/tbl456/viw789",
        },
    )
    @patch("config.load")
    def test_should_return_complete_config_when_all_required_vars_present(
        self, mock_load
    ):
        """Test complete configuration returned with all required variables."""
        # Act
        result = config.validate()

        # Assert
        mock_load.assert_called_once()
        assert result["AIRTABLE_API_KEY"] == "test_api_key"
        assert (
            result["AIRTABLE_VIEW_URL"] == "https://airtable.com/app123/tbl456/viw789"
        )
        assert "GR_COLUMNS" in result
        assert "GR_HEADERS" in result
        assert "FAC_CLI_DEBUG" in result

    @patch.dict(
        os.environ,
        {
            "AIRTABLE_API_KEY": "test_api_key",
            "AIRTABLE_VIEW_URL": "https://airtable.com/app123/tbl456/viw789",
            "GR_COLUMNS": "Custom,Columns",
            "GR_HEADERS": "Custom Headers,More Headers",
            "FAC_CLI_DEBUG": "true",
        },
    )
    @patch("config.load")
    def test_should_use_custom_optional_values_when_provided(self, mock_load):
        """Test that custom optional values are used when provided."""
        # Act
        result = config.validate()

        # Assert
        assert result["GR_COLUMNS"] == "Custom,Columns"
        assert result["GR_HEADERS"] == "Custom Headers,More Headers"
        assert result["FAC_CLI_DEBUG"] == True

    @patch.dict(
        os.environ,
        {
            "AIRTABLE_API_KEY": "test_api_key",
            "AIRTABLE_VIEW_URL": "https://airtable.com/app123/tbl456/viw789",
        },
    )
    @patch("config.load")
    def test_should_use_default_optional_values_when_not_provided(self, mock_load):
        """Test that default optional values are used when not provided."""
        # Act
        result = config.validate()

        # Assert
        assert result["GR_COLUMNS"] == "Name,Email,Status,Date"
        assert (
            result["GR_HEADERS"]
            == "Student Name,Email Address,Current Status,Last Updated"
        )
        assert result["FAC_CLI_DEBUG"] == False

    @patch.dict(os.environ, {"AIRTABLE_API_KEY": "test_api_key"}, clear=True)
    @patch("config.load")
    def test_should_exit_when_airtable_view_url_missing(self, mock_load):
        """Test system exit when AIRTABLE_VIEW_URL is missing."""
        # Act & Assert
        with pytest.raises(SystemExit) as exit_info:
            config.validate()

        assert exit_info.value.code == 1

    @patch.dict(
        os.environ,
        {"AIRTABLE_VIEW_URL": "https://airtable.com/app123/tbl456/viw789"},
        clear=True,
    )
    @patch("config.load")
    def test_should_exit_when_airtable_api_key_missing(self, mock_load):
        """Test system exit when AIRTABLE_API_KEY is missing."""
        # Act & Assert
        with pytest.raises(SystemExit) as exit_info:
            config.validate()

        assert exit_info.value.code == 1

    @patch.dict(os.environ, {}, clear=True)
    @patch("config.load")
    def test_should_exit_when_all_required_vars_missing(self, mock_load):
        """Test system exit when all required variables are missing."""
        # Act & Assert
        with pytest.raises(SystemExit) as exit_info:
            config.validate()

        assert exit_info.value.code == 1


class TestConfigError:
    """Test error handling functionality."""

    @patch("builtins.print")
    def test_should_print_error_message_and_tip(self, mock_print):
        """Test that error function prints correct messages."""
        # Act & Assert
        with pytest.raises(SystemExit) as exit_info:
            config.error("Test error message")

        assert exit_info.value.code == 1
        assert mock_print.call_count == 2

    @patch("builtins.print")
    def test_should_exit_with_custom_code(self, mock_print):
        """Test that error function exits with custom exit code."""
        # Act & Assert
        with pytest.raises(SystemExit) as exit_info:
            config.error("Test error", 42)

        assert exit_info.value.code == 42
