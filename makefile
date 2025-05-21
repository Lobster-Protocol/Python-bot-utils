.PHONY: all fmt format check venv install install-dev install-prod build-prod clean

# Python and venv settings
PYTHON := python3
VENV_NAME := .venv
VENV_ACTIVATE := $(VENV_NAME)/bin/activate
PIP := $(VENV_NAME)/bin/pip
DIST_DIR := dist

# Default target runs venvinstall
all: @

# Run fmt (format + check)
fmt:
	pre-commit run isort --all-files
	pre-commit run black --all-files
	pre-commit run --all-files
	@echo "All formatting and checks complete!"

# Format code only
format:
	pre-commit run isort --all-files
	pre-commit run black --all-files
	@echo "Formatting complete!"

# Check without modifying files
check:
	pre-commit run --all-files --hook-stage manual
	@echo "Checks complete!"

# Virtual environment
venv:
	$(PYTHON) -m venv $(VENV_NAME)
	@echo "Run 'source $(VENV_ACTIVATE)' to activate the virtual environment"

venv-enable: venv
	@echo "To activate the virtual environment, run:"
	@echo "source $(VENV_ACTIVATE)"

# Install pre-commit hooks and base package
install: venv
	make install-dev

# Install with development dependencies
install-dev: venv
	$(PIP) install -e ".[dev,test]"
	$(PIP) install pre-commit
	pre-commit install

# Clean up
clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -type d -delete
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf *.egg-info
	rm -rf .mypy_cache
	rm -rf $(DIST_DIR)
	rm -rf build

# Production build
build-prod: clean
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install build wheel
	$(PYTHON) -m build -w -s
	@echo "Production build created in $(DIST_DIR)/"

# Install for production
install-prod: venv
	$(PIP) install -e .
	@echo "Package installed in production mode (without dev dependencies)"

# Help command
help:
	@echo "Available targets:"
	@echo "  all                Run fmt (default)"
	@echo "  fmt                Format files and run all checks"
	@echo "  check              Run all lint checks without modifying files"
	@echo "  venv               Create a virtual environment"
	@echo "  install            Install package and pre-commit hooks"
	@echo "  install-dev        Install package with dev dependencies"
	@echo "  install-prod       Install package for production (no dev dependencies)"
	@echo "  build-prod         Create production wheel and source distribution"
	@echo "  clean              Remove Python artifacts"
	@echo "  help               Show this help message"
