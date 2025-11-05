.PHONY: install test lint format clean build publish

install:
	pip install -e ".[dev]"

test:  ## Run all tests
	pytest tests/ -v

test-fast:  ## Run fast tests only (no network)
	pytest tests/ -v -m "not slow"

test-slow:  ## Run slow tests (requires internet)
	pytest tests/ -v -m slow

test-integration:  ## Run integration tests
	pytest tests/ -v -m integration

test-cov:  ## Run tests with coverage
	pytest tests/ --cov=create_fastapi_boilerplate --cov-report=html

lint:
	ruff check .

format:
	ruff format .

typecheck:
	mypy create_fastapi_boilerplate/

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache .coverage htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +

build: clean
	python -m build

publish-test: build
	python -m twine upload --repository testpypi dist/*

publish: build
	python -m twine upload dist/*

install-dev:
	pip install -e ".[dev]"