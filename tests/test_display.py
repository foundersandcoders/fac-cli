"""Tests for display module."""

import pytest
import sys
from unittest.mock import patch, Mock
from io import StringIO

# Add parent directory to path for imports
sys.path.insert(0, "..")

import display


class TestDisplayFormat:
    """Test data formatting functionality."""

    def test_should_format_data_with_matching_columns_and_headers(self):
        """Test formatting with matching columns and headers."""
        # Arrange
        data = [
            {"name": "John", "email": "john@example.com", "status": "active"},
            {"name": "Jane", "email": "jane@example.com", "status": "inactive"},
        ]
        columns = ["name", "email", "status"]
        headers = ["Name", "Email", "Status"]

        # Act
        result = display.format(data, columns, headers)

        # Assert
        assert len(result) == 2
        assert result[0] == ["John", "john@example.com", "active"]
        assert result[1] == ["Jane", "jane@example.com", "inactive"]

    def test_should_handle_missing_columns_gracefully(self):
        """Test formatting when data is missing expected columns."""
        # Arrange
        data = [
            {"name": "John", "email": "john@example.com"},  # Missing status
            {"name": "Jane", "status": "inactive"},  # Missing email
        ]
        columns = ["name", "email", "status"]
        headers = ["Name", "Email", "Status"]

        # Act
        result = display.format(data, columns, headers)

        # Assert
        assert len(result) == 2
        assert result[0] == ["John", "john@example.com", ""]
        assert result[1] == ["Jane", "", "inactive"]

    def test_should_handle_none_values_correctly(self):
        """Test formatting with None values in data."""
        # Arrange
        data = [
            {"name": "John", "email": None, "status": "active"},
            {"name": None, "email": "jane@example.com", "status": None},
        ]
        columns = ["name", "email", "status"]
        headers = ["Name", "Email", "Status"]

        # Act
        result = display.format(data, columns, headers)

        # Assert
        assert result[0] == ["John", "", "active"]
        assert result[1] == ["", "jane@example.com", ""]

    def test_should_truncate_long_values(self):
        """Test that long values are truncated with ellipsis."""
        # Arrange
        long_value = "a" * 60  # Longer than 50 character limit
        data = [{"name": "John", "description": long_value}]
        columns = ["name", "description"]
        headers = ["Name", "Description"]

        # Act
        result = display.format(data, columns, headers)

        # Assert
        assert len(result[0][1]) == 50  # 47 chars + "..."
        assert result[0][1].endswith("...")

    def test_should_handle_empty_data_list(self):
        """Test formatting with empty data list."""
        # Arrange
        data = []
        columns = ["name", "email"]
        headers = ["Name", "Email"]

        # Act
        result = display.format(data, columns, headers)

        # Assert
        assert result == []

    def test_should_raise_error_for_mismatched_columns_headers(self):
        """Test error when columns and headers count don't match."""
        # Arrange
        data = [{"name": "John", "email": "john@example.com"}]
        columns = ["name", "email"]
        headers = ["Name"]  # Missing header

        # Act & Assert
        with pytest.raises(SystemExit) as exit_info:
            display.format(data, columns, headers)

        assert exit_info.value.code == 1


class TestDisplayTable:
    """Test table formatting functionality."""

    @patch("display.tabulate")
    def test_should_create_table_with_grid_format_by_default(self, mock_tabulate):
        """Test table creation with default grid format."""
        # Arrange
        data = [["John", "john@example.com"], ["Jane", "jane@example.com"]]
        headers = ["Name", "Email"]
        mock_tabulate.return_value = "formatted_table"

        # Act
        result = display.table(data, headers)

        # Assert
        mock_tabulate.assert_called_once_with(data, headers=headers, tablefmt="grid")
        assert result == "formatted_table"

    @patch("display.tabulate")
    def test_should_create_table_with_custom_style(self, mock_tabulate):
        """Test table creation with custom style."""
        # Arrange
        data = [["John", "john@example.com"]]
        headers = ["Name", "Email"]
        mock_tabulate.return_value = "formatted_table"

        # Act
        result = display.table(data, headers, style="simple")

        # Assert
        mock_tabulate.assert_called_once_with(data, headers=headers, tablefmt="simple")
        assert result == "formatted_table"

    def test_should_return_no_data_message_for_empty_data(self):
        """Test table formatting with empty data."""
        # Arrange
        data = []
        headers = ["Name", "Email"]

        # Act
        result = display.table(data, headers)

        # Assert
        assert result == "No data to display"

    @patch("display.tabulate")
    def test_should_handle_tabulate_errors_gracefully(self, mock_tabulate):
        """Test error handling when tabulate fails."""
        # Arrange
        data = [["John", "john@example.com"]]
        headers = ["Name", "Email"]
        mock_tabulate.side_effect = Exception("Tabulate error")

        # Act & Assert
        with pytest.raises(SystemExit) as exit_info:
            display.table(data, headers)

        assert exit_info.value.code == 1


class TestDisplayPrintTable:
    """Test complete table printing functionality."""

    @patch("display.print")
    @patch("display.format")
    @patch("display.table")
    def test_should_print_formatted_table_for_valid_data(
        self, mock_table, mock_format, mock_print
    ):
        """Test complete table printing workflow."""
        # Arrange
        data = [{"name": "John", "email": "john@example.com"}]
        columns = ["name", "email"]
        headers = ["Name", "Email"]

        mock_format.return_value = [["John", "john@example.com"]]
        mock_table.return_value = "formatted_table_output"

        # Act
        display.print_table(data, columns, headers)

        # Assert
        mock_format.assert_called_once_with(data, columns, headers)
        mock_table.assert_called_once_with([["John", "john@example.com"]], headers)
        mock_print.assert_called_once_with("formatted_table_output")

    @patch("builtins.print")
    def test_should_print_no_data_message_for_empty_data(self, mock_print):
        """Test printing when no data is available."""
        # Arrange
        data = []
        columns = ["name", "email"]
        headers = ["Name", "Email"]

        # Act
        display.print_table(data, columns, headers)

        # Assert
        mock_print.assert_called_once_with("No data available")


class TestDisplayMessages:
    """Test message printing functionality."""

    @patch("builtins.print")
    def test_should_print_success_message_with_checkmark(self, mock_print):
        """Test success message formatting."""
        # Act
        display.print_success("Operation completed")

        # Assert
        mock_print.assert_called_once_with("✓ Operation completed")

    @patch("builtins.print")
    def test_should_print_info_message_with_info_icon(self, mock_print):
        """Test info message formatting."""
        # Act
        display.print_info("Processing data")

        # Assert
        mock_print.assert_called_once_with("ℹ Processing data")

    @patch("builtins.print")
    def test_should_print_warning_message_to_stderr(self, mock_print):
        """Test warning message is printed to stderr."""
        # Act
        display.print_warning("Warning message")

        # Assert
        mock_print.assert_called_once_with("⚠ Warning message", file=sys.stderr)

    @patch("builtins.print")
    def test_should_print_error_message_to_stderr(self, mock_print):
        """Test error message is printed to stderr."""
        # Act
        display.print_error("Error occurred")

        # Assert
        mock_print.assert_called_once_with("✗ Error occurred", file=sys.stderr)


class TestDisplayError:
    """Test error handling functionality."""

    @patch("display.print_error")
    def test_should_print_error_and_exit_with_default_code(self, mock_print_error):
        """Test error function prints and exits with default code."""
        # Act & Assert
        with pytest.raises(SystemExit) as exit_info:
            display.error("Test error message")

        mock_print_error.assert_called_once_with("Test error message")
        assert exit_info.value.code == 1

    @patch("display.print_error")
    def test_should_print_error_and_exit_with_custom_code(self, mock_print_error):
        """Test error function prints and exits with custom code."""
        # Act & Assert
        with pytest.raises(SystemExit) as exit_info:
            display.error("Custom error", 42)

        mock_print_error.assert_called_once_with("Custom error")
        assert exit_info.value.code == 42


class TestDisplayIntegration:
    """Integration tests for display module."""

    def test_should_handle_complete_workflow_with_real_data(self):
        """Test complete display workflow with real data."""
        # Arrange
        data = [
            {"name": "John Doe", "email": "john@example.com", "status": "active"},
            {"name": "Jane Smith", "email": "jane@example.com", "status": "pending"},
        ]
        columns = ["name", "email", "status"]
        headers = ["Full Name", "Email Address", "Status"]

        # Act - should not raise exceptions
        formatted = display.format(data, columns, headers)
        table_output = display.table(formatted, headers)

        # Assert
        assert len(formatted) == 2
        assert isinstance(table_output, str)
        assert "Full Name" in table_output
        assert "John Doe" in table_output
        assert "Jane Smith" in table_output

    def test_should_handle_edge_cases_gracefully(self):
        """Test edge cases in display functionality."""
        # Test with mixed data types
        data = [
            {"id": 1, "name": "John", "active": True, "score": 95.5},
            {"id": 2, "name": "Jane", "active": False, "score": None},
        ]
        columns = ["id", "name", "active", "score"]
        headers = ["ID", "Name", "Active", "Score"]

        # Act - should handle type conversion gracefully
        formatted = display.format(data, columns, headers)

        # Assert
        assert formatted[0] == ["1", "John", "True", "95.5"]
        assert formatted[1] == ["2", "Jane", "False", ""]
