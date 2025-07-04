"""Data processing utilities for the interactive roundnet app."""

from datetime import datetime
from typing import Any

import pandas as pd

# Note: This file has been updated to work with the new interactive data management system.
# Functions now use data from manager.py instead of sample data generators.


def calculate_win_rate(team_id: str) -> float:
    """Calculate win rate for a specific team."""
    from roundnet.data.manager import get_games

    games = get_games()
    team_games = [g for g in games if g['team_a_id'] == team_id or g['team_b_id'] == team_id]

    if len(team_games) == 0:
        return 0.0

    wins = 0
    for game in team_games:
        if game['team_a_id'] == team_id and game['score_a'] > game['score_b']:
            wins += 1
        elif game['team_b_id'] == team_id and game['score_b'] > game['score_a']:
            wins += 1

    return wins / len(team_games)


def get_team_performance_trends(team_id: str, window_size: int = 5) -> pd.DataFrame:
    """Calculate rolling performance trends for a team."""
    from roundnet.data.manager import get_games

    games = get_games()
    team_games = [g for g in games if g['team_a_id'] == team_id or g['team_b_id'] == team_id]

    # Sort by date
    team_games.sort(key=lambda x: x['date'])

    results = []
    for game in team_games:
        if game['team_a_id'] == team_id:
            won = game['score_a'] > game['score_b']
            points_for = game['score_a']
            points_against = game['score_b']
        else:
            won = game['score_b'] > game['score_a']
            points_for = game['score_b']
            points_against = game['score_a']

        results.append({
            "date": game['date'],
            "won": 1 if won else 0,
            "points_for": points_for,
            "points_against": points_against,
        })

    df = pd.DataFrame(results)
    if len(df) > 0:
        df["rolling_win_rate"] = df["won"].rolling(window=window_size, min_periods=1).mean()
        df["rolling_avg_points"] = df["points_for"].rolling(window=window_size, min_periods=1).mean()

    return df


def filter_games_by_date_range(start_date: datetime, end_date: datetime) -> list[dict[str, Any]]:
    """Filter games by date range."""
    from roundnet.data.manager import get_games

    games = get_games()
    filtered_games = []

    for game in games:
        game_date = game['date']
        if isinstance(game_date, str):
            game_date = datetime.strptime(game_date, '%Y-%m-%d').date()

        if start_date <= game_date <= end_date:
            filtered_games.append(game)

    return filtered_games


def get_head_to_head_record(team_a_id: str, team_b_id: str) -> dict[str, Any]:
    """Get head-to-head record between two teams."""
    from roundnet.data.manager import get_games

    games = get_games()
    h2h_games = [
        g for g in games
        if (g['team_a_id'] == team_a_id and g['team_b_id'] == team_b_id) or
           (g['team_a_id'] == team_b_id and g['team_b_id'] == team_a_id)
    ]

    team_a_wins = 0
    team_b_wins = 0
    draws = 0
    total_games = len(h2h_games)

    for game in h2h_games:
        if game['team_a_id'] == team_a_id:
            if game['score_a'] > game['score_b']:
                team_a_wins += 1
            elif game['score_a'] < game['score_b']:
                team_b_wins += 1
            else:
                draws += 1
        else:  # team_a_id is team_b in this game
            if game['score_b'] > game['score_a']:
                team_a_wins += 1
            elif game['score_b'] < game['score_a']:
                team_b_wins += 1
            else:
                draws += 1

    return {
        'total_games': total_games,
        'team_a_wins': team_a_wins,
        'team_b_wins': team_b_wins,
        'draws': draws,
        'team_a_win_rate': team_a_wins / total_games if total_games > 0 else 0,
        'team_b_win_rate': team_b_wins / total_games if total_games > 0 else 0
    }


def get_player_team_contribution(player_id: str) -> dict[str, Any]:
    """Calculate a player's contribution to their team's performance."""
    # NOTE: This function is disabled since we removed the team concept
    return {}

    # Find team stats
    from roundnet.data.manager import get_team_by_id
    team = get_team_by_id(player['team_id'])
    if not team:
        return {}

    team_stat = team_stats_df[team_stats_df['team_name'] == team['name']]
    if team_stat.empty:
        return {}

    stat = team_stat.iloc[0]

    return {
        'player_name': player['name'],
        'team_name': team['name'],
        'team_games': stat['games_played'],
        'team_wins': stat['wins'],
        'team_losses': stat['losses'],
        'team_win_rate': stat['win_rate'],
        'estimated_contribution': stat['win_rate'] * 100  # Simplified contribution score
    }


def generate_summary_stats() -> dict[str, Any]:
    """Generate summary statistics for the dashboard."""
    from roundnet.data.manager import (
        get_games,
        get_players,
        get_recent_games,
        get_teams,
    )

    games = get_games()
    players = get_players()
    teams = get_teams()

    total_games = len(games)
    total_players = len(players)
    total_teams = len(teams)

    # Calculate average game duration
    avg_game_duration = 0
    if games:
        total_duration = sum(game.get('duration_minutes', 30) for game in games)
        avg_game_duration = total_duration / len(games)

    # Get recent activity
    recent_games = get_recent_games(7)
    recent_game_count = len(recent_games)

    # Calculate most active team
    most_active_team = None
    if teams and games:
        team_game_counts = {}
        for team in teams:
            team_id = team['id']
            count = len([g for g in games if g['team_a_id'] == team_id or g['team_b_id'] == team_id])
            team_game_counts[team['name']] = count

        if team_game_counts:
            most_active_team = max(team_game_counts, key=lambda x: team_game_counts[x])

    return {
        "total_games": total_games,
        "total_players": total_players,
        "total_teams": total_teams,
        "avg_game_duration": round(avg_game_duration, 1),
        "recent_games": recent_game_count,
        "most_active_team": most_active_team,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
