"""Data management for the roundnet application using file-based persistence."""

from datetime import date
from typing import Any

import pandas as pd
import streamlit as st

from roundnet.data.file_manager import FileDataManager
from roundnet.data.models import Player


def get_data_manager() -> FileDataManager:
    """Get or create the file data manager."""
    if 'data_manager' not in st.session_state:
        st.session_state.data_manager = FileDataManager()
    return st.session_state.data_manager


def initialize_session_state() -> None:
    """Initialize session state for data storage."""
    # Just ensure the data manager is created
    get_data_manager()


# Player management functions
def add_player(name: str, skill_level: int = 5) -> str:
    """Add a new player."""
    dm = get_data_manager()
    player = dm.add_player(name, skill_level)
    return player.id


def get_players() -> list[dict[str, Any]]:
    """Get all players as dictionaries for compatibility."""
    dm = get_data_manager()
    players = dm.get_players()
    return [p.to_dict() for p in players]


def get_players_objects() -> list[Player]:
    """Get all players as Player objects."""
    dm = get_data_manager()
    return dm.get_players()


def get_player_by_id(player_id: str) -> dict[str, Any] | None:
    """Get player by ID as dictionary."""
    dm = get_data_manager()
    player = dm.get_player_by_id(player_id)
    return player.to_dict() if player else None


def delete_player(player_id: str) -> None:
    """Delete a player."""
    dm = get_data_manager()
    dm.delete_player(player_id)


def update_player_skill(player_id: str, skill_level: int) -> None:
    """Update a player's skill level."""
    dm = get_data_manager()
    player = dm.get_player_by_id(player_id)
    if player:
        player.skill_level = skill_level
        dm.update_player(player)


# Playing day management functions
def add_playing_day(play_date: date, location: str = "", description: str = "") -> str:
    """Add a new playing day."""
    dm = get_data_manager()
    playing_day = dm.add_playing_day(play_date, location, description)
    return playing_day.id


def get_playing_days() -> list[dict[str, Any]]:
    """Get all playing days as dictionaries."""
    dm = get_data_manager()
    playing_days = dm.get_playing_days()
    return [pd.to_dict() for pd in playing_days]


def get_playing_day_by_id(playing_day_id: str) -> dict[str, Any] | None:
    """Get playing day by ID as dictionary."""
    dm = get_data_manager()
    playing_day = dm.get_playing_day_by_id(playing_day_id)
    return playing_day.to_dict() if playing_day else None


def assign_players_to_playing_day(playing_day_id: str, player_ids: list[str]) -> None:
    """Assign players to a playing day."""
    dm = get_data_manager()
    dm.assign_players_to_playing_day(playing_day_id, player_ids)


def generate_teams_for_playing_day(playing_day_id: str, algorithm: str = "random") -> list[list[str]]:
    """Generate teams for a playing day."""
    dm = get_data_manager()
    return dm.generate_teams_for_playing_day(playing_day_id, algorithm)


def delete_playing_day(playing_day_id: str) -> None:
    """Delete a playing day."""
    dm = get_data_manager()
    dm.delete_playing_day(playing_day_id)


# Game management functions
def add_game(playing_day_id: str, team_a_player_ids: list[str], team_b_player_ids: list[str],
             team_a_wins: bool = False, team_b_wins: bool = False, is_tie: bool = False,
             duration_minutes: int = 30, notes: str = "") -> str:
    """Add a new game."""
    dm = get_data_manager()
    game = dm.add_game(playing_day_id, team_a_player_ids, team_b_player_ids,
                       team_a_wins, team_b_wins, is_tie, duration_minutes, notes)
    return game.id


def get_games() -> list[dict[str, Any]]:
    """Get all games as dictionaries."""
    dm = get_data_manager()
    games = dm.get_games()
    return [g.to_dict() for g in games]


def get_games_for_playing_day(playing_day_id: str) -> list[dict[str, Any]]:
    """Get games for a specific playing day."""
    dm = get_data_manager()
    games = dm.get_games_for_playing_day(playing_day_id)
    return [g.to_dict() for g in games]


def delete_game(game_id: str) -> None:
    """Delete a game."""
    dm = get_data_manager()
    dm.delete_game(game_id)


# Statistics functions
def get_player_stats() -> pd.DataFrame:
    """Calculate player statistics."""
    players = get_players_objects()

    if not players:
        return pd.DataFrame()

    stats = []
    for player in players:
        stats.append({
            'player_name': player.name,
            'games_played': player.total_games,
            'wins': player.total_wins,
            'losses': player.total_games - player.total_wins,
            'win_rate': player.win_rate,
            'skill_level': player.skill_level
        })

    return pd.DataFrame(stats).sort_values('win_rate', ascending=False)


def get_recent_games(days: int = 7) -> list[dict[str, Any]]:
    """Get games from recent playing days."""
    dm = get_data_manager()
    recent_playing_days = dm.get_recent_playing_days(days)

    all_recent_games = []
    for playing_day in recent_playing_days:
        games = dm.get_games_for_playing_day(playing_day.id)
        for game in games:
            game_dict = game.to_dict()
            game_dict['playing_day_date'] = playing_day.date
            game_dict['playing_day_location'] = playing_day.location
            all_recent_games.append(game_dict)

    return sorted(all_recent_games, key=lambda x: x['playing_day_date'], reverse=True)


def get_partnership_stats() -> pd.DataFrame:
    """Get partnership statistics."""
    dm = get_data_manager()
    partnerships = dm.get_partnerships()
    players = {p.id: p for p in dm.get_players()}

    if not partnerships:
        return pd.DataFrame()

    stats = []
    for partnership in partnerships:
        player_a = players.get(partnership.player_a_id)
        player_b = players.get(partnership.player_b_id)

        if player_a and player_b:
            stats.append({
                'player_a_name': player_a.name,
                'player_b_name': player_b.name,
                'times_together': partnership.times_together,
                'wins_together': partnership.wins_together,
                'win_rate_together': partnership.win_rate_together
            })

    return pd.DataFrame(stats).sort_values('times_together', ascending=False)


# Legacy compatibility functions (for existing code)
def get_teams() -> list[dict[str, Any]]:
    """Legacy function - returns empty list since we don't use teams anymore."""
    return []


def get_team_stats() -> pd.DataFrame:
    """Legacy function - returns empty DataFrame since we don't use teams anymore."""
    return pd.DataFrame()


def add_team(name: str, description: str = "") -> str:
    """Legacy function - not implemented in new system."""
    st.warning("Teams are no longer used in this system. Please use Playing Days instead.")
    return ""


def get_team_by_id(team_id: str) -> dict[str, Any] | None:
    """Legacy function - returns None since we don't use teams anymore."""
    return None
