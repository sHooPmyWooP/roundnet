"""Data loading utilities."""

import pandas as pd
import streamlit as st
from typing import Optional, Dict, Any, List
from pathlib import Path
import requests
from datetime import datetime

from roundnet.config.settings import DEFAULT_DATA_PATH, API_BASE_URL, API_TIMEOUT


@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_csv_data(file_path: str) -> pd.DataFrame:
    """Load data from a CSV file with caching."""
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        st.error(f"File not found: {file_path}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()


@st.cache_data(ttl=1800)  # Cache for 30 minutes
def fetch_api_data(endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Fetch data from an API endpoint with caching."""
    try:
        url = f"{API_BASE_URL}/{endpoint.lstrip('/')}"
        response = requests.get(url, params=params, timeout=API_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"API request failed: {str(e)}")
        return {}
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return {}


def load_sample_data() -> pd.DataFrame:
    """Load sample roundnet game data."""
    # Generate sample data for demonstration
    sample_data = {
        "game_id": range(1, 101),
        "date": pd.date_range(start="2024-01-01", periods=100, freq="D"),
        "team_a": [f"Team {i % 5 + 1}" for i in range(100)],
        "team_b": [f"Team {(i + 2) % 5 + 1}" for i in range(100)],
        "score_a": [15 + (i % 6) for i in range(100)],
        "score_b": [10 + (i % 8) for i in range(100)],
        "duration_minutes": [25 + (i % 20) for i in range(100)],
        "location": [f"Court {i % 3 + 1}" for i in range(100)],
        "game_type": ["Tournament" if i % 3 == 0 else "Practice" for i in range(100)],
    }

    return pd.DataFrame(sample_data)


def load_player_data() -> pd.DataFrame:
    """Load sample player data."""
    players = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry"]
    teams = ["Team 1", "Team 2", "Team 3", "Team 4", "Team 5"]

    sample_data = {
        "player_id": range(1, len(players) + 1),
        "name": players,
        "team": [teams[i % len(teams)] for i in range(len(players))],
        "games_played": [45 + (i * 7) for i in range(len(players))],
        "wins": [30 + (i * 3) for i in range(len(players))],
        "losses": [15 + (i * 4) for i in range(len(players))],
        "points_scored": [450 + (i * 50) for i in range(len(players))],
        "points_conceded": [320 + (i * 30) for i in range(len(players))],
    }

    return pd.DataFrame(sample_data)


def save_data_to_csv(df: pd.DataFrame, filename: str) -> bool:
    """Save DataFrame to CSV file."""
    try:
        file_path = Path(DEFAULT_DATA_PATH) / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(file_path, index=False)
        return True
    except Exception as e:
        st.error(f"Error saving data: {str(e)}")
        return False


def validate_data(df: pd.DataFrame, required_columns: List[str]) -> bool:
    """Validate that DataFrame has required columns."""
    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        st.error(f"Missing required columns: {missing_columns}")
        return False
    return True
