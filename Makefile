# Development commands for the roundnet project

.PHONY: install dev test lint format clean run help

# Default target
help:
	@echo "Available commands:"
	@echo "  install    - Install dependencies"
	@echo "  dev        - Install development dependencies"
	@echo "  run        - Run the Streamlit app"
	@echo "  test       - Run tests"
	@echo "  test-cov   - Run tests with coverage"
	@echo "  lint       - Run linting checks"
	@echo "  format     - Format code"
	@echo "  pre-commit - Run pre-commit hooks"
	@echo "  clean      - Clean cache and temporary files"

install:
	uv sync

dev:
	uv sync --extra dev

run:
	uv run streamlit run src/roundnet/main.py

test:
	uv run pytest

test-cov:
	uv run pytest --cov=src --cov-report=html --cov-report=term

lint:
	uv run ruff check src tests
	uv run mypy src

format:
	uv run black src tests
	uv run ruff check --fix src tests

pre-commit:
	uv run pre-commit run --all-files

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/ .coverage 2>/dev/null || true
