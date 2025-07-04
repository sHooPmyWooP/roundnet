"""Application configuration settings."""

import os
from typing import Optional

# App configuration
APP_TITLE = "Roundnet Analytics Dashboard"
APP_DESCRIPTION = """
🏐 **Welcome to the Interactive Roundnet Analytics Dashboard!**

Manage your roundnet teams, track player performance, and record game results with our easy-to-use web interface.
No file uploads needed - create and manage everything directly through the app!

**Features:**
- 🏐 Create and manage teams
- 👤 Add and organize players
- 🎯 Record game results
- 📊 View detailed statistics and analytics
- 📈 Track performance trends over time
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
DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")

# Feature flags
ENABLE_REAL_TIME_UPDATES = os.getenv("ENABLE_REAL_TIME_UPDATES", "false").lower() == "true"
ENABLE_ADVANCED_ANALYTICS = os.getenv("ENABLE_ADVANCED_ANALYTICS", "true").lower() == "true"
