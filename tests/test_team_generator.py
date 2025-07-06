"""Tests for team generator module."""


import pytest

from roundnet.data.models import Partnership, Player
from roundnet.data.team_generator import TeamGenerator


@pytest.fixture
def sample_players():
    """Sample players for testing."""
    return [
        Player(id="player1", name="Alice", skill_level=8),
        Player(id="player2", name="Bob", skill_level=7),
        Player(id="player3", name="Charlie", skill_level=6),
        Player(id="player4", name="David", skill_level=9),
        Player(id="player5", name="Eve", skill_level=5),
        Player(id="player6", name="Frank", skill_level=8),
    ]


@pytest.fixture
def sample_partnerships():
    """Sample partnerships for testing."""
    return [
        Partnership(
            player_a_id="player1",
            player_b_id="player2",
            times_together=5,
            wins_together=3
        ),
        Partnership(
            player_a_id="player3",
            player_b_id="player4",
            times_together=3,
            wins_together=1
        ),
    ]


@pytest.fixture
def team_generator(sample_players, sample_partnerships):
    """Team generator instance for testing."""
    return TeamGenerator(sample_players, sample_partnerships)


class TestTeamGenerator:
    """Tests for TeamGenerator class."""

    def test_init(self, sample_players, sample_partnerships):
        """Test TeamGenerator initialization."""
        generator = TeamGenerator(sample_players, sample_partnerships)

        assert len(generator.players) == len(sample_players)
        assert "player1" in generator.players
        assert len(generator.partnerships) > 0

    def test_build_partnership_dict(self, team_generator):
        """Test partnership dictionary building."""
        # Should be able to lookup partnerships in both directions
        assert ("player1", "player2") in team_generator.partnerships
        assert ("player2", "player1") in team_generator.partnerships

        # Should be the same partnership object
        p1 = team_generator.partnerships[("player1", "player2")]
        p2 = team_generator.partnerships[("player2", "player1")]
        assert p1 is p2

    def test_get_partnership_count(self, team_generator):
        """Test getting partnership count."""
        count = team_generator.get_partnership_count("player1", "player2")
        assert count == 5

        # Test reverse order
        count_reverse = team_generator.get_partnership_count("player2", "player1")
        assert count_reverse == 5

        # Test non-existent partnership
        count_none = team_generator.get_partnership_count("player1", "player5")
        assert count_none == 0

    def test_random_teams_even_players(self, team_generator):
        """Test random team generation with even number of players."""
        player_ids = ["player1", "player2", "player3", "player4"]
        teams = team_generator.random_teams(player_ids)

        assert len(teams) == 2
        assert all(len(team) == 2 for team in teams)

        # All players should be assigned
        all_assigned = [player for team in teams for player in team]
        assert sorted(all_assigned) == sorted(player_ids)

    def test_random_teams_odd_players(self, team_generator):
        """Test random team generation with odd number of players."""
        player_ids = ["player1", "player2", "player3"]

        with pytest.raises(ValueError, match="Number of players must be even"):
            team_generator.random_teams(player_ids)

    def test_skill_balanced_teams(self, team_generator):
        """Test skill-balanced team generation."""
        player_ids = ["player1", "player2", "player3", "player4"]
        teams = team_generator.skill_balanced_teams(player_ids)

        assert len(teams) == 2
        assert all(len(team) == 2 for team in teams)

        # All players should be assigned
        all_assigned = [player for team in teams for player in team]
        assert sorted(all_assigned) == sorted(player_ids)

    def test_skill_balanced_teams_odd_players(self, team_generator):
        """Test skill-balanced team generation with odd players."""
        player_ids = ["player1", "player2", "player3"]

        with pytest.raises(ValueError, match="Number of players must be even"):
            team_generator.skill_balanced_teams(player_ids)

    def test_partnership_balanced_teams(self, team_generator):
        """Test partnership-balanced team generation."""
        player_ids = ["player1", "player2", "player3", "player4"]
        teams = team_generator.partnership_balanced_teams(player_ids)

        assert len(teams) == 2
        assert all(len(team) == 2 for team in teams)

        # All players should be assigned
        all_assigned = [player for team in teams for player in team]
        assert sorted(all_assigned) == sorted(player_ids)

    def test_win_rate_balanced_teams(self, team_generator):
        """Test win-rate-balanced team generation."""
        player_ids = ["player1", "player2", "player3", "player4"]
        teams = team_generator.win_rate_balanced_teams(player_ids)

        assert len(teams) == 2
        assert all(len(team) == 2 for team in teams)

        # All players should be assigned
        all_assigned = [player for team in teams for player in team]
        assert sorted(all_assigned) == sorted(player_ids)

    def test_generate_teams_random(self, team_generator):
        """Test generate_teams with random algorithm."""
        player_ids = ["player1", "player2", "player3", "player4"]
        teams = team_generator.generate_teams(player_ids, "random")

        assert len(teams) == 2
        assert all(len(team) == 2 for team in teams)

    def test_generate_teams_skill_balanced(self, team_generator):
        """Test generate_teams with skill_balanced algorithm."""
        player_ids = ["player1", "player2", "player3", "player4"]
        teams = team_generator.generate_teams(player_ids, "skill_balanced")

        assert len(teams) == 2
        assert all(len(team) == 2 for team in teams)

    def test_generate_teams_partnership_balanced(self, team_generator):
        """Test generate_teams with partnership_balanced algorithm."""
        player_ids = ["player1", "player2", "player3", "player4"]
        teams = team_generator.generate_teams(player_ids, "partnership_balanced")

        assert len(teams) == 2
        assert all(len(team) == 2 for team in teams)

    def test_generate_teams_win_rate_balanced(self, team_generator):
        """Test generate_teams with win_rate_balanced algorithm."""
        player_ids = ["player1", "player2", "player3", "player4"]
        teams = team_generator.generate_teams(player_ids, "win_rate_balanced")

        assert len(teams) == 2
        assert all(len(team) == 2 for team in teams)

    def test_generate_teams_invalid_algorithm(self, team_generator):
        """Test generate_teams with invalid algorithm."""
        player_ids = ["player1", "player2", "player3", "player4"]

        with pytest.raises(ValueError, match="Unknown algorithm"):
            team_generator.generate_teams(player_ids, "invalid_algorithm")

    def test_calculate_team_balance_score(self, team_generator):
        """Test team balance score calculation."""
        teams = [["player1", "player2"], ["player3", "player4"]]
        balance_score = team_generator.calculate_team_balance_score(teams)

        assert "skill_variance" in balance_score
        assert "partnership_variance" in balance_score
        assert "overall_score" in balance_score
        assert all(isinstance(score, (int, float)) for score in balance_score.values())

    def test_calculate_team_balance_score_empty_teams(self, team_generator):
        """Test team balance score calculation with empty teams."""
        teams = []
        balance_score = team_generator.calculate_team_balance_score(teams)

        assert balance_score["skill_variance"] == 0
        assert balance_score["partnership_variance"] == 0
        assert balance_score["overall_score"] == 0

    def test_team_generation_consistency(self, team_generator):
        """Test that team generation maintains player assignment consistency."""
        player_ids = ["player1", "player2", "player3", "player4", "player5", "player6"]

        for algorithm in ["random", "skill_balanced", "partnership_balanced", "win_rate_balanced"]:
            teams = team_generator.generate_teams(player_ids, algorithm)

            # Check that all players are assigned exactly once
            all_assigned = [player for team in teams for player in team]
            assert sorted(all_assigned) == sorted(player_ids)

            # Check team sizes
            assert all(len(team) == 2 for team in teams)
            assert len(teams) == len(player_ids) // 2
