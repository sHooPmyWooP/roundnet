"""Data processing utilities."""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime, timedelta

from roundnet.data.loader import load_sample_data, load_player_data


def calculate_win_rate(games_df: pd.DataFrame, team_name: str) -> float:
    """Calculate win rate for a specific team."""
    team_games = games_df[
        (games_df["team_a"] == team_name) | (games_df["team_b"] == team_name)
    ]

    if len(team_games) == 0:
        return 0.0

    wins = 0
    for _, game in team_games.iterrows():
        if game["team_a"] == team_name and game["score_a"] > game["score_b"]:
            wins += 1
        elif game["team_b"] == team_name and game["score_b"] > game["score_a"]:
            wins += 1

    return wins / len(team_games)


def get_team_statistics(games_df: pd.DataFrame) -> pd.DataFrame:
    """Calculate comprehensive statistics for all teams."""
    teams = set(games_df["team_a"].unique()) | set(games_df["team_b"].unique())

    stats = []
    for team in teams:
        team_games = games_df[
            (games_df["team_a"] == team) | (games_df["team_b"] == team)
        ]

        wins = 0
        losses = 0
        points_for = 0
        points_against = 0

        for _, game in team_games.iterrows():
            if game["team_a"] == team:
                points_for += game["score_a"]
                points_against += game["score_b"]
                if game["score_a"] > game["score_b"]:
                    wins += 1
                else:
                    losses += 1
            else:
                points_for += game["score_b"]
                points_against += game["score_a"]
                if game["score_b"] > game["score_a"]:
                    wins += 1
                else:
                    losses += 1

        total_games = wins + losses
        win_rate = wins / total_games if total_games > 0 else 0
        avg_points_for = points_for / total_games if total_games > 0 else 0
        avg_points_against = points_against / total_games if total_games > 0 else 0

        stats.append({
            "team": team,
            "games_played": total_games,
            "wins": wins,
            "losses": losses,
            "win_rate": win_rate,
            "points_for": points_for,
            "points_against": points_against,
            "avg_points_for": avg_points_for,
            "avg_points_against": avg_points_against,
            "point_differential": points_for - points_against,
        })

    return pd.DataFrame(stats).sort_values("win_rate", ascending=False)


def filter_games_by_date(games_df: pd.DataFrame, start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """Filter games by date range."""
    games_df["date"] = pd.to_datetime(games_df["date"])
    return games_df[
        (games_df["date"] >= start_date) & (games_df["date"] <= end_date)
    ]


def get_recent_games(games_df: pd.DataFrame, days: int = 7) -> pd.DataFrame:
    """Get games from the last N days."""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    return filter_games_by_date(games_df, start_date, end_date)


def calculate_player_stats(games_df: pd.DataFrame, player_df: pd.DataFrame) -> pd.DataFrame:
    """Calculate detailed player statistics."""
    # This is a simplified version - in a real app, you'd have more detailed game records
    stats = []

    for _, player in player_df.iterrows():
        team = player["team"]

        # Get games for this player's team
        team_games = games_df[
            (games_df["team_a"] == team) | (games_df["team_b"] == team)
        ]

        wins = 0
        total_games = len(team_games)

        for _, game in team_games.iterrows():
            if game["team_a"] == team and game["score_a"] > game["score_b"]:
                wins += 1
            elif game["team_b"] == team and game["score_b"] > game["score_a"]:
                wins += 1

        win_rate = wins / total_games if total_games > 0 else 0

        # Calculate performance metrics (sample calculations)
        attack_rating = min(95, 60 + (win_rate * 30) + np.random.normal(0, 5))
        defense_rating = min(95, 55 + (win_rate * 25) + np.random.normal(0, 5))
        consistency = min(95, 65 + (win_rate * 20) + np.random.normal(0, 3))
        teamwork = min(95, 70 + (win_rate * 15) + np.random.normal(0, 4))

        stats.append({
            "player_name": player["name"],
            "team": team,
            "games_played": total_games,
            "wins": wins,
            "losses": total_games - wins,
            "win_rate": win_rate,
            "attack_rating": max(0, attack_rating),
            "defense_rating": max(0, defense_rating),
            "consistency": max(0, consistency),
            "teamwork": max(0, teamwork),
        })

    return pd.DataFrame(stats)


def get_performance_trends(games_df: pd.DataFrame, team_name: str, window_size: int = 5) -> pd.DataFrame:
    """Calculate rolling performance trends for a team."""
    team_games = games_df[
        (games_df["team_a"] == team_name) | (games_df["team_b"] == team_name)
    ].sort_values("date")

    results = []
    for _, game in team_games.iterrows():
        if game["team_a"] == team_name:
            won = game["score_a"] > game["score_b"]
            points_for = game["score_a"]
            points_against = game["score_b"]
        else:
            won = game["score_b"] > game["score_a"]
            points_for = game["score_b"]
            points_against = game["score_a"]

        results.append({
            "date": game["date"],
            "won": 1 if won else 0,
            "points_for": points_for,
            "points_against": points_against,
        })

    df = pd.DataFrame(results)
    if len(df) > 0:
        df["rolling_win_rate"] = df["won"].rolling(window=window_size, min_periods=1).mean()
        df["rolling_avg_points"] = df["points_for"].rolling(window=window_size, min_periods=1).mean()

    return df


def generate_summary_stats() -> Dict[str, Any]:
    """Generate summary statistics for the dashboard."""
    games_df = load_sample_data()
    player_df = load_player_data()

    total_games = len(games_df)
    total_players = len(player_df)
    avg_game_duration = games_df["duration_minutes"].mean()

    # Get recent activity
    recent_games = get_recent_games(games_df, days=7)
    recent_game_count = len(recent_games)

    return {
        "total_games": total_games,
        "total_players": total_players,
        "avg_game_duration": avg_game_duration,
        "recent_games": recent_game_count,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
