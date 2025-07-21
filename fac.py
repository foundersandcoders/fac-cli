#!/usr/bin/env python3
"""FAC CLI - Command line interface for Founders and Coders training operations."""

import sys
from typing import List, Tuple

import config


def parse(args: List[str]) -> Tuple[str, List[str]]:
    """Parse command line arguments."""
    if len(args) < 2:
        return "help", []

    command = args[1]
    remaining_args = args[2:] if len(args) > 2 else []

    return command, remaining_args


def route(args: List[str]) -> None:
    """Route command to appropriate handler."""
    command, cmd_args = parse(args)
    dispatch(command, cmd_args)


def dispatch(command: str, args: List[str]) -> None:
    """Dispatch to command handler."""
    # Help commands don't need configuration validation
    help_commands = ["help", "--help", "-h"]

    if command in help_commands:
        show_help()
        return

    commands = {
        "gr": lambda: run_gr(args),
    }

    if command in commands:
        try:
            # Validate configuration for commands that need it
            config.validate()
            commands[command]()
        except KeyboardInterrupt:
            print("\nOperation cancelled by user", file=sys.stderr)
            sys.exit(130)
        except Exception as e:
            if config.get("FAC_CLI_DEBUG", "false").lower() == "true":
                raise
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        show_error(f"Unknown command: {command}")


def run_gr(args: List[str]) -> None:
    """Run gateway recent command."""
    try:
        from commands import gr

        gr.run(args)
    except ImportError:
        config.error("Gateway recent command module not found")


def show_help() -> None:
    """Show help information."""
    help_text = """
FAC CLI - Founders and Coders Training Operations

Usage:
  ./fac.py <command> [options]

Available commands:
  gr              Gateway recent - fetch and display recent gateway data
  help, --help    Show this help message

Examples:
  ./fac.py gr     Display recent gateway data from Airtable
  ./fac.py help   Show this help message

Configuration:
  Copy .env.example to .env and configure your Airtable credentials.

For more information, see README.md
"""
    print(help_text.strip())


def show_error(message: str) -> None:
    """Show error message and help."""
    print(f"Error: {message}", file=sys.stderr)
    print("Use './fac.py help' for usage information", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    """Main entry point."""
    route(sys.argv)


if __name__ == "__main__":
    main()
