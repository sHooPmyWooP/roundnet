"""Application configuration settings."""

import os

# App configuration
APP_TITLE = "Roundnet Player Management"
APP_DESCRIPTION = """
🏐 **Welcome to the Roundnet Player Management System!**

Organize players, create playing days, and generate balanced teams with intelligent algorithms.
Track performance and partnerships with persistent file-based storage.

**Features:**
- 👤 Create and manage players with skill levels
- 📅 Organize playing days and assign players
- � Generate balanced teams using multiple algorithms
- 🎯 Record game results (wins/losses/ties)
- 📊 Track player statistics and partnerships
- � Persistent file-based data storage
"""

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
ENABLE_REAL_TIME_UPDATES = os.getenv("ENABLE_REAL_TIME_UPDATES", "false").lower() == "true"
ENABLE_ADVANCED_ANALYTICS = os.getenv("ENABLE_ADVANCED_ANALYTICS", "true").lower() == "true"
