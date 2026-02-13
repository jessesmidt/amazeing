# Makefile for A-Maze-ing Python Project

# Variables
PYTHON := python3
PIP := pip3
MAIN_SCRIPT := a_maze_ing.py
CONFIG_FILE := config.txt

# Phony targets (targets that don't represent files)
.PHONY: install run debug clean lint lint-strict help

# Default target
.DEFAULT_GOAL := help

# Install project dependencies
install:
	@echo "Installing project dependencies..."
	$(PIP) install -r requirements.txt

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
	flake8 .
	@echo "Running mypy with required flags..."
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

# Run strict linting (optional, enhanced checking)
lint-strict:
	@echo "Running flake8..."
	flake8 .
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