"""Tests for data loading functionality."""

from unittest.mock import patch

from roundnet.data.loader import (
    create_sample_data,
    create_sample_teams_and_games,
)


def test_create_sample_data():
    """Test creating sample data for the new system."""
    with patch('roundnet.data.loader.add_player') as mock_add_player, \
         patch('roundnet.data.loader.add_playing_day') as mock_add_playing_day, \
         patch('roundnet.data.loader.assign_players_to_playing_day') as mock_assign:

        create_sample_data()

        # Verify that players were created
        assert mock_add_player.call_count > 0

        # Verify that playing days were created
        assert mock_add_playing_day.call_count > 0

        # Verify that players were assigned to playing days
        assert mock_assign.call_count > 0


def test_create_sample_teams_and_games():
    """Test creating sample teams and games (legacy function)."""
    with patch('roundnet.data.loader.create_sample_data') as mock_create_sample:

        create_sample_teams_and_games()

        # Verify that the new function was called
        assert mock_create_sample.call_count == 1
