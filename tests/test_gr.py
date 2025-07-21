"""Tests for gateway recent (gr) command module."""

import pytest
import sys
from unittest.mock import patch, Mock

# Add parent directory to path for imports
sys.path.insert(0, "..")

from commands import gr


class TestGrRun:
    """Test gateway recent command execution."""

    @patch("commands.gr.display_data")
    @patch("commands.gr.process")
    @patch("commands.gr.fetch")
    @patch("display.print_success")
    @patch("display.print_info")
    def test_should_execute_complete_pipeline_successfully(
        self,
        mock_print_info,
        mock_print_success,
        mock_fetch,
        mock_process,
        mock_display_data,
    ):
        """Test complete gr command execution pipeline."""
        # Arrange
        mock_data = [{"Name": "John", "Email": "john@example.com"}]
        mock_processed = [{"Name": "John", "Email": "john@example.com"}]

        mock_fetch.return_value = mock_data
        mock_process.return_value = mock_processed

        # Act
        gr.run([])

        # Assert
        mock_print_info.assert_called_once_with("Fetching gateway recent data...")
        mock_fetch.assert_called_once()
        mock_process.assert_called_once_with(mock_data)
        mock_display_data.assert_called_once_with(mock_processed)
        mock_print_success.assert_called_once_with("Displayed 1 records")

    @patch("commands.gr.display_data")
    @patch("commands.gr.process")
    @patch("commands.gr.fetch")
    @patch("display.print_success")
    @patch("display.print_info")
    def test_should_handle_empty_data_correctly(
        self,
        mock_print_info,
        mock_print_success,
        mock_fetch,
        mock_process,
        mock_display_data,
    ):
        """Test handling of empty data from fetch."""
        # Arrange
        mock_fetch.return_value = []
        mock_process.return_value = []

        # Act
        gr.run([])

        # Assert
        mock_print_success.assert_called_once_with("Displayed 0 records")


class TestGrFetch:
    """Test data fetching functionality."""

    @patch("sources.airtable.get")
    @patch("config.validate")
    def test_should_fetch_data_with_correct_credentials(
        self, mock_validate, mock_airtable_get
    ):
        """Test fetching data with configuration credentials."""
        # Arrange
        mock_config = {
            "AIRTABLE_API_KEY": "test_key",
            "AIRTABLE_VIEW_URL": "https://airtable.com/app123/tbl456/viw789",
        }
        mock_data = [{"Name": "John", "Email": "john@example.com"}]

        mock_validate.return_value = mock_config
        mock_airtable_get.return_value = mock_data

        # Act
        result = gr.fetch()

        # Assert
        mock_validate.assert_called_once()
        mock_airtable_get.assert_called_once_with(
            "test_key", "https://airtable.com/app123/tbl456/viw789"
        )
        assert result == mock_data

    @patch("sources.airtable.get")
    @patch("config.validate")
    def test_should_propagate_airtable_errors(self, mock_validate, mock_airtable_get):
        """Test that Airtable errors are properly propagated."""
        # Arrange
        mock_config = {
            "AIRTABLE_API_KEY": "test_key",
            "AIRTABLE_VIEW_URL": "https://airtable.com/app123/tbl456/viw789",
        }
        mock_validate.return_value = mock_config
        mock_airtable_get.side_effect = Exception("Airtable API error")

        # Act & Assert
        with pytest.raises(Exception, match="Airtable API error"):
            gr.fetch()

    @patch("config.validate")
    def test_should_propagate_config_validation_errors(self, mock_validate):
        """Test that configuration validation errors are propagated."""
        # Arrange
        mock_validate.side_effect = SystemExit(1)

        # Act & Assert
        with pytest.raises(SystemExit):
            gr.fetch()


class TestGrProcess:
    """Test data processing functionality."""

    def test_should_process_family_name_arrays_to_abbreviations(self):
        """Test that Family name arrays are flattened and abbreviated."""
        # Arrange
        data = [
            {"Family name": ["Owen"], "Status": "active"},
            {"Family name": ["Jurado Traverso"], "Status": "pending"},
            {"Family name": ["Elizabeth"], "Status": "completed"},
        ]

        # Act
        result = gr.process(data)

        # Assert
        assert result[0]["Family name"] == "Owen"
        assert result[1]["Family name"] == "Jura" 
        assert result[2]["Family name"] == "Eliz"

    def test_should_handle_string_family_names(self):
        """Test that string Family names are processed correctly."""
        # Arrange
        data = [
            {"Family name": "SingleName", "Status": "active"},
            {"Family name": "Al", "Status": "pending"},
        ]

        # Act
        result = gr.process(data)

        # Assert
        assert result[0]["Family name"] == "Sing"
        assert result[1]["Family name"] == "Al"

    def test_should_preserve_non_family_name_fields(self):
        """Test that other fields are preserved unchanged."""
        # Arrange
        data = [
            {
                "Family name": ["Owen"],
                "Status": "active",
                "Email": "owen@example.com",
                "Complex": {"nested": "value"},
            }
        ]

        # Act
        result = gr.process(data)

        # Assert
        assert result[0]["Family name"] == "Owen"
        assert result[0]["Status"] == "active"
        assert result[0]["Email"] == "owen@example.com"
        assert result[0]["Complex"]["nested"] == "value"

    def test_should_handle_empty_data_gracefully(self):
        """Test processing of empty data list."""
        # Arrange
        data = []

        # Act
        result = gr.process(data)

        # Assert
        assert result == []

    def test_should_handle_none_input(self):
        """Test processing when None is passed as input."""
        # Arrange
        data = None

        # Act
        result = gr.process(data)

        # Assert
        assert result == []

    def test_should_handle_records_without_family_name(self):
        """Test processing records that don't have Family name field."""
        # Arrange
        data = [
            {"Name": "John", "Email": "john@example.com", "Status": "active"},
            {"Different": "structure"},
        ]

        # Act
        result = gr.process(data)

        # Assert
        assert len(result) == 2
        assert result[0]["Name"] == "John"
        assert result[1]["Different"] == "structure"


class TestGrFlattenArrayValue:
    """Test array flattening functionality."""

    def test_should_flatten_single_item_array(self):
        """Test flattening array with single item."""
        # Act
        result = gr.flatten_array_value(["Owen"])

        # Assert
        assert result == "Owen"

    def test_should_flatten_multi_item_array_using_first_element(self):
        """Test flattening array with multiple items."""
        # Act
        result = gr.flatten_array_value(["First", "Second", "Third"])

        # Assert
        assert result == "First"

    def test_should_pass_through_string_unchanged(self):
        """Test that strings pass through unchanged."""
        # Act
        result = gr.flatten_array_value("Already a string")

        # Assert
        assert result == "Already a string"

    def test_should_handle_empty_array(self):
        """Test handling of empty array."""
        # Act
        result = gr.flatten_array_value([])

        # Assert
        assert result == ""

    def test_should_handle_none_value(self):
        """Test handling of None value."""
        # Act
        result = gr.flatten_array_value(None)

        # Assert
        assert result == ""

    def test_should_convert_non_string_array_elements(self):
        """Test conversion of non-string array elements."""
        # Act
        result = gr.flatten_array_value([42])

        # Assert
        assert result == "42"


class TestGrAbbreviateName:
    """Test name abbreviation functionality."""

    def test_should_abbreviate_long_names_to_four_characters(self):
        """Test abbreviation of names longer than 4 characters."""
        # Act
        result = gr.abbreviate_name("Elizabeth")

        # Assert
        assert result == "Eliz"

    def test_should_return_short_names_unchanged(self):
        """Test that names 4 characters or shorter are unchanged."""
        # Arrange
        test_cases = ["Owen", "Al", "Jo", "Anne"]

        for name in test_cases:
            # Act
            result = gr.abbreviate_name(name)

            # Assert
            assert result == name

    def test_should_handle_empty_string(self):
        """Test handling of empty string."""
        # Act
        result = gr.abbreviate_name("")

        # Assert
        assert result == ""

    def test_should_handle_exactly_four_characters(self):
        """Test handling of names exactly 4 characters."""
        # Act
        result = gr.abbreviate_name("John")

        # Assert
        assert result == "John"


class TestGrDisplayData:
    """Test display data functionality."""

    @patch("display.print_table")
    @patch("commands.gr.parse_headers")
    @patch("commands.gr.parse_columns")
    @patch("config.validate")
    def test_should_display_table_with_parsed_config(
        self, mock_validate, mock_parse_columns, mock_parse_headers, mock_print_table
    ):
        """Test display with configuration parsing."""
        # Arrange
        mock_config = {
            "GR_COLUMNS": "Name,Email,Status",
            "GR_HEADERS": "Student Name,Email Address,Current Status",
        }
        data = [{"Name": "John", "Email": "john@example.com", "Status": "active"}]

        mock_validate.return_value = mock_config
        mock_parse_columns.return_value = ["Name", "Email", "Status"]
        mock_parse_headers.return_value = [
            "Student Name",
            "Email Address",
            "Current Status",
        ]

        # Act
        gr.display_data(data)

        # Assert
        mock_validate.assert_called_once()
        mock_parse_columns.assert_called_once_with("Name,Email,Status")
        mock_parse_headers.assert_called_once_with(
            "Student Name,Email Address,Current Status"
        )
        mock_print_table.assert_called_once_with(
            data,
            ["Name", "Email", "Status"],
            ["Student Name", "Email Address", "Current Status"],
        )

    @patch("display.print_table")
    @patch("config.validate")
    def test_should_handle_config_validation_errors(
        self, mock_validate, mock_print_table
    ):
        """Test error handling when configuration validation fails."""
        # Arrange
        mock_validate.side_effect = SystemExit(1)

        # Act & Assert
        with pytest.raises(SystemExit):
            gr.display_data([])


class TestGrParseColumns:
    """Test column parsing functionality."""

    def test_should_parse_comma_separated_columns(self):
        """Test parsing of comma-separated column names."""
        # Arrange
        columns_str = "Name,Email,Status,Date"

        # Act
        result = gr.parse_columns(columns_str)

        # Assert
        assert result == ["Name", "Email", "Status", "Date"]

    def test_should_handle_spaces_around_commas(self):
        """Test parsing with spaces around commas."""
        # Arrange
        columns_str = "Name, Email , Status ,Date"

        # Act
        result = gr.parse_columns(columns_str)

        # Assert
        assert result == ["Name", "Email", "Status", "Date"]

    def test_should_handle_empty_string(self):
        """Test parsing of empty string."""
        # Arrange
        columns_str = ""

        # Act
        result = gr.parse_columns(columns_str)

        # Assert
        assert result == []

    def test_should_filter_out_empty_columns(self):
        """Test filtering out empty column names."""
        # Arrange
        columns_str = "Name,,Email, ,Status"

        # Act
        result = gr.parse_columns(columns_str)

        # Assert
        assert result == ["Name", "Email", "Status"]

    def test_should_handle_single_column(self):
        """Test parsing of single column."""
        # Arrange
        columns_str = "Name"

        # Act
        result = gr.parse_columns(columns_str)

        # Assert
        assert result == ["Name"]

    def test_should_handle_trailing_comma(self):
        """Test parsing with trailing comma."""
        # Arrange
        columns_str = "Name,Email,Status,"

        # Act
        result = gr.parse_columns(columns_str)

        # Assert
        assert result == ["Name", "Email", "Status"]


class TestGrParseHeaders:
    """Test header parsing functionality."""

    def test_should_parse_comma_separated_headers(self):
        """Test parsing of comma-separated header names."""
        # Arrange
        headers_str = "Student Name,Email Address,Current Status,Last Updated"

        # Act
        result = gr.parse_headers(headers_str)

        # Assert
        assert result == [
            "Student Name",
            "Email Address",
            "Current Status",
            "Last Updated",
        ]

    def test_should_handle_spaces_around_commas(self):
        """Test parsing with spaces around commas."""
        # Arrange
        headers_str = "Student Name, Email Address , Current Status ,Last Updated"

        # Act
        result = gr.parse_headers(headers_str)

        # Assert
        assert result == [
            "Student Name",
            "Email Address",
            "Current Status",
            "Last Updated",
        ]

    def test_should_handle_empty_string(self):
        """Test parsing of empty string."""
        # Arrange
        headers_str = ""

        # Act
        result = gr.parse_headers(headers_str)

        # Assert
        assert result == []

    def test_should_filter_out_empty_headers(self):
        """Test filtering out empty header names."""
        # Arrange
        headers_str = "Name,,Email, ,Status"

        # Act
        result = gr.parse_headers(headers_str)

        # Assert
        assert result == ["Name", "Email", "Status"]

    def test_should_preserve_header_spaces(self):
        """Test that spaces within headers are preserved."""
        # Arrange
        headers_str = "Full Name,Email Address,Account Status"

        # Act
        result = gr.parse_headers(headers_str)

        # Assert
        assert result == ["Full Name", "Email Address", "Account Status"]


class TestGrIntegration:
    """Integration tests for gr command."""

    @patch("sources.airtable.get")
    @patch("display.print_table")
    @patch("config.validate")
    def test_should_handle_complete_workflow_with_real_structure(
        self, mock_validate, mock_print_table, mock_airtable_get
    ):
        """Test complete gr workflow with realistic data structure."""
        # Arrange
        mock_config = {
            "AIRTABLE_API_KEY": "test_key",
            "AIRTABLE_VIEW_URL": "https://airtable.com/app123/tbl456/viw789",
            "GR_COLUMNS": "Name,Email,Status",
            "GR_HEADERS": "Student Name,Email Address,Current Status",
        }
        mock_data = [
            {"Name": "John Doe", "Email": "john@example.com", "Status": "active"},
            {"Name": "Jane Smith", "Email": "jane@example.com", "Status": "pending"},
        ]

        mock_validate.return_value = mock_config
        mock_airtable_get.return_value = mock_data

        # Act - should execute without errors
        with patch("display.print_info"), patch("display.print_success"):
            gr.run([])

        # Assert
        mock_airtable_get.assert_called_once_with(
            "test_key", "https://airtable.com/app123/tbl456/viw789"
        )
        mock_print_table.assert_called_once_with(
            mock_data,
            ["Name", "Email", "Status"],
            ["Student Name", "Email Address", "Current Status"],
        )
