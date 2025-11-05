"""
# create-fastapi-boilerplate

Production-grade FastAPI project generator with enterprise features.

## Features

✅ **JWT Authentication** - OAuth2 with access & refresh tokens, RBAC  
✅ **Async SQLAlchemy 2.0** - PostgreSQL with full async support  
✅ **Redis Rate Limiting** - Intelligent rate limiting per user/IP  
✅ **OpenTelemetry** - Distributed tracing with Jaeger  
✅ **Prometheus Metrics** - Production-ready monitoring  
✅ **Docker & Compose** - Complete containerization  
✅ **Full Test Suite** - pytest with async support  
✅ **CI/CD Pipeline** - GitHub Actions ready  
✅ **Code Quality** - Ruff, MyPy, pre-commit hooks  

## Installation

```bash
pip install create-fastapi-boilerplate
```

Or with pipx (recommended):

```bash
pipx install create-fastapi-boilerplate
```

## Usage

Create a new FastAPI project:

```bash
create-fastapi-boilerplate my-awesome-api
cd my-awesome-api
make compose-up
```

That's it! Your FastAPI app is now running at http://localhost:8000

## Options

```bash
create-fastapi-boilerplate --help

Options:
  project_name          Name of your project
  --output-dir, -o      Output directory (default: current directory)
  --no-git              Skip git initialization
  --no-install          Skip dependency installation
  --version, -v         Show version
```

## What You Get

```
my-awesome-api/
├── app/                    # Application code
│   ├── api/               # API routes
│   ├── core/              # Config, security
│   ├── models/            # Database models
│   ├── schemas/           # Pydantic schemas
│   └── services/          # Business logic
├── tests/                 # Test suite
├── migrations/            # Alembic migrations
├── docker-compose.yml     # Services setup
├── Dockerfile             # Multi-stage build
├── Makefile               # Dev commands
└── .github/workflows/     # CI/CD
```

## Quick Start

```bash
# Start with Docker (recommended)
make compose-up

# OR run locally
make install          # Install dependencies
make migrate          # Run migrations
make dev              # Start dev server

# Run tests
make test

# Code quality
make lint
make format
make typecheck
```

## API Endpoints

- `POST /api/v1/auth/register` - Register user
- `POST /api/v1/auth/login` - Login
- `GET /api/v1/users/me` - Get current user
- `GET /health` - Health check
- `GET /docs` - OpenAPI docs

## Requirements

- Python 3.8+
- Git
- Docker (optional, but recommended)

## Default Credentials

⚠️ Change these in production!

- Email: `admin@example.com`
- Password: `admin123`

## Documentation

Visit the generated project for complete documentation:
- `README.md` - Full documentation
- `SETUP.md` - Setup guide
- `CONTRIBUTING.md` - Contribution guidelines

## Template Repository

This tool clones from: https://github.com/parth1618/fastapi-boilerplate

## Support

- [Issues](https://github.com/parth1618/fastapi-boilerplate/issues)
- [Discussions](https://github.com/parth1618/fastapi-boilerplate/discussions)

## License

MIT License - See LICENSE file

## Contributing

Contributions welcome! Please see CONTRIBUTING.md

---

Made with ❤️ by [Parth Joshi](https://github.com/parth1618)
"""