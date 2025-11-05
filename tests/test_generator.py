"""Tests for project generator."""

import os
import subprocess
from pathlib import Path

import pytest

from create_fastapi_boilerplate.generator import FastAPIProjectGenerator


class TestProjectNameValidation:
    """Test project name validation."""

    def test_valid_project_name(self, valid_project_name: str) -> None:
        """Test valid project name."""
        generator = FastAPIProjectGenerator(valid_project_name)
        assert generator.validate_project_name() is True

    def test_invalid_project_names(self, invalid_project_names: list[str]) -> None:
        """Test invalid project names."""
        for name in invalid_project_names:
            generator = FastAPIProjectGenerator(name)
            assert generator.validate_project_name() is False

    def test_project_name_with_underscore(self) -> None:
        """Test project name with underscore."""
        generator = FastAPIProjectGenerator("test_project")
        assert generator.validate_project_name() is True

    def test_project_name_with_hyphen(self) -> None:
        """Test project name with hyphen."""
        generator = FastAPIProjectGenerator("test-project")
        assert generator.validate_project_name() is True


class TestDirectoryOperations:
    """Test directory operations."""

    def test_check_directory_not_exists(
        self, temp_dir: Path, valid_project_name: str
    ) -> None:
        """Test check when directory doesn't exist."""
        generator = FastAPIProjectGenerator(
            valid_project_name, output_dir=str(temp_dir)
        )
        assert generator.check_directory_exists() is True

    def test_project_path_creation(
        self, temp_dir: Path, valid_project_name: str
    ) -> None:
        """Test project path is created correctly."""
        generator = FastAPIProjectGenerator(
            valid_project_name, output_dir=str(temp_dir)
        )
        expected_path = temp_dir / valid_project_name
        assert generator.project_path == expected_path


class TestPrerequisites:
    """Test prerequisite checks."""

    def test_git_available(self, valid_project_name: str) -> None:
        """Test git is available."""
        generator = FastAPIProjectGenerator(valid_project_name)
        # This should pass on CI/CD and dev machines
        assert generator.check_prerequisites() is True


@pytest.mark.slow
class TestProjectGeneration:
    """Test project generation (requires internet for cloning)."""

    def test_generate_project_basic(
        self, temp_dir: Path, valid_project_name: str
    ) -> None:
        """Test basic project generation."""
        generator = FastAPIProjectGenerator(
            valid_project_name,
            output_dir=str(temp_dir),
            init_git=False,
            install_deps=False,
        )
        
        success = generator.generate()
        assert success is True
        
        # Check project directory exists
        project_path = temp_dir / valid_project_name
        assert project_path.exists()
        
        # Check essential files exist
        essential_files = [
            "pyproject.toml",
            "README.md",
            "Dockerfile",
            "docker-compose.yml",
            ".env",
            ".env.example",
            "Makefile",
            "app/main.py",
            "app/core/config.py",
        ]
        
        for file in essential_files:
            file_path = project_path / file
            assert file_path.exists(), f"Missing file: {file}"

    def test_project_customization(
        self, temp_dir: Path, valid_project_name: str
    ) -> None:
        """Test project files are customized with project name."""
        generator = FastAPIProjectGenerator(
            valid_project_name,
            output_dir=str(temp_dir),
            init_git=False,
            install_deps=False,
        )
        
        success = generator.generate()
        assert success is True, "Project generation failed"
        
        project_path = temp_dir / valid_project_name
        assert project_path.exists(), "Project path does not exist"
        
        # Check pyproject.toml is customized
        pyproject_path = project_path / "pyproject.toml"
        assert pyproject_path.exists(), "pyproject.toml not found"
        pyproject_content = pyproject_path.read_text()
        assert f'name = "{valid_project_name}"' in pyproject_content
        
        # Check docker-compose.yml is customized
        compose_path = project_path / "docker-compose.yml"
        assert compose_path.exists(), "docker-compose.yml not found"
        compose_content = compose_path.read_text()
        assert f"container_name: {valid_project_name}_postgres" in compose_content
        
        # Check .env is created with JWT secret
        env_path = project_path / ".env"
        assert env_path.exists(), ".env file not found"
        env_content = env_path.read_text()
        assert "JWT_SECRET_KEY=" in env_content
        assert "JWT_SECRET_KEY=your-super-secret-jwt-key" not in env_content

    def test_git_initialization(
        self, temp_dir: Path, valid_project_name: str
    ) -> None:
        """Test git is initialized correctly."""
        generator = FastAPIProjectGenerator(
            valid_project_name,
            output_dir=str(temp_dir),
            init_git=True,
            install_deps=False,
        )
        
        success = generator.generate()
        assert success is True, "Project generation failed"
        
        project_path = temp_dir / valid_project_name
        
        # Check .git directory exists
        git_dir = project_path / ".git"
        assert git_dir.exists()
        
        # Check initial commit exists
        original_dir = os.getcwd()
        try:
            os.chdir(project_path)
            result = subprocess.run(
                ["git", "log", "--oneline"],
                capture_output=True,
                text=True,
            )
            assert "Initial commit from create-fastapi-boilerplate" in result.stdout
        finally:
            os.chdir(original_dir)


@pytest.mark.slow
class TestFileCustomization:
    """Test specific file customizations."""

    def test_env_file_has_unique_jwt_secret(
        self, temp_dir: Path
    ) -> None:
        """Test .env file gets unique JWT secret."""
        # Generate two projects
        gen1 = FastAPIProjectGenerator(
            "project1",
            output_dir=str(temp_dir),
            init_git=False,
            install_deps=False,
        )
        success1 = gen1.generate()
        assert success1 is True, "First project generation failed"
        
        gen2 = FastAPIProjectGenerator(
            "project2",
            output_dir=str(temp_dir),
            init_git=False,
            install_deps=False,
        )
        success2 = gen2.generate()
        assert success2 is True, "Second project generation failed"
        
        # Get JWT secrets
        env1_path = temp_dir / "project1" / ".env"
        env2_path = temp_dir / "project2" / ".env"
        
        assert env1_path.exists(), "project1/.env not found"
        assert env2_path.exists(), "project2/.env not found"
        
        env1 = env1_path.read_text()
        env2 = env2_path.read_text()
        
        secret1 = [line for line in env1.split("\n") if "JWT_SECRET_KEY=" in line][0]
        secret2 = [line for line in env2.split("\n") if "JWT_SECRET_KEY=" in line][0]
        
        # Secrets should be different
        assert secret1 != secret2

    def test_readme_customization(
        self, temp_dir: Path, valid_project_name: str
    ) -> None:
        """Test README is customized."""
        generator = FastAPIProjectGenerator(
            valid_project_name,
            output_dir=str(temp_dir),
            init_git=False,
            install_deps=False,
        )
        
        success = generator.generate()
        assert success is True, "Project generation failed"
        
        project_path = temp_dir / valid_project_name
        readme_path = project_path / "README.md"
        
        assert readme_path.exists(), "README.md not found"
        readme_content = readme_path.read_text()
        
        # Should contain project name
        assert valid_project_name in readme_content.lower()