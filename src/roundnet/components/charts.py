"""Chart components for data visualization."""

from datetime import datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from roundnet.config.settings import DEFAULT_CHART_HEIGHT
from roundnet.data.manager import get_games, get_team_stats


def create_games_over_time_chart() -> go.Figure:
    """Create a chart showing games played over time."""
    games = get_games()

    if not games:
        # Return empty chart
        fig = go.Figure()
        fig.add_annotation(
            text="No games recorded yet",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font={"size": 16}
        )
        fig.update_layout(
            title="Games Over Time",
            height=DEFAULT_CHART_HEIGHT,
            xaxis_title="Date",
            yaxis_title="Number of Games"
        )
        return fig

    # Convert games to DataFrame for easier processing
    game_dates = []
    for game in games:
        game_date = game['date']
        if isinstance(game_date, str):
            game_date = datetime.strptime(game_date, '%Y-%m-%d').date()
        game_dates.append(game_date)

    # Count games by date
    date_counts = pd.Series(game_dates).value_counts().sort_index()

    # Create cumulative sum for total games over time
    cumulative_games = date_counts.cumsum()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=cumulative_games.index,
        y=cumulative_games.values,
        mode="lines+markers",
        name="Total Games",
        line={"color": "#2E8B57", "width": 3},
        marker={"size": 6}
    ))

    fig.update_layout(
        title="Cumulative Games Over Time",
        xaxis_title="Date",
        yaxis_title="Total Games",
        height=DEFAULT_CHART_HEIGHT,
        hovermode="x unified",
        showlegend=True
    )

    return fig


def create_win_rate_chart() -> go.Figure:
    """Create a win rate chart for all teams."""
    team_stats = get_team_stats()

    if team_stats.empty:
        # Return empty chart
        fig = go.Figure()
        fig.add_annotation(
            text="No team data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font={"size": 16}
        )
        fig.update_layout(
            title="Team Win Rates",
            height=DEFAULT_CHART_HEIGHT,
            xaxis_title="Team",
            yaxis_title="Win Rate"
        )
        return fig

    fig = go.Figure(data=[
        go.Bar(
            x=team_stats['team_name'],
            y=team_stats['win_rate'],
            marker_color=px.colors.qualitative.Set3,
            text=[f"{rate:.1%}" for rate in team_stats['win_rate']],
            textposition="auto"
        )
    ])

    fig.update_layout(
        title="Team Win Rates",
        xaxis_title="Team",
        yaxis_title="Win Rate",
        height=DEFAULT_CHART_HEIGHT,
        yaxis={"tickformat": ".0%"}
    )

    return fig


def create_score_distribution_chart() -> go.Figure:
    """Create a score distribution chart from actual game data."""
    games = get_games()

    if not games:
        # Return empty chart
        fig = go.Figure()
        fig.add_annotation(
            text="No game data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font={"size": 16}
        )
        fig.update_layout(
            title="Score Distribution",
            height=DEFAULT_CHART_HEIGHT,
            xaxis_title="Score",
            yaxis_title="Frequency"
        )
        return fig

    # Collect all scores
    all_scores = []
    for game in games:
        all_scores.extend([game['score_a'], game['score_b']])

    if not all_scores:
        return create_score_distribution_chart()  # Return empty chart

    fig = go.Figure(data=[
        go.Histogram(
            x=all_scores,
            nbinsx=max(10, len(set(all_scores))),
            marker_color="#4CAF50",
            opacity=0.7
        )
    ])

    fig.update_layout(
        title="Score Distribution",
        xaxis_title="Score",
        yaxis_title="Frequency",
        height=DEFAULT_CHART_HEIGHT
    )

    return fig


def create_team_performance_chart() -> go.Figure:
    """Create a comprehensive team performance chart."""
    team_stats = get_team_stats()

    if team_stats.empty:
        # Return empty chart
        fig = go.Figure()
        fig.add_annotation(
            text="No team performance data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font={"size": 16}
        )
        fig.update_layout(
            title="Team Performance Overview",
            height=DEFAULT_CHART_HEIGHT
        )
        return fig

    fig = go.Figure()

    # Add wins
    fig.add_trace(go.Bar(
        name='Wins',
        x=team_stats['team_name'],
        y=team_stats['wins'],
        marker_color='#2E8B57'
    ))

    # Add losses
    fig.add_trace(go.Bar(
        name='Losses',
        x=team_stats['team_name'],
        y=team_stats['losses'],
        marker_color='#DC143C'
    ))

    # Add draws if any
    if 'draws' in team_stats.columns and team_stats['draws'].sum() > 0:
        fig.add_trace(go.Bar(
            name='Draws',
            x=team_stats['team_name'],
            y=team_stats['draws'],
            marker_color='#FFD700'
        ))

    fig.update_layout(
        title='Team Performance Overview',
        xaxis_title='Team',
        yaxis_title='Number of Games',
        barmode='stack',
        height=DEFAULT_CHART_HEIGHT
    )

    return fig


def create_player_performance_radar(player_stats: dict[str, float]) -> go.Figure:
    """Create a radar chart for player performance."""
    categories = list(player_stats.keys())
    values = list(player_stats.values())

    # Close the radar chart
    categories.append(categories[0])
    values.append(values[0])

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Performance',
        line_color='#FF6B6B'
    ))

    fig.update_layout(
        polar={
            "radialaxis": {
                "visible": True,
                "range": [0, 100]
            }},
        showlegend=False,
        title="Player Performance Radar",
        height=DEFAULT_CHART_HEIGHT
    )

    return fig
