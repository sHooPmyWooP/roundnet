"""Pytest configuration and fixtures."""

from datetime import date
from typing import Any

import pandas as pd
import pytest


@pytest.fixture
def sample_games_data() -> pd.DataFrame:
    """Fixture providing sample games data for testing."""
    return pd.DataFrame({
        "game_id": [1, 2, 3, 4, 5],
        "date": pd.date_range(start="2024-01-01", periods=5, freq="D"),
        "team_a": ["Team 1", "Team 2", "Team 1", "Team 3", "Team 2"],
        "team_b": ["Team 2", "Team 3", "Team 3", "Team 1", "Team 1"],
        "score_a": [15, 12, 21, 18, 14],
        "score_b": [10, 15, 19, 20, 16],
        "duration_minutes": [25, 30, 35, 28, 32],
        "location": ["Court 1", "Court 2", "Court 1", "Court 3", "Court 2"],
        "game_type": ["Tournament", "Practice", "Tournament", "Practice", "Tournament"],
    })


@pytest.fixture
def sample_player_data() -> pd.DataFrame:
    """Fixture providing sample player data for testing."""
    return pd.DataFrame({
        "player_id": [1, 2, 3, 4],
        "name": ["Alice", "Bob", "Charlie", "Diana"],
        "team": ["Team 1", "Team 1", "Team 2", "Team 2"],
        "games_played": [45, 42, 38, 40],
        "wins": [30, 28, 25, 24],
        "losses": [15, 14, 13, 16],
        "points_scored": [450, 420, 380, 400],
        "points_conceded": [320, 280, 260, 320],
    })


@pytest.fixture
def mock_sidebar_data() -> dict[str, Any]:
    """Fixture providing mock sidebar selection data."""
    return {
        "start_date": date(2024, 1, 1),
        "end_date": date(2024, 12, 31),
        "selected_team": "Team 1",
        "selected_player": "Alice",
        "selected_game_types": ["Tournament", "Practice"],
        "show_advanced_stats": True,
        "auto_refresh": False,
        "refresh_interval": None,
    }
