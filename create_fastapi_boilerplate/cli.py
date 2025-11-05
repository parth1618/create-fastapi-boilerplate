"""Command-line interface for create-fastapi-boilerplate."""

import argparse
import sys

from .generator import FastAPIProjectGenerator


def main() -> int:
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="Create a new FastAPI project from production-grade boilerplate",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  create-fastapi-boilerplate my-awesome-api
  create-fastapi-boilerplate my-project --output-dir ~/projects
  create-fastapi-boilerplate my-api --no-git
  
Features:
  - JWT Authentication with RBAC
  - SQLAlchemy 2.0 with async PostgreSQL
  - Redis rate limiting
  - OpenTelemetry tracing
  - Prometheus metrics
  - Docker & Docker Compose
  - Full test suite
  - CI/CD with GitHub Actions
  
For more information, visit:
  https://github.com/parth1618/fastapi-boilerplate
        """
    )
    
    parser.add_argument(
        "project_name",
        help="Name of your FastAPI project (lowercase, hyphens/underscores allowed)"
    )
    
    parser.add_argument(
        "--output-dir",
        "-o",
        help="Output directory (defaults to current directory)",
        default=None
    )
    
    parser.add_argument(
        "--no-git",
        action="store_true",
        help="Skip git initialization"
    )
    
    parser.add_argument(
        "--no-install",
        action="store_true",
        help="Skip dependency installation"
    )
    
    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version="create-fastapi-boilerplate 1.0.0"
    )
    
    args = parser.parse_args()
    
    # Generate project
    generator = FastAPIProjectGenerator(
        project_name=args.project_name,
        output_dir=args.output_dir,
        init_git=not args.no_git,
        install_deps=not args.no_install
    )
    
    success = generator.generate()
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())