"""Application configuration settings."""

import os

# App configuration
APP_TITLE = "Roundnet-Management"
APP_DESCRIPTION = """"""

# Data configuration
DEFAULT_DATA_PATH = "data/"
CACHE_TTL = 3600  # 1 hour in seconds

# Chart configuration
DEFAULT_CHART_HEIGHT = 400
DEFAULT_CHART_WIDTH = 600

# API configuration
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.example.com")
API_TIMEOUT = 30

# Database configuration (if needed)
DATABASE_URL: str | None = os.getenv("DATABASE_URL")

# Feature flags
ENABLE_REAL_TIME_UPDATES = (
    os.getenv("ENABLE_REAL_TIME_UPDATES", "false").lower() == "true"
)
ENABLE_ADVANCED_ANALYTICS = (
    os.getenv("ENABLE_ADVANCED_ANALYTICS", "true").lower() == "true"
)
