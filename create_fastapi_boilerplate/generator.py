"""Project generator for FastAPI boilerplate."""

import os
import re
import secrets
import shutil
import subprocess
from pathlib import Path
from typing import Optional


class FastAPIProjectGenerator:
    """Generator for FastAPI boilerplate projects."""

    TEMPLATE_REPO = "https://github.com/parth1618/fastapi-boilerplate"
    
    def __init__(
        self,
        project_name: str,
        output_dir: Optional[str] = None,
        init_git: bool = True,
        install_deps: bool = False
    ):
        self.project_name = project_name
        self.output_dir = Path(output_dir) if output_dir else Path.cwd()
        self.project_path = self.output_dir / project_name
        self.init_git = init_git
        self.install_deps = install_deps
        
    def validate_project_name(self) -> bool:
        """Validate project name follows conventions."""
        if not re.match(r'^[a-z][a-z0-9_-]*$', self.project_name):
            self._error(
                f"Invalid project name: '{self.project_name}'",
                "Project name must:",
                "- Start with a lowercase letter",
                "- Contain only lowercase letters, numbers, hyphens, and underscores"
            )
            return False
        
        if len(self.project_name) > 50:
            self._error("Project name too long (max 50 characters)")
            return False
            
        return True
    
    def check_prerequisites(self) -> bool:
        """Check if required tools are installed."""
        required_tools = ["git"]
        missing_tools = []
        
        for tool in required_tools:
            if not shutil.which(tool):
                missing_tools.append(tool)
        
        if missing_tools:
            self._error(
                "Missing required tools:",
                *[f"- {tool}" for tool in missing_tools],
                "",
                "Please install them and try again."
            )
            return False
        
        return True
    
    def check_directory_exists(self) -> bool:
        """Check if project directory already exists."""
        if self.project_path.exists():
            self._warning(f"Directory '{self.project_name}' already exists!")
            response = input("   Delete and continue? (y/N): ").strip().lower()
            if response == 'y':
                try:
                    shutil.rmtree(self.project_path)
                    self._success("Old directory removed")
                    return True
                except Exception as e:
                    self._error(f"Failed to remove directory: {e}")
                    return False
            return False
        return True
    
    def clone_template(self) -> bool:
        """Clone the template repository."""
        self._info("Cloning FastAPI boilerplate template...")
        
        try:
            # Clone with depth 1 for faster cloning
            result = subprocess.run(
                [
                    "git", "clone",
                    "--depth", "1",
                    "--single-branch",
                    "--branch", "master",
                    self.TEMPLATE_REPO,
                    str(self.project_path)
                ],
                check=True,
                capture_output=True,
                text=True
            )
            
            # Remove .git directory to start fresh
            git_dir = self.project_path / ".git"
            if git_dir.exists():
                shutil.rmtree(git_dir)
            
            self._success("Template cloned successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            self._error(
                "Failed to clone template",
                f"Error: {e.stderr}",
                "",
                "Please check your internet connection and try again."
            )
            return False
        except Exception as e:
            self._error(f"Unexpected error: {e}")
            return False
    
    def customize_project(self) -> None:
        """Customize project files."""
        self._info(f"Customizing project for '{self.project_name}'...")
        
        # Generate secure JWT secret
        jwt_secret = secrets.token_urlsafe(32)
        
        # Define customizations
        customizations = {
            'pyproject.toml': [
                ('name = "fastapi-boilerplate"', f'name = "{self.project_name}"'),
                ('description = "Production-ready FastAPI backend boilerplate"', 
                 f'description = "{self.project_name} - FastAPI application"'),
                 ('"Parth Joshi <parthjoshi.1618@gmail.com>"', '"Your Name <youremail@example.com>"')
            ],
            'docker-compose.yml': [
                ('container_name: fastapi_postgres', f'container_name: {self.project_name}_postgres'),
                ('container_name: fastapi_redis', f'container_name: {self.project_name}_redis'),
                ('container_name: fastapi_jaeger', f'container_name: {self.project_name}_jaeger'),
                ('container_name: fastapi_otel_collector', f'container_name: {self.project_name}_otel_collector'),
                ('container_name: fastapi_prometheus', f'container_name: {self.project_name}_prometheus'),
            ],
            'Dockerfile': [
                ('fastapi-boilerplate', self.project_name),
            ],
            '.env.example': [
                ('JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production', 
                 f'JWT_SECRET_KEY={jwt_secret}'),
                 ('OTEL_SERVICE_NAME=fastapi-boilerplate', f'OTEL_SERVICE_NAME={self.project_name}'),
            ],
            'README.md': [
                ('FastAPI Boilerplate', f'{self.project_name.replace("-", " ").title()}'),
                ('fastapi-boilerplate', self.project_name),
                ('parth1618', 'your-username'),
                ('Parth Joshi', 'Your Name'),
                ('parthjoshi.1618@gmail.com', 'youremail@example.com'),
            ],
            'SETUP.md': [
                ('FastAPI Boilerplate', f'{self.project_name.replace("-", " ").title()}'),
                ('fastapi-boilerplate', self.project_name),
                ('parth1618', 'your-username'),
            ],
            'CONTRIBUTING.md': [
                ('FastAPI Boilerplate', f'{self.project_name.replace("-", " ").title()}'),
                ('fastapi-boilerplate', self.project_name),
                ('parth1618', 'your-username'),
            ],
            'app/core/config.py': [
                ('PROJECT_NAME: str = "FastAPI Boilerplate"', 
                 f'PROJECT_NAME: str = "{self.project_name.replace("-", " ").title()}"'),
                 ('OTEL_SERVICE_NAME: str = "fastapi-boilerplate"', 
                 f'OTEL_SERVICE_NAME: str = "{self.project_name}"'),
            ],
            'app/main.py': [
                ('"Welcome to FastAPI Boilerplate"', f'"Welcome to {self.project_name.replace("-", " ").title()}"'),
            ],
            '.github/workflows/ci.yml': [
                ('FastAPI Boilerplate', f'{self.project_name.replace("-", " ").title()}'),
                ('fastapi-boilerplate', self.project_name),
            ],
            'LICENSE': [
                ('FastAPI Boilerplate', f'{self.project_name.replace("-", " ").title()}'),
            ],
        }
        
        # Apply customizations
        for file_path, replacements in customizations.items():
            full_path = self.project_path / file_path
            if full_path.exists():
                content = full_path.read_text(encoding='utf-8')
                for old, new in replacements:
                    content = content.replace(old, new)
                full_path.write_text(content, encoding='utf-8')
        
        # Create .env file from template
        env_example = self.project_path / ".env.example"
        env_file = self.project_path / ".env"
        if env_example.exists():
            shutil.copy(env_example, env_file)
            self._success("Created .env file with secure JWT secret")
        
        self._success("Project customized successfully")
    
    def setup_git(self) -> None:
        """Initialize git repository."""
        if not self.init_git:
            return
            
        self._info("Initializing git repository...")
        
        original_dir = os.getcwd()
        try:
            os.chdir(self.project_path)
            
            subprocess.run(["git", "init"], check=True, capture_output=True)
            subprocess.run(["git", "add", "."], check=True, capture_output=True)
            subprocess.run(
                ["git", "commit", "-m", "Initial commit from create-fastapi-boilerplate"],
                check=True,
                capture_output=True
            )
            
            self._success("Git repository initialized")
            
        except subprocess.CalledProcessError:
            self._warning("Git initialization failed (continuing anyway)")
        finally:
            os.chdir(original_dir)
    
    def install_dependencies(self) -> None:
        """Install project dependencies."""
        if not self.install_deps:
            return
            
        self._info("Installing dependencies (this may take a few minutes)...")
        
        original_dir = os.getcwd()
        try:
            os.chdir(self.project_path)
            
            # Check if poetry is installed
            if shutil.which("poetry"):
                subprocess.run(
                    ["poetry", "install"],
                    check=True,
                    capture_output=True
                )
                self._success("Dependencies installed successfully")
            else:
                self._warning(
                    "Poetry not found. Skipping dependency installation.",
                    "Install Poetry: https://python-poetry.org/docs/#installation",
                    "Then run: cd {} && poetry install".format(self.project_name)
                )
                
        except subprocess.CalledProcessError as e:
            self._warning("Dependency installation failed (continuing anyway)")
        finally:
            os.chdir(original_dir)
    
    def print_next_steps(self) -> None:
        """Print next steps."""
        print("\n" + "=" * 70)
        print(f"🎉 Success! Created {self.project_name} at {self.project_path}")
        print("=" * 70)
        
        print("\n📚 Next steps:\n")
        print(f"   cd {self.project_name}")
        print()
        
        if not self.install_deps:
            print("   # Install dependencies")
            print("   make install")
            print()
        
        print("   # Start services with Docker (Recommended)")
        print("   make compose-up")
        print()
        print("   # OR run locally")
        print("   make migrate  # Run database migrations")
        print("   make dev      # Start development server")
        print()
        print("   # Run tests")
        print("   make test")
        
        print("\n📖 Documentation:")
        print("   - README.md - Complete documentation")
        print("   - SETUP.md - Detailed setup guide")
        print("   - CONTRIBUTING.md - Contribution guidelines")
        
        print("\n🌐 Access your app:")
        print("   - API: http://localhost:8000")
        print("   - Docs: http://localhost:8000/docs")
        print("   - ReDoc: http://localhost:8000/redoc")
        
        print("\n🔐 Default credentials (change in production!):")
        print("   Email: admin@example.com")
        print("   Password: admin123")
        
        print("\n💡 Pro tips:")
        print("   - Update .env with your configuration")
        print("   - Run 'make help' to see all available commands")
        print("   - Install pre-commit hooks: make precommit-install")
        print("   - Check CI/CD pipeline in .github/workflows/")
        
        print("\n⭐ Star the template repo:")
        print("   https://github.com/parth1618/fastapi-boilerplate")
        
        print("\nHappy coding! 🚀\n")
    
    def generate(self) -> bool:
        """Main generation workflow."""
        self._print_banner()
        
        # Validation
        if not self.validate_project_name():
            return False
        
        if not self.check_prerequisites():
            return False
        
        if not self.check_directory_exists():
            return False
        
        # Generation
        if not self.clone_template():
            return False
        
        self.customize_project()
        self.setup_git()
        self.install_dependencies()
        
        # Success
        self.print_next_steps()
        return True
    
    # Helper methods for output
    def _print_banner(self) -> None:
        """Print banner."""
        print("\n" + "=" * 70)
        print("🚀 Create FastAPI App - Production-Grade Boilerplate Generator")
        print("=" * 70 + "\n")
    
    def _info(self, *messages: str) -> None:
        """Print info message."""
        for msg in messages:
            print(f"📦 {msg}")
    
    def _success(self, *messages: str) -> None:
        """Print success message."""
        for msg in messages:
            print(f"✅ {msg}")
    
    def _warning(self, *messages: str) -> None:
        """Print warning message."""
        for msg in messages:
            print(f"⚠️  {msg}")
    
    def _error(self, *messages: str) -> None:
        """Print error message."""
        for msg in messages:
            print(f"❌ {msg}")