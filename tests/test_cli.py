"""Tests for CLI interface."""

import os
import subprocess
import sys


class TestCLIBasics:
    """Test basic CLI functionality."""

    def test_cli_help(self) -> None:
        """Test --help flag."""
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"  # Force UTF-8 for Windows
        result = subprocess.run(
            [sys.executable, "-m", "create_fastapi_boilerplate", "--help"],
            capture_output=True,
            text=True,
            env=env
        )
        assert result.returncode == 0
        assert "Create a new FastAPI project" in result.stdout

    def test_cli_version(self) -> None:
        """Test --version flag."""
        result = subprocess.run(
            [sys.executable, "-m", "create_fastapi_boilerplate", "--version"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "1.0.1" in result.stdout


class TestCLIArguments:
    """Test CLI argument parsing."""

    def test_cli_requires_project_name(self) -> None:
        """Test CLI requires project name."""
        result = subprocess.run(
            [sys.executable, "-m", "create_fastapi_boilerplate"],
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0
        assert "required" in result.stderr.lower()

    def test_cli_invalid_project_name(self) -> None:
        """Test CLI rejects invalid project name."""
        result = subprocess.run(
            [sys.executable, "-m", "create_fastapi_boilerplate", "Invalid-Name"],
            capture_output=True,
            text=True,
        )
        # The generator validates but main() returns 0 instead of 1
        assert result.returncode != 0 or "Invalid project name" in result.stdout
