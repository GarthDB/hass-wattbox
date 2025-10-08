.PHONY: help install test lint format check-all clean pre-commit

# Default target
help:
	@echo "Available commands:"
	@echo "  install     - Install development dependencies"
	@echo "  test        - Run all tests"
	@echo "  lint        - Run linting checks (flake8, mypy)"
	@echo "  format      - Format code (black, isort)"
	@echo "  check-all   - Run all checks (format, lint, test)"
	@echo "  pre-commit  - Install pre-commit hooks"
	@echo "  clean       - Clean up temporary files"

# Install dependencies
install:
	pip install -r requirements-dev.txt

# Run tests
test:
	python3 -m pytest tests/ --cov=custom_components/wattbox --cov-report=term-missing --tb=short

# Run linting
lint:
	python3 -m flake8 custom_components/wattbox tests/
	# python3 -m mypy custom_components/wattbox tests/ --ignore-missing-imports  # Skip due to HA stubs issues

# Format code
format:
	python3 -m black custom_components/wattbox tests/
	python3 -m isort --profile=black custom_components/wattbox tests/

# Check formatting without changing files
format-check:
	python3 -m black --check custom_components/wattbox tests/
	python3 -m isort --check-only --profile=black custom_components/wattbox tests/

# Run all checks
check-all: format-check lint test

# Install pre-commit hooks
pre-commit:
	pip install pre-commit
	pre-commit install
	pre-commit install --hook-type pre-push

# Clean up
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .coverage htmlcov/ .pytest_cache/ .mypy_cache/

# Quick fix (format + test)
fix: format test
