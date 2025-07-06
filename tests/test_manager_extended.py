"""Additional tests for data manager module."""

from datetime import date, timedelta
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from roundnet.data.manager import (
    add_game,
    add_player,
    delete_game,
    delete_player,
    delete_playing_day,
    generate_teams_for_playing_day,
    get_data_manager,
    get_games,
    get_games_for_playing_day,
    get_partnership_stats,
    get_player_by_id,
    get_player_stats,
    get_players,
    get_players_objects,
    get_recent_games,
    initialize_session_state,
    update_player_skill,
)


@pytest.fixture
def mock_data_manager():
    """Mock data manager for testing."""
    mock_dm = MagicMock()

    # Mock player data
    mock_player = MagicMock()
    mock_player.id = "player1"
    mock_player.name = "Alice"
    mock_player.skill_level = 8
    mock_player.to_dict.return_value = {
        "id": "player1",
        "name": "Alice",
        "skill_level": 8,
        "notes": ""
    }

    mock_dm.add_player.return_value = mock_player
    mock_dm.get_players.return_value = [mock_player]
    mock_dm.get_player_by_id.return_value = mock_player

    # Mock playing day data
    mock_playing_day = MagicMock()
    mock_playing_day.id = "day1"
    mock_playing_day.to_dict.return_value = {
        "id": "day1",
        "date": date.today(),
        "location": "Park",
        "description": "Test day"
    }

    mock_dm.add_playing_day.return_value = mock_playing_day
    mock_dm.get_playing_days.return_value = [mock_playing_day]
    mock_dm.get_playing_day_by_id.return_value = mock_playing_day

    # Mock game data
    mock_game = MagicMock()
    mock_game.id = "game1"
    mock_game.to_dict.return_value = {
        "id": "game1",
        "team_a_id": "team1",
        "team_b_id": "team2",
        "score_a": 21,
        "score_b": 19,
        "date": date.today(),
        "playing_day_id": "day1"
    }

    mock_dm.add_game.return_value = mock_game
    mock_dm.get_games.return_value = [mock_game]

    return mock_dm


class TestGetDataManager:
    """Tests for get_data_manager function."""

    @patch('streamlit.session_state')
    @patch('roundnet.data.manager.FileDataManager')
    def test_get_data_manager_creates_new(self, mock_fdm, mock_session_state):
        """Test that get_data_manager creates new instance when none exists."""
        mock_instance = MagicMock()
        mock_fdm.return_value = mock_instance

        # Mock session state as a dict that doesn't have 'data_manager'
        mock_session_state.__contains__.return_value = False

        manager = get_data_manager()

        mock_fdm.assert_called_once()
        assert manager is mock_instance

    @patch('streamlit.session_state')
    def test_get_data_manager_returns_existing(self, mock_session_state):
        """Test that get_data_manager returns existing instance."""
        existing_manager = MagicMock()
        mock_session_state.__contains__.return_value = True
        mock_session_state.data_manager = existing_manager

        manager = get_data_manager()
        assert manager is existing_manager


class TestInitializeSessionState:
    """Tests for initialize_session_state function."""

    @patch('roundnet.data.manager.get_data_manager')
    def test_initialize_session_state(self, mock_get_data_manager):
        """Test that initialize_session_state calls get_data_manager."""
        initialize_session_state()
        mock_get_data_manager.assert_called_once()


class TestPlayerManagement:
    """Tests for player management functions."""

    @patch('roundnet.data.manager.get_data_manager')
    def test_add_player(self, mock_get_dm, mock_data_manager):
        """Test adding a player."""
        mock_get_dm.return_value = mock_data_manager

        player_id = add_player("Alice", 8)

        mock_data_manager.add_player.assert_called_once_with("Alice", 8)
        assert player_id == "player1"

    @patch('roundnet.data.manager.get_data_manager')
    def test_get_players(self, mock_get_dm, mock_data_manager):
        """Test getting all players."""
        mock_get_dm.return_value = mock_data_manager

        players = get_players()

        mock_data_manager.get_players.assert_called_once()
        assert len(players) == 1
        assert players[0]["id"] == "player1"

    @patch('roundnet.data.manager.get_data_manager')
    def test_get_players_objects(self, mock_get_dm, mock_data_manager):
        """Test getting player objects."""
        mock_get_dm.return_value = mock_data_manager

        players = get_players_objects()

        mock_data_manager.get_players.assert_called_once()
        assert len(players) == 1

    @patch('roundnet.data.manager.get_data_manager')
    def test_get_player_by_id(self, mock_get_dm, mock_data_manager):
        """Test getting player by ID."""
        mock_get_dm.return_value = mock_data_manager

        player = get_player_by_id("player1")

        mock_data_manager.get_player_by_id.assert_called_once_with("player1")
        assert player["id"] == "player1"

    @patch('roundnet.data.manager.get_data_manager')
    def test_get_player_by_id_not_found(self, mock_get_dm, mock_data_manager):
        """Test getting non-existent player by ID."""
        mock_data_manager.get_player_by_id.return_value = None
        mock_get_dm.return_value = mock_data_manager

        player = get_player_by_id("nonexistent")

        assert player is None

    @patch('roundnet.data.manager.get_data_manager')
    def test_delete_player(self, mock_get_dm, mock_data_manager):
        """Test deleting a player."""
        mock_get_dm.return_value = mock_data_manager

        delete_player("player1")

        mock_data_manager.delete_player.assert_called_once_with("player1")

    @patch('roundnet.data.manager.get_data_manager')
    def test_update_player_skill(self, mock_get_dm):
        """Test updating player skill level."""
        mock_player = MagicMock()
        mock_player.skill_level = 5

        mock_data_manager = MagicMock()
        mock_data_manager.get_player_by_id.return_value = mock_player
        mock_get_dm.return_value = mock_data_manager

        update_player_skill("player1", 9)

        mock_data_manager.get_player_by_id.assert_called_once_with("player1")
        assert mock_player.skill_level == 9
        mock_data_manager.update_player.assert_called_once_with(mock_player)


class TestPlayingDayManagement:
    """Tests for playing day management functions."""

    @patch('roundnet.data.manager.get_data_manager')
    def test_add_playing_day(self, mock_get_dm, mock_data_manager):
        """Test adding a playing day."""
        mock_get_dm.return_value = mock_data_manager
        test_date = date.today()

        day_id = add_playing_day(test_date, "Park", "Test day")

        mock_data_manager.add_playing_day.assert_called_once_with(test_date, "Park", "Test day")
        assert day_id == "day1"

    @patch('roundnet.data.manager.get_data_manager')
    def test_get_playing_days(self, mock_get_dm, mock_data_manager):
        """Test getting all playing days."""
        mock_get_dm.return_value = mock_data_manager

        days = get_playing_days()

        mock_data_manager.get_playing_days.assert_called_once()
        assert len(days) == 1
        assert days[0]["id"] == "day1"

    @patch('roundnet.data.manager.get_data_manager')
    def test_get_playing_day_by_id(self, mock_get_dm, mock_data_manager):
        """Test getting playing day by ID."""
        mock_get_dm.return_value = mock_data_manager

        day = get_playing_day_by_id("day1")

        mock_data_manager.get_playing_day_by_id.assert_called_once_with("day1")
        assert day["id"] == "day1"

    @patch('roundnet.data.manager.get_data_manager')
    def test_assign_players_to_playing_day(self, mock_get_dm, mock_data_manager):
        """Test assigning players to playing day."""
        mock_get_dm.return_value = mock_data_manager

        assign_players_to_playing_day("day1", ["player1", "player2"])

        mock_data_manager.assign_players_to_playing_day.assert_called_once_with("day1", ["player1", "player2"])

    @patch('roundnet.data.manager.get_data_manager')
    def test_generate_teams_for_playing_day(self, mock_get_dm, mock_data_manager):
        """Test generating teams for playing day."""
        mock_data_manager.generate_teams_for_playing_day.return_value = [["player1", "player2"], ["player3", "player4"]]
        mock_get_dm.return_value = mock_data_manager

        teams = generate_teams_for_playing_day("day1", "random")

        mock_data_manager.generate_teams_for_playing_day.assert_called_once_with("day1", "random")
        assert len(teams) == 2

    @patch('roundnet.data.manager.get_data_manager')
    def test_delete_playing_day(self, mock_get_dm, mock_data_manager):
        """Test deleting a playing day."""
        mock_get_dm.return_value = mock_data_manager

        delete_playing_day("day1")

        mock_data_manager.delete_playing_day.assert_called_once_with("day1")


class TestGameManagement:
    """Tests for game management functions."""

    @patch('roundnet.data.manager.get_data_manager')
    def test_add_game(self, mock_get_dm, mock_data_manager):
        """Test adding a game."""
        mock_get_dm.return_value = mock_data_manager

        game_id = add_game("day1", ["player1", "player2"], ["player3", "player4"], 21, 19)

        mock_data_manager.add_game.assert_called_once()
        assert game_id == "game1"

    @patch('roundnet.data.manager.get_data_manager')
    def test_get_games(self, mock_get_dm, mock_data_manager):
        """Test getting all games."""
        mock_get_dm.return_value = mock_data_manager

        games = get_games()

        mock_data_manager.get_games.assert_called_once()
        assert len(games) == 1
        assert games[0]["id"] == "game1"

    @patch('roundnet.data.manager.get_data_manager')
    def test_get_games_for_playing_day(self, mock_get_dm, mock_data_manager):
        """Test getting games for specific playing day."""
        mock_data_manager.get_games_for_playing_day.return_value = [mock_data_manager.get_games.return_value[0]]
        mock_get_dm.return_value = mock_data_manager

        games = get_games_for_playing_day("day1")

        mock_data_manager.get_games_for_playing_day.assert_called_once_with("day1")
        assert len(games) == 1

    @patch('roundnet.data.manager.get_data_manager')
    def test_delete_game(self, mock_get_dm, mock_data_manager):
        """Test deleting a game."""
        mock_get_dm.return_value = mock_data_manager

        delete_game("game1")

        mock_data_manager.delete_game.assert_called_once_with("game1")


class TestStatistics:
    """Tests for statistics functions."""

    @patch('roundnet.data.manager.get_players_objects')
    def test_get_player_stats(self, mock_get_players_objects):
        """Test getting player statistics."""
        from roundnet.data.models import Player

        mock_player = Player(name="Alice", total_games=5, total_wins=3, skill_level=8)
        mock_get_players_objects.return_value = [mock_player]

        stats = get_player_stats()

        assert isinstance(stats, pd.DataFrame)
        assert len(stats) == 1
        assert 'player_name' in stats.columns
        assert stats.iloc[0]['player_name'] == 'Alice'
        assert stats.iloc[0]['games_played'] == 5
        assert stats.iloc[0]['wins'] == 3

    @patch('roundnet.data.manager.get_data_manager')
    def test_get_recent_games(self, mock_get_dm):
        """Test getting recent games."""
        from roundnet.data.models import Game, PlayingDay

        recent_date = date.today() - timedelta(days=3)
        mock_playing_day = PlayingDay(id="day1", date=recent_date, location="Park")
        mock_game = Game(id="game1", playing_day_id="day1", team_a_player_ids=["player1", "player2"], team_b_player_ids=["player3", "player4"])

        mock_data_manager = MagicMock()
        mock_data_manager.get_recent_playing_days.return_value = [mock_playing_day]
        mock_data_manager.get_games_for_playing_day.return_value = [mock_game]
        mock_get_dm.return_value = mock_data_manager

        recent_games = get_recent_games(7)

        assert len(recent_games) == 1
        assert 'playing_day_date' in recent_games[0]
        assert 'playing_day_location' in recent_games[0]

    @patch('roundnet.data.manager.get_data_manager')
    def test_get_partnership_stats(self, mock_get_dm):
        """Test getting partnership statistics."""
        from roundnet.data.models import Partnership, Player

        mock_partnership = Partnership(player_a_id="p1", player_b_id="p2", times_together=3, wins_together=2)
        mock_player_a = Player(id="p1", name="Alice")
        mock_player_b = Player(id="p2", name="Bob")

        mock_data_manager = MagicMock()
        mock_data_manager.get_partnerships.return_value = [mock_partnership]
        mock_data_manager.get_players.return_value = [mock_player_a, mock_player_b]
        mock_get_dm.return_value = mock_data_manager

        stats = get_partnership_stats()

        assert isinstance(stats, pd.DataFrame)
        assert len(stats) == 1
        assert 'player_a_name' in stats.columns
        assert 'player_b_name' in stats.columns
        assert 'times_together' in stats.columns
