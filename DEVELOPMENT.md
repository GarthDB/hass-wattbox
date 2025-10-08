# Development Setup

This guide helps you set up local development with automated quality checks.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
make install
# or
pip install -r requirements-dev.txt
```

### 2. Set Up Pre-commit Hooks (Recommended)
```bash
make pre-commit
# or
pip install pre-commit
pre-commit install
pre-commit install --hook-type pre-push
```

### 3. Configure Git Hooks (Alternative)
```bash
git config core.hooksPath .githooks
```

## 🛠️ Available Commands

### Using Make (Recommended)
```bash
make help          # Show all available commands
make format        # Format code (black + isort)
make lint          # Run linting (flake8 + mypy)
make test          # Run tests
make check-all     # Run all checks (format + lint + test)
make fix           # Format code and run tests
make clean         # Clean up temporary files
```

### Using Scripts
```bash
./scripts/test-local.sh  # Run all CI checks locally
```

### Manual Commands
```bash
# Format code
black custom_components/wattbox tests/
isort --profile=black custom_components/wattbox tests/

# Check formatting
black --check custom_components/wattbox tests/
isort --check-only --profile=black custom_components/wattbox tests/

# Run linting
flake8 custom_components/wattbox tests/
mypy custom_components/wattbox tests/ --ignore-missing-imports

# Run tests
pytest tests/ --cov=custom_components/wattbox --cov-report=term-missing
```

## 🔧 IDE Setup

### VS Code
The project includes `.vscode/settings.json` with:
- Auto-formatting on save (Black)
- Auto-import sorting (isort)
- Linting enabled (flake8, mypy)
- Trailing whitespace removal

### Other IDEs
Configure your IDE to:
- Use Black for Python formatting
- Use isort for import sorting
- Enable flake8 and mypy linting
- Remove trailing whitespace on save

## 🚨 Pre-Push Workflow

### Option 1: Pre-commit Hooks (Automatic)
Pre-commit hooks will automatically run checks on:
- `git commit` - Basic checks (formatting, linting)
- `git push` - Full checks (formatting, linting, tests)

### Option 2: Manual Check
```bash
make check-all
# or
./scripts/test-local.sh
```

### Option 3: Git Pre-push Hook
```bash
git config core.hooksPath .githooks
```

## 🐛 Troubleshooting

### Pre-commit Hooks Not Working
```bash
# Reinstall hooks
pre-commit uninstall
pre-commit install
pre-commit install --hook-type pre-push
```

### Formatting Issues
```bash
# Auto-fix formatting
make format

# Check what would be changed
make format-check
```

### Test Failures
```bash
# Run tests with verbose output
pytest tests/ -v --tb=short

# Run specific test file
pytest tests/test_specific.py -v
```

## 📋 CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/ci.yml`) runs:
1. **Format Check**: `black --check` and `isort --check-only`
2. **Linting**: `flake8` and `mypy`
3. **Testing**: `pytest` with coverage
4. **Security**: `bandit` and `safety`

All these checks should pass locally before pushing!
