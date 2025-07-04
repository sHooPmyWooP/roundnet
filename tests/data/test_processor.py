"""Tests for data processing functionality."""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from roundnet.data.processor import (
    calculate_win_rate,
    get_team_statistics,
    filter_games_by_date,
    get_recent_games,
    calculate_player_stats,
    generate_summary_stats
)


def test_calculate_win_rate(sample_games_data):
    """Test win rate calculation for a team."""
    # Team 1 plays in games 1, 3, 4, 5 and wins games 1, 3
    win_rate = calculate_win_rate(sample_games_data, "Team 1")

    # Should be 2 wins out of 4 games = 0.5
    assert abs(win_rate - 0.5) < 0.01


def test_calculate_win_rate_no_games():
    """Test win rate calculation for team with no games."""
    df = pd.DataFrame({
        "game_id": [1],
        "team_a": ["Team A"],
        "team_b": ["Team B"],
        "score_a": [15],
        "score_b": [10]
    })

    win_rate = calculate_win_rate(df, "Team C")
    assert win_rate == 0.0


def test_get_team_statistics(sample_games_data):
    """Test comprehensive team statistics calculation."""
    stats_df = get_team_statistics(sample_games_data)

    # Check that we get a DataFrame
    assert isinstance(stats_df, pd.DataFrame)

    # Check expected columns
    expected_columns = [
        "team", "games_played", "wins", "losses", "win_rate",
        "points_for", "points_against", "avg_points_for", "avg_points_against",
        "point_differential"
    ]
    for col in expected_columns:
        assert col in stats_df.columns

    # Check that all teams are represented
    teams = set(sample_games_data["team_a"]) | set(sample_games_data["team_b"])
    assert set(stats_df["team"]) == teams

    # Check that games played sum correctly
    # Each game contributes 2 to total games played (one for each team)
    total_games_played = stats_df["games_played"].sum()
    expected_total = len(sample_games_data) * 2
    assert total_games_played == expected_total


def test_filter_games_by_date(sample_games_data):
    """Test filtering games by date range."""
    start_date = datetime(2024, 1, 2)
    end_date = datetime(2024, 1, 4)

    filtered_df = filter_games_by_date(sample_games_data, start_date, end_date)

    # Should get games from Jan 2, 3, 4 (3 games)
    assert len(filtered_df) == 3

    # Check that all dates are within range
    filtered_dates = pd.to_datetime(filtered_df["date"])
    assert all(filtered_dates >= start_date)
    assert all(filtered_dates <= end_date)


def test_get_recent_games():
    """Test getting recent games."""
    # Create a DataFrame with some recent and some old games
    dates = [
        datetime.now() - timedelta(days=1),  # Recent
        datetime.now() - timedelta(days=3),  # Recent
        datetime.now() - timedelta(days=10), # Old
        datetime.now() - timedelta(days=20), # Old
    ]

    df = pd.DataFrame({
        "game_id": [1, 2, 3, 4],
        "date": dates,
        "team_a": ["A", "B", "C", "D"],
        "team_b": ["B", "C", "D", "A"],
        "score_a": [15, 12, 18, 20],
        "score_b": [10, 15, 16, 22],
        "duration_minutes": [25, 30, 28, 35],
        "location": ["Court 1"] * 4,
        "game_type": ["Tournament"] * 4,
    })

    recent_df = get_recent_games(df, days=7)

    # Should get 2 recent games
    assert len(recent_df) == 2


def test_calculate_player_stats(sample_games_data, sample_player_data):
    """Test player statistics calculation."""
    stats_df = calculate_player_stats(sample_games_data, sample_player_data)

    # Check that we get a DataFrame
    assert isinstance(stats_df, pd.DataFrame)

    # Check expected columns
    expected_columns = [
        "player_name", "team", "games_played", "wins", "losses", "win_rate",
        "attack_rating", "defense_rating", "consistency", "teamwork"
    ]
    for col in expected_columns:
        assert col in stats_df.columns

    # Check that all players are represented
    assert len(stats_df) == len(sample_player_data)

    # Check that ratings are within reasonable bounds (0-100)
    for rating_col in ["attack_rating", "defense_rating", "consistency", "teamwork"]:
        assert all(stats_df[rating_col] >= 0)
        assert all(stats_df[rating_col] <= 100)


def test_generate_summary_stats():
    """Test summary statistics generation."""
    stats = generate_summary_stats()

    # Check that we get a dictionary
    assert isinstance(stats, dict)

    # Check expected keys
    expected_keys = [
        "total_games", "total_players", "avg_game_duration",
        "recent_games", "last_updated"
    ]
    for key in expected_keys:
        assert key in stats

    # Check data types
    assert isinstance(stats["total_games"], int)
    assert isinstance(stats["total_players"], int)
    assert isinstance(stats["avg_game_duration"], (int, float))
    assert isinstance(stats["recent_games"], int)
    assert isinstance(stats["last_updated"], str)

    # Check reasonable values
    assert stats["total_games"] > 0
    assert stats["total_players"] > 0
    assert stats["avg_game_duration"] > 0
