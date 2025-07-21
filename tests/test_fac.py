"""Tests for main FAC CLI module."""

import pytest
import sys
from unittest.mock import patch, Mock
from io import StringIO

# Add parent directory to path for imports
sys.path.insert(0, "..")

import fac


class TestFacParse:
    """Test command line argument parsing."""

    def test_should_return_help_command_for_no_arguments(self):
        """Test that no arguments returns help command."""
        # Arrange
        args = ["fac.py"]

        # Act
        command, cmd_args = fac.parse(args)

        # Assert
        assert command == "help"
        assert cmd_args == []

    def test_should_return_help_command_for_single_argument(self):
        """Test that single argument (script name) returns help."""
        # Arrange
        args = ["fac.py"]

        # Act
        command, cmd_args = fac.parse(args)

        # Assert
        assert command == "help"
        assert cmd_args == []

    def test_should_parse_command_without_arguments(self):
        """Test parsing command without additional arguments."""
        # Arrange
        args = ["fac.py", "gr"]

        # Act
        command, cmd_args = fac.parse(args)

        # Assert
        assert command == "gr"
        assert cmd_args == []

    def test_should_parse_command_with_arguments(self):
        """Test parsing command with additional arguments."""
        # Arrange
        args = ["fac.py", "gr", "--verbose", "--limit", "10"]

        # Act
        command, cmd_args = fac.parse(args)

        # Assert
        assert command == "gr"
        assert cmd_args == ["--verbose", "--limit", "10"]

    def test_should_handle_help_flags(self):
        """Test parsing of help flags as commands."""
        # Test cases for different help variations
        help_variations = ["help", "--help", "-h"]

        for help_flag in help_variations:
            # Arrange
            args = ["fac.py", help_flag]

            # Act
            command, cmd_args = fac.parse(args)

            # Assert
            assert command == help_flag
            assert cmd_args == []


class TestFacRoute:
    """Test command routing functionality."""

    @patch("fac.dispatch")
    def test_should_route_to_dispatch_with_parsed_args(self, mock_dispatch):
        """Test that route calls dispatch with parsed arguments."""
        # Arrange
        args = ["fac.py", "gr", "--verbose"]

        # Act
        fac.route(args)

        # Assert
        mock_dispatch.assert_called_once_with("gr", ["--verbose"])

    @patch("fac.parse")
    @patch("fac.dispatch")
    def test_should_use_parse_function_for_argument_processing(
        self, mock_dispatch, mock_parse
    ):
        """Test that route uses parse function for processing arguments."""
        # Arrange
        args = ["fac.py", "test_command"]
        mock_parse.return_value = ("test_command", [])

        # Act
        fac.route(args)

        # Assert
        mock_parse.assert_called_once_with(args)
        mock_dispatch.assert_called_once_with("test_command", [])


class TestFacDispatch:
    """Test command dispatch functionality."""

    @patch("fac.show_help")
    def test_should_show_help_for_help_command(self, mock_show_help):
        """Test that help commands show help without validation."""
        # Test all help command variations
        help_commands = ["help", "--help", "-h"]

        for help_cmd in help_commands:
            mock_show_help.reset_mock()

            # Act
            fac.dispatch(help_cmd, [])

            # Assert
            mock_show_help.assert_called_once()

    @patch("config.validate")
    @patch("fac.run_gr")
    def test_should_execute_gr_command_with_validation(
        self, mock_run_gr, mock_validate
    ):
        """Test that gr command is executed with configuration validation."""
        # Arrange
        mock_validate.return_value = {"AIRTABLE_API_KEY": "test"}

        # Act
        fac.dispatch("gr", ["--verbose"])

        # Assert
        mock_validate.assert_called_once()
        mock_run_gr.assert_called_once_with(["--verbose"])

    @patch("fac.show_error")
    def test_should_show_error_for_unknown_command(self, mock_show_error):
        """Test that unknown commands show error."""
        # Act
        fac.dispatch("unknown_command", [])

        # Assert
        mock_show_error.assert_called_once_with("Unknown command: unknown_command")

    @patch("config.validate")
    @patch("fac.run_gr")
    @patch("builtins.print")
    def test_should_handle_keyboard_interrupt_gracefully(
        self, mock_print, mock_run_gr, mock_validate
    ):
        """Test handling of KeyboardInterrupt (Ctrl+C)."""
        # Arrange
        mock_validate.return_value = {"AIRTABLE_API_KEY": "test"}
        mock_run_gr.side_effect = KeyboardInterrupt()

        # Act & Assert
        with pytest.raises(SystemExit) as exit_info:
            fac.dispatch("gr", [])

        assert exit_info.value.code == 130
        mock_print.assert_called_once_with(
            "\nOperation cancelled by user", file=sys.stderr
        )

    @patch("config.validate")
    @patch("fac.run_gr")
    @patch("builtins.print")
    def test_should_handle_general_exceptions_in_non_debug_mode(
        self, mock_print, mock_run_gr, mock_validate
    ):
        """Test handling of general exceptions in non-debug mode."""
        # Arrange
        mock_validate.return_value = {"AIRTABLE_API_KEY": "test"}
        mock_run_gr.side_effect = Exception("Test error")

        with patch("config.get", return_value="false"):
            # Act & Assert
            with pytest.raises(SystemExit) as exit_info:
                fac.dispatch("gr", [])

        assert exit_info.value.code == 1
        mock_print.assert_called_once_with("Error: Test error", file=sys.stderr)

    @patch("config.validate")
    @patch("fac.run_gr")
    def test_should_reraise_exceptions_in_debug_mode(self, mock_run_gr, mock_validate):
        """Test that exceptions are re-raised in debug mode."""
        # Arrange
        mock_validate.return_value = {"AIRTABLE_API_KEY": "test"}
        mock_run_gr.side_effect = ValueError("Debug test error")

        with patch("config.get", return_value="true"):
            # Act & Assert
            with pytest.raises(ValueError, match="Debug test error"):
                fac.dispatch("gr", [])


class TestFacRunGr:
    """Test gr command execution."""

    @patch("commands.gr.run")
    def test_should_import_and_execute_gr_command(self, mock_gr_run):
        """Test that gr command is imported and executed correctly."""
        # Arrange
        args = ["--verbose", "--limit", "10"]

        # Act
        fac.run_gr(args)

        # Assert
        mock_gr_run.assert_called_once_with(args)

    @patch("config.error")
    def test_should_handle_import_error_gracefully(self, mock_config_error):
        """Test handling when gr module cannot be imported."""
        # Arrange
        with patch("builtins.__import__", side_effect=ImportError("Module not found")):
            # Act
            fac.run_gr([])

        # Assert
        mock_config_error.assert_called_once_with(
            "Gateway recent command module not found"
        )


class TestFacShowHelp:
    """Test help display functionality."""

    @patch("builtins.print")
    def test_should_display_complete_help_text(self, mock_print):
        """Test that complete help text is displayed."""
        # Act
        fac.show_help()

        # Assert
        mock_print.assert_called_once()
        help_text = mock_print.call_args[0][0]

        # Verify key elements are in help text
        assert "FAC CLI - Founders and Coders Training Operations" in help_text
        assert "Usage:" in help_text
        assert "gr" in help_text
        assert "Gateway recent" in help_text
        assert "help" in help_text
        assert "Examples:" in help_text
        assert "Configuration:" in help_text
        assert ".env" in help_text

    @patch("builtins.print")
    def test_should_include_all_available_commands(self, mock_print):
        """Test that all available commands are shown in help."""
        # Act
        fac.show_help()

        # Assert
        help_text = mock_print.call_args[0][0]

        # Check for gr command documentation
        assert "gr" in help_text
        assert "Gateway recent" in help_text
        assert "fetch and display recent gateway data" in help_text

        # Check for help command documentation
        assert "help, --help" in help_text
        assert "Show this help message" in help_text


class TestFacShowError:
    """Test error display functionality."""

    @patch("builtins.print")
    def test_should_print_error_message_to_stderr(self, mock_print):
        """Test that error message is printed to stderr."""
        # Act & Assert
        with pytest.raises(SystemExit) as exit_info:
            fac.show_error("Test error message")

        # Assert exit code
        assert exit_info.value.code == 1

        # Assert print calls - should be 2 calls (error message and help tip)
        assert mock_print.call_count == 2

        # Check first call (error message)
        first_call = mock_print.call_args_list[0]
        assert first_call[0][0] == "Error: Test error message"
        assert first_call[1]["file"] == sys.stderr

        # Check second call (help tip)
        second_call = mock_print.call_args_list[1]
        assert "Use './fac.py help' for usage information" in second_call[0][0]
        assert second_call[1]["file"] == sys.stderr


class TestFacMain:
    """Test main entry point functionality."""

    @patch("fac.route")
    @patch("sys.argv", ["fac.py", "gr"])
    def test_should_call_route_with_sys_argv(self, mock_route):
        """Test that main calls route with sys.argv."""
        # Act
        fac.main()

        # Assert
        mock_route.assert_called_once_with(["fac.py", "gr"])

    @patch("fac.route")
    def test_should_handle_route_exceptions(self, mock_route):
        """Test that main handles exceptions from route."""
        # Arrange - route should handle its own exceptions and exit gracefully
        mock_route.side_effect = SystemExit(1)  # Route exits on error

        # Act & Assert - should propagate SystemExit from route
        with patch("sys.argv", ["fac.py", "test"]):
            with pytest.raises(SystemExit) as exit_info:
                fac.main()
            assert exit_info.value.code == 1


class TestFacIntegration:
    """Integration tests for main CLI functionality."""

    @patch("commands.gr.run")
    @patch("config.validate")
    def test_should_execute_complete_gr_command_workflow(
        self, mock_validate, mock_gr_run
    ):
        """Test complete workflow for gr command execution."""
        # Arrange
        mock_validate.return_value = {
            "AIRTABLE_API_KEY": "test_key",
            "AIRTABLE_VIEW_URL": "https://airtable.com/app123/tbl456/viw789",
        }

        # Act
        fac.route(["fac.py", "gr", "--verbose"])

        # Assert
        mock_validate.assert_called_once()
        mock_gr_run.assert_called_once_with(["--verbose"])

    @patch("fac.show_help")
    def test_should_show_help_for_various_help_requests(self, mock_show_help):
        """Test that various help requests all show help."""
        help_requests = [
            ["fac.py"],
            ["fac.py", "help"],
            ["fac.py", "--help"],
            ["fac.py", "-h"],
        ]

        for args in help_requests:
            mock_show_help.reset_mock()

            # Act
            fac.route(args)

            # Assert
            mock_show_help.assert_called_once()

    @patch("builtins.print")
    def test_should_handle_error_cases_appropriately(self, mock_print):
        """Test error handling for various error conditions."""
        # Test unknown command
        with pytest.raises(SystemExit):
            fac.route(["fac.py", "unknown_command"])

        # Verify error message was printed
        assert any(
            "Unknown command: unknown_command" in str(call)
            for call in mock_print.call_args_list
        )
