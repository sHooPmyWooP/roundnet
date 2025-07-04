"""Data management for in-memory storage of players, teams, and games."""

import streamlit as st
import pandas as pd
from datetime import datetime, date
from typing import Dict, List, Any, Optional
import uuid


def initialize_session_state():
    """Initialize session state for data storage."""
    if 'players' not in st.session_state:
        st.session_state.players = []

    if 'teams' not in st.session_state:
        st.session_state.teams = []

    if 'games' not in st.session_state:
        st.session_state.games = []


def add_player(name: str, team_id: Optional[str] = None) -> str:
    """Add a new player."""
    player_id = str(uuid.uuid4())
    player = {
        'id': player_id,
        'name': name,
        'team_id': team_id,
        'created_at': datetime.now()
    }
    st.session_state.players.append(player)
    return player_id


def add_team(name: str, description: str = "") -> str:
    """Add a new team."""
    team_id = str(uuid.uuid4())
    team = {
        'id': team_id,
        'name': name,
        'description': description,
        'created_at': datetime.now()
    }
    st.session_state.teams.append(team)
    return team_id


def add_game(team_a_id: str, team_b_id: str, score_a: int, score_b: int,
             game_date: date, duration_minutes: int = 30, location: str = "",
             game_type: str = "Practice") -> str:
    """Add a new game result."""
    game_id = str(uuid.uuid4())
    game = {
        'id': game_id,
        'team_a_id': team_a_id,
        'team_b_id': team_b_id,
        'score_a': score_a,
        'score_b': score_b,
        'date': game_date,
        'duration_minutes': duration_minutes,
        'location': location,
        'game_type': game_type,
        'winner_id': team_a_id if score_a > score_b else team_b_id if score_b > score_a else None,
        'created_at': datetime.now()
    }
    st.session_state.games.append(game)
    return game_id


def get_players() -> List[Dict[str, Any]]:
    """Get all players."""
    return st.session_state.players


def get_teams() -> List[Dict[str, Any]]:
    """Get all teams."""
    return st.session_state.teams


def get_games() -> List[Dict[str, Any]]:
    """Get all games."""
    return st.session_state.games


def get_team_by_id(team_id: str) -> Optional[Dict[str, Any]]:
    """Get team by ID."""
    for team in st.session_state.teams:
        if team['id'] == team_id:
            return team
    return None


def get_player_by_id(player_id: str) -> Optional[Dict[str, Any]]:
    """Get player by ID."""
    for player in st.session_state.players:
        if player['id'] == player_id:
            return player
    return None


def update_player_team(player_id: str, team_id: Optional[str]):
    """Update a player's team assignment."""
    for player in st.session_state.players:
        if player['id'] == player_id:
            player['team_id'] = team_id
            break


def delete_player(player_id: str):
    """Delete a player."""
    st.session_state.players = [p for p in st.session_state.players if p['id'] != player_id]


def delete_team(team_id: str):
    """Delete a team and remove team assignment from players."""
    st.session_state.teams = [t for t in st.session_state.teams if t['id'] != team_id]
    # Remove team assignment from players
    for player in st.session_state.players:
        if player['team_id'] == team_id:
            player['team_id'] = None


def delete_game(game_id: str):
    """Delete a game."""
    st.session_state.games = [g for g in st.session_state.games if g['id'] != game_id]


def get_team_stats() -> pd.DataFrame:
    """Calculate team statistics."""
    teams = get_teams()
    games = get_games()

    if not teams:
        return pd.DataFrame()

    stats = []
    for team in teams:
        team_id = team['id']
        team_games = [g for g in games if g['team_a_id'] == team_id or g['team_b_id'] == team_id]

        wins = 0
        losses = 0
        draws = 0
        points_for = 0
        points_against = 0

        for game in team_games:
            if game['team_a_id'] == team_id:
                points_for += game['score_a']
                points_against += game['score_b']
                if game['score_a'] > game['score_b']:
                    wins += 1
                elif game['score_a'] < game['score_b']:
                    losses += 1
                else:
                    draws += 1
            else:
                points_for += game['score_b']
                points_against += game['score_a']
                if game['score_b'] > game['score_a']:
                    wins += 1
                elif game['score_b'] < game['score_a']:
                    losses += 1
                else:
                    draws += 1

        total_games = wins + losses + draws
        win_rate = wins / total_games if total_games > 0 else 0

        stats.append({
            'team_name': team['name'],
            'games_played': total_games,
            'wins': wins,
            'losses': losses,
            'draws': draws,
            'win_rate': win_rate,
            'points_for': points_for,
            'points_against': points_against,
            'point_differential': points_for - points_against
        })

    return pd.DataFrame(stats).sort_values('win_rate', ascending=False)


def get_player_stats() -> pd.DataFrame:
    """Calculate player statistics based on their team's performance."""
    players = get_players()
    teams = get_teams()
    team_stats_df = get_team_stats()

    if not players or team_stats_df.empty:
        return pd.DataFrame()

    player_stats = []
    for player in players:
        team_id = player.get('team_id')
        if team_id:
            team = get_team_by_id(team_id)
            if team:
                team_stat = team_stats_df[team_stats_df['team_name'] == team['name']]
                if not team_stat.empty:
                    stat = team_stat.iloc[0]
                    player_stats.append({
                        'player_name': player['name'],
                        'team_name': team['name'],
                        'games_played': stat['games_played'],
                        'wins': stat['wins'],
                        'losses': stat['losses'],
                        'win_rate': stat['win_rate']
                    })
                else:
                    player_stats.append({
                        'player_name': player['name'],
                        'team_name': team['name'],
                        'games_played': 0,
                        'wins': 0,
                        'losses': 0,
                        'win_rate': 0
                    })
        else:
            player_stats.append({
                'player_name': player['name'],
                'team_name': 'No Team',
                'games_played': 0,
                'wins': 0,
                'losses': 0,
                'win_rate': 0
            })

    return pd.DataFrame(player_stats)


def get_recent_games(days: int = 7) -> List[Dict[str, Any]]:
    """Get games from the last N days."""
    games = get_games()
    recent_date = datetime.now().date() - pd.Timedelta(days=days)

    recent_games = []
    for game in games:
        game_date = game['date']
        if isinstance(game_date, str):
            game_date = datetime.strptime(game_date, '%Y-%m-%d').date()

        if game_date >= recent_date:
            # Add team names
            team_a = get_team_by_id(game['team_a_id'])
            team_b = get_team_by_id(game['team_b_id'])

            game_with_names = game.copy()
            game_with_names['team_a_name'] = team_a['name'] if team_a else 'Unknown Team'
            game_with_names['team_b_name'] = team_b['name'] if team_b else 'Unknown Team'
            recent_games.append(game_with_names)

    return sorted(recent_games, key=lambda x: x['date'], reverse=True)
