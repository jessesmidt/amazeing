VENV = venv
PYTHON := $(VENV)/bin/python3
PIP := $(VENV)/bin/pip
MAIN_SCRIPT := a_maze_ing.py
CONFIG_FILE := config.txt


# Phony targets (targets that don't represent files)
.PHONY: venv install run debug clean lint lint-strict help

# Default target
.DEFAULT_GOAL := help

# Create virtual environment
venv:
	python3 -m venv $(VENV)
	@echo "Virtual environment created!"

# Install project dependencies
install: venv
	@echo "Installing project dependencies..."
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install mlx-2.2-py3-none-any.whl
	@echo "Dependencies installed!"

# Run the main script
run:
	@echo "Running A-Maze-ing..."
	$(PYTHON) $(MAIN_SCRIPT) $(CONFIG_FILE)

# Run the main script in debug mode using pdb
debug:
	@echo "Running A-Maze-ing in debug mode..."
	$(PYTHON) -m pdb $(MAIN_SCRIPT) $(CONFIG_FILE)

# Clean temporary files and caches
clean:
	@echo "Cleaning temporary files and caches..."
	@if [ -d "venv" ]; then rm -rf venv && echo "Removed venv/"; fi
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type f -name "*.pyd" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".eggs" -exec rm -rf {} + 2>/dev/null || true
	@echo "Cleanup complete!"

# Run linting with flake8 and mypy (mandatory flags)
lint:
	@echo "Running flake8..."
	$(PYTHON) -m flake8
	@echo "Running mypy with required flags..."
	$(PYTHON) -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

# Run strict linting (optional, enhanced checking)
lint-strict:
	@echo "Running flake8..."
	python3 -m flake8
	@echo "Running mypy with strict mode..."
	mypy . --strict

# Display help information
help:
	@echo "A-Maze-ing Project - Available Make targets:"
	@echo ""
	@echo "  make install      - Install project dependencies"
	@echo "  make run          - Execute the main script with default config"
	@echo "  make debug        - Run the main script in debug mode (pdb)"
	@echo "  make clean        - Remove temporary files and caches"
	@echo "  make lint         - Run flake8 and mypy with required flags"
	@echo "  make lint-strict  - Run flake8 and mypy with strict mode"
	@echo "  make help         - Show this help message"
	@echo ""