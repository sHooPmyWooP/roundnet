"""Tests for data processor module - FIXED VERSION."""

from datetime import date
from unittest.mock import patch

import pandas as pd
import pytest

from roundnet.data.processor import (
    calculate_win_rate,
    filter_games_by_date_range,
    generate_summary_stats,
    get_head_to_head_record,
    get_player_team_contribution,
    get_team_performance_trends,
)


@pytest.fixture
def sample_games():
    """Sample games data for testing."""
    return [
        {
            'id': 'game1',
            'playing_day_id': 'day1',
            'team_a_id': 'team1',
            'team_b_id': 'team2',
            'score_a': 21,
            'score_b': 19,
            'date': date(2024, 1, 1)
        },
        {
            'id': 'game2',
            'playing_day_id': 'day1',
            'team_a_id': 'team2',
            'team_b_id': 'team3',
            'score_a': 15,
            'score_b': 21,
            'date': date(2024, 1, 2)
        },
        {
            'id': 'game3',
            'playing_day_id': 'day2',
            'team_a_id': 'team1',
            'team_b_id': 'team3',
            'score_a': 18,
            'score_b': 21,
            'date': date(2024, 1, 3)
        }
    ]


@pytest.fixture
def sample_players():
    """Sample players data for testing."""
    return [
        {'id': 'player1', 'name': 'Alice', 'skill_level': 8},
        {'id': 'player2', 'name': 'Bob', 'skill_level': 7},
        {'id': 'player3', 'name': 'Charlie', 'skill_level': 6},
        {'id': 'player4', 'name': 'David', 'skill_level': 9},
    ]


class TestCalculateWinRate:
    """Tests for calculate_win_rate function."""

    @patch('roundnet.data.manager.get_games')
    def test_calculate_win_rate_with_wins(self, mock_get_games, sample_games):
        """Test calculating win rate for a team with wins."""
        mock_get_games.return_value = sample_games

        win_rate = calculate_win_rate('team1')

        assert win_rate == 0.5  # 1 win out of 2 games

    @patch('roundnet.data.manager.get_games')
    def test_calculate_win_rate_no_games(self, mock_get_games):
        """Test calculating win rate for a team with no games."""
        mock_get_games.return_value = []

        win_rate = calculate_win_rate('team1')

        assert win_rate == 0.0

    @patch('roundnet.data.manager.get_games')
    def test_calculate_win_rate_team_not_in_games(self, mock_get_games, sample_games):
        """Test calculating win rate for a team that hasn't played."""
        mock_get_games.return_value = sample_games

        win_rate = calculate_win_rate('team_nonexistent')

        assert win_rate == 0.0


class TestGetTeamPerformanceTrends:
    """Tests for get_team_performance_trends function."""

    @patch('roundnet.data.manager.get_games')
    def test_get_team_performance_trends(self, mock_get_games, sample_games):
        """Test getting team performance trends."""
        mock_get_games.return_value = sample_games

        trends = get_team_performance_trends('team1')

        assert isinstance(trends, pd.DataFrame)
        assert len(trends) > 0
        assert 'date' in trends.columns

    @patch('roundnet.data.manager.get_games')
    def test_get_team_performance_trends_no_games(self, mock_get_games):
        """Test getting team performance trends with no games."""
        mock_get_games.return_value = []

        trends = get_team_performance_trends('team1')

        assert isinstance(trends, pd.DataFrame)
        assert len(trends) == 0


class TestFilterGamesByDateRange:
    """Tests for filter_games_by_date_range function."""

    @patch('roundnet.data.manager.get_games')
    def test_filter_games_by_date_range(self, mock_get_games, sample_games):
        """Test filtering games by date range."""
        mock_get_games.return_value = sample_games

        start_date = date(2024, 1, 1)
        end_date = date(2024, 1, 2)
        filtered_games = filter_games_by_date_range(start_date, end_date)

        assert len(filtered_games) == 2
        assert all(game['date'] >= start_date and game['date'] <= end_date for game in filtered_games)

    @patch('roundnet.data.manager.get_games')
    def test_filter_games_by_date_range_no_matches(self, mock_get_games, sample_games):
        """Test filtering games by date range with no matches."""
        mock_get_games.return_value = sample_games

        start_date = date(2024, 2, 1)
        end_date = date(2024, 2, 28)
        filtered_games = filter_games_by_date_range(start_date, end_date)

        assert len(filtered_games) == 0


class TestGetHeadToHeadRecord:
    """Tests for get_head_to_head_record function."""

    @patch('roundnet.data.manager.get_games')
    def test_get_head_to_head_record(self, mock_get_games, sample_games):
        """Test getting head-to-head record between teams."""
        mock_get_games.return_value = sample_games

        record = get_head_to_head_record('team1', 'team2')

        assert isinstance(record, dict)
        assert 'team_a_wins' in record
        assert 'team_b_wins' in record
        assert record['team_a_wins'] == 1
        assert record['team_b_wins'] == 0

    @patch('roundnet.data.manager.get_games')
    def test_get_head_to_head_record_no_games(self, mock_get_games):
        """Test getting head-to-head record with no games."""
        mock_get_games.return_value = []

        record = get_head_to_head_record('team1', 'team2')

        assert isinstance(record, dict)
        assert record['team_a_wins'] == 0
        assert record['team_b_wins'] == 0


class TestGetPlayerTeamContribution:
    """Tests for get_player_team_contribution function."""

    @patch('roundnet.data.manager.get_player_by_id')
    def test_get_player_team_contribution(self, mock_get_player):
        """Test getting player team contribution."""
        mock_get_player.return_value = {'id': 'player1', 'name': 'Alice'}

        contribution = get_player_team_contribution('player1')

        assert isinstance(contribution, dict)
        # This function has minimal implementation, just check it doesn't crash

    @patch('roundnet.data.manager.get_player_by_id')
    def test_get_player_team_contribution_no_player(self, mock_get_player):
        """Test getting player team contribution for non-existent player."""
        mock_get_player.return_value = None

        contribution = get_player_team_contribution('nonexistent')

        assert isinstance(contribution, dict)


class TestGenerateSummaryStats:
    """Tests for generate_summary_stats function."""

    @patch('roundnet.data.manager.get_team_stats')
    def test_generate_summary_stats(self, mock_get_team_stats, sample_games, sample_players):
        """Test generating summary statistics."""
        mock_get_team_stats.return_value = pd.DataFrame([
            {'team_id': 'team1', 'wins': 5, 'losses': 3},
            {'team_id': 'team2', 'wins': 3, 'losses': 5},
        ])

        stats = generate_summary_stats()

        assert isinstance(stats, dict)
        assert 'total_games' in stats
        assert 'total_teams' in stats

    @patch('roundnet.data.manager.get_team_stats')
    def test_generate_summary_stats_empty_data(self, mock_get_team_stats):
        """Test generating summary statistics with empty data."""
        mock_get_team_stats.return_value = pd.DataFrame()

        stats = generate_summary_stats()

        assert isinstance(stats, dict)
        assert stats['total_games'] == 0
        assert stats['total_teams'] == 0
