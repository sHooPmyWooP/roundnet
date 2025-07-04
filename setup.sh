#!/bin/bash

# Roundnet Project Setup Script
# This script sets up the development environment for the roundnet Streamlit app

set -e

echo "🏐 Setting up Roundnet Streamlit Project..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
else
    echo "✅ uv is already installed"
fi

# Install dependencies
echo "📦 Installing dependencies..."
uv sync --extra dev

# Install pre-commit hooks
echo "🔧 Setting up pre-commit hooks..."
uv run pre-commit install

# Run initial checks
echo "🧪 Running initial code quality checks..."
uv run ruff check src tests
uv run black --check src tests
uv run mypy src

# Run tests
echo "🧪 Running tests..."
uv run pytest

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To run the Streamlit app:"
echo "  uv run streamlit run src/roundnet/main.py"
echo ""
echo "Other useful commands:"
echo "  make run        - Run the app"
echo "  make test       - Run tests"
echo "  make lint       - Run linting"
echo "  make format     - Format code"
echo "  make help       - Show all commands"
echo ""
echo "The app will be available at: http://localhost:8501"
