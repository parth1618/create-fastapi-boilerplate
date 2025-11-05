"""Integration tests."""

import os
import subprocess
from pathlib import Path

import pytest


@pytest.mark.slow
@pytest.mark.integration
class TestFullGeneration:
    """Test complete project generation flow."""

    def test_generate_and_verify_structure(
        self, temp_dir: Path
    ) -> None:
        """Test generating project and verifying structure."""
        project_name = "integration-test"
        
        # Ensure temp directory exists and is accessible
        assert temp_dir.exists(), f"Temp directory {temp_dir} does not exist"
        
        # Change to temp directory to ensure we have a valid working directory
        original_dir = os.getcwd()
        try:
            os.chdir(temp_dir)
            
            # Generate project
            result = subprocess.run(
                [
                    "create-fastapi-boilerplate",
                    project_name,
                    "--output-dir", str(temp_dir),
                    "--no-git",
                    "--no-install",
                ],
                capture_output=True,
                text=True,
                cwd=str(temp_dir),  # Explicitly set working directory
            )
            
            assert result.returncode == 0, f"Generation failed: {result.stdout}\n{result.stderr}"
            
            project_path = temp_dir / project_name
            assert project_path.exists()
            
            # Check directory structure
            expected_dirs = [
                "app",
                "app/api",
                "app/core",
                "app/models",
                "app/schemas",
                "app/services",
                "tests",
                "migrations",
            ]
            
            for dir_name in expected_dirs:
                dir_path = project_path / dir_name
                assert dir_path.exists(), f"Missing directory: {dir_name}"
        finally:
            os.chdir(original_dir)

    @pytest.mark.skip(reason="Requires Docker")
    def test_generated_project_can_start(
        self, temp_dir: Path
    ) -> None:
        """Test generated project can start with Docker."""
        project_name = "start-test"
        
        # Generate project
        subprocess.run(
            [
                "create-fastapi-boilerplate",
                project_name,
                "--output-dir", str(temp_dir),
                "--no-git",
            ],
            check=True,
        )
        
        project_path = temp_dir / project_name
        
        # Try to start with Docker Compose
        result = subprocess.run(
            ["docker-compose", "up", "-d"],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=60,
        )
        
        assert result.returncode == 0
        
        # Cleanup
        subprocess.run(
            ["docker-compose", "down"],
            cwd=project_path,
            capture_output=True,
        )