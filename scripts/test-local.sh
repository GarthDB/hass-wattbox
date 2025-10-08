#!/bin/bash
# Local testing script to run CI checks before pushing

set -e

echo "🔍 Running local CI checks..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print status
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
        exit 1
    fi
}

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo -e "${RED}❌ Please run this script from the project root directory${NC}"
    exit 1
fi

# Install dependencies if needed
echo "📦 Installing dependencies..."
pip install -r requirements-dev.txt > /dev/null 2>&1
print_status $? "Dependencies installed"

# Run black formatting check
echo "🎨 Checking code formatting with black..."
python3 -m black --check custom_components/wattbox tests/
print_status $? "Black formatting check passed"

# Run isort import sorting check
echo "📋 Checking import sorting with isort..."
python3 -m isort --check-only --profile=black custom_components/wattbox tests/
print_status $? "Import sorting check passed"

# Run flake8 linting
echo "🔍 Running flake8 linting..."
python3 -m flake8 custom_components/wattbox tests/
print_status $? "Flake8 linting passed"

# Run mypy type checking
echo "🔬 Running mypy type checking..."
python3 -m mypy custom_components/wattbox tests/ --ignore-missing-imports
print_status $? "MyPy type checking passed"

# Run pytest tests
echo "🧪 Running pytest tests..."
python3 -m pytest tests/ --cov=custom_components/wattbox --cov-report=term-missing --tb=short
print_status $? "All tests passed"

echo -e "${GREEN}🎉 All local checks passed! Ready to push.${NC}"
