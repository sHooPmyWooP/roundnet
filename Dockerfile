# Use Python 3.13 slim image as base
FROM python:3.13-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Copy dependency files
COPY pyproject.toml uv.lock README.md ./

# Install Python dependencies
RUN uv sync --frozen --no-dev

# Copy application code
COPY src/ ./src/
COPY data/ ./data/

# Create data directory with proper permissions
RUN mkdir -p /app/data && chmod 755 /app/data

# Expose the port that Streamlit runs on
EXPOSE 8501

# Set environment variables for Streamlit
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run the application
CMD ["uv", "run", "streamlit", "run", "src/roundnet/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
