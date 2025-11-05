"""Pytest configuration and fixtures."""

import shutil
import tempfile
from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture()
def temp_dir() -> Generator[Path, None, None]:
    """Create temporary directory for tests."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    # Cleanup
    if temp_path.exists():
        shutil.rmtree(temp_path)


@pytest.fixture()
def valid_project_name() -> str:
    """Valid project name for testing."""
    return "test-project"


@pytest.fixture()
def invalid_project_names() -> list[str]:
    """Invalid project names for testing."""
    return [
        "Test-Project",  # Capital letter
        "123-project",   # Starts with number
        "test project",  # Contains space
        "test@project",  # Invalid character
        "",              # Empty
        "a" * 51,        # Too long
    ]