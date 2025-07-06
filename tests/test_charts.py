"""Tests for charts module."""

from unittest.mock import patch

import pandas as pd
import plotly.graph_objects as go
import pytest

from roundnet.components.charts import (
    create_games_over_time_chart,
    create_player_performance_radar,
    create_sample_chart,
    create_score_distribution_chart,
    create_team_performance_chart,
    create_win_rate_chart,
)


@pytest.fixture
def sample_games():
    """Sample games data for testing."""
    return [
        {
            'id': 'game1',
            'team_a_id': 'team1',
            'team_b_id': 'team2',
            'score_a': 21,
            'score_b': 19,
            'date': '2024-01-01'
        },
        {
            'id': 'game2',
            'team_a_id': 'team1',
            'team_b_id': 'team3',
            'score_a': 15,
            'score_b': 21,
            'date': '2024-01-02'
        },
        {
            'id': 'game3',
            'team_a_id': 'team2',
            'team_b_id': 'team3',
            'score_a': 18,
            'score_b': 21,
            'date': '2024-01-03'
        }
    ]


@pytest.fixture
def sample_team_stats():
    """Sample team stats for testing."""
    return pd.DataFrame([
        {'team_name': 'Team A', 'games_played': 5, 'wins': 3, 'losses': 2, 'win_rate': 0.6},
        {'team_name': 'Team B', 'games_played': 4, 'wins': 2, 'losses': 2, 'win_rate': 0.5},
        {'team_name': 'Team C', 'games_played': 3, 'wins': 1, 'losses': 2, 'win_rate': 0.33},
    ])


class TestCreateGamesOverTimeChart:
    """Tests for create_games_over_time_chart function."""

    @patch('roundnet.components.charts.get_games')
    def test_create_games_over_time_chart_with_games(self, mock_get_games, sample_games):
        """Test creating games over time chart with games data."""
        mock_get_games.return_value = sample_games

        fig = create_games_over_time_chart()

        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0
        assert "Games Over Time" in str(fig.layout.title.text)

    @patch('roundnet.components.charts.get_games')
    def test_create_games_over_time_chart_no_games(self, mock_get_games):
        """Test creating games over time chart with no games data."""
        mock_get_games.return_value = []

        fig = create_games_over_time_chart()

        assert isinstance(fig, go.Figure)
        assert "No games recorded yet" in str(fig.layout.annotations[0].text)


class TestCreateWinRateChart:
    """Tests for create_win_rate_chart function."""

    @patch('roundnet.components.charts.get_team_stats')
    def test_create_win_rate_chart_with_stats(self, mock_get_team_stats, sample_team_stats):
        """Test creating win rate chart with team stats."""
        mock_get_team_stats.return_value = sample_team_stats

        fig = create_win_rate_chart()

        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0
        assert "Team Win Rates" in str(fig.layout.title.text)

    @patch('roundnet.components.charts.get_team_stats')
    def test_create_win_rate_chart_no_stats(self, mock_get_team_stats):
        """Test creating win rate chart with no team stats."""
        mock_get_team_stats.return_value = pd.DataFrame()

        fig = create_win_rate_chart()

        assert isinstance(fig, go.Figure)
        assert "No team data available" in str(fig.layout.annotations[0].text)


class TestCreateScoreDistributionChart:
    """Tests for create_score_distribution_chart function."""

    @patch('roundnet.components.charts.get_games')
    def test_create_score_distribution_chart_with_games(self, mock_get_games, sample_games):
        """Test creating score distribution chart with games data."""
        mock_get_games.return_value = sample_games

        fig = create_score_distribution_chart()

        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0
        assert "Score Distribution" in str(fig.layout.title.text)

    @patch('roundnet.components.charts.get_games')
    def test_create_score_distribution_chart_no_games(self, mock_get_games):
        """Test creating score distribution chart with no games data."""
        mock_get_games.return_value = []

        fig = create_score_distribution_chart()

        assert isinstance(fig, go.Figure)
        assert "No game data available" in str(fig.layout.annotations[0].text)


class TestCreateTeamPerformanceChart:
    """Tests for create_team_performance_chart function."""

    @patch('roundnet.components.charts.get_team_stats')
    def test_create_team_performance_chart_with_stats(self, mock_get_team_stats, sample_team_stats):
        """Test creating team performance chart with team stats."""
        mock_get_team_stats.return_value = sample_team_stats

        fig = create_team_performance_chart()

        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0
        assert "Team Performance Overview" in str(fig.layout.title.text)

    @patch('roundnet.components.charts.get_team_stats')
    def test_create_team_performance_chart_no_stats(self, mock_get_team_stats):
        """Test creating team performance chart with no team stats."""
        mock_get_team_stats.return_value = pd.DataFrame()

        fig = create_team_performance_chart()

        assert isinstance(fig, go.Figure)
        assert "No team performance data available" in str(fig.layout.annotations[0].text)


class TestCreatePlayerPerformanceRadar:
    """Tests for create_player_performance_radar function."""

    def test_create_player_performance_radar_with_stats(self):
        """Test creating player performance radar chart with stats."""
        player_stats = {
            'win_rate': 0.7,
            'avg_score': 18.5,
            'consistency': 0.8,
            'partnership_diversity': 0.6,
            'recent_form': 0.9
        }

        fig = create_player_performance_radar(player_stats)

        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0
        assert "Player Performance Radar" in str(fig.layout.title.text)

    def test_create_player_performance_radar_empty_stats(self):
        """Test creating player performance radar chart with empty stats."""
        player_stats = {}

        # This should raise an IndexError currently, so we test for that
        with pytest.raises(IndexError):
            create_player_performance_radar(player_stats)


class TestCreateSampleChart:
    """Tests for create_sample_chart function."""

    def test_create_sample_chart(self):
        """Test creating sample chart."""
        fig = create_sample_chart()

        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0
        assert "Sample Chart" in str(fig.layout.title.text)
        assert fig.data[0].x == (1, 2, 3, 4, 5)
        assert fig.data[0].y == (2, 4, 3, 5, 1)


class TestChartPropertiesAndLayouts:
    """Tests for chart properties and layouts."""

    @patch('roundnet.components.charts.get_games')
    def test_chart_has_proper_height(self, mock_get_games, sample_games):
        """Test that charts have proper height set."""
        mock_get_games.return_value = sample_games

        fig = create_games_over_time_chart()

        # Should have height from DEFAULT_CHART_HEIGHT
        assert fig.layout.height is not None
        assert fig.layout.height > 0

    @patch('roundnet.components.charts.get_team_stats')
    def test_chart_has_axis_labels(self, mock_get_team_stats, sample_team_stats):
        """Test that charts have proper axis labels."""
        mock_get_team_stats.return_value = sample_team_stats

        fig = create_win_rate_chart()

        # Should have proper axis titles
        assert fig.layout.xaxis.title is not None
        assert fig.layout.yaxis.title is not None

    def test_chart_colors_and_styling(self):
        """Test that charts have proper colors and styling."""
        fig = create_sample_chart()

        # Should have proper layout and styling
        assert fig.layout.title is not None
        assert hasattr(fig.data[0], 'mode')
        assert 'markers' in fig.data[0].mode
