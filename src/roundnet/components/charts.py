"""Chart components for data visualization."""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, Any
import numpy as np

from roundnet.config.settings import DEFAULT_CHART_HEIGHT


def create_sample_chart() -> go.Figure:
    """Create a sample chart for demonstration."""
    # Generate sample data
    dates = pd.date_range(start="2024-01-01", end="2024-12-31", freq="W")
    wins = np.random.poisson(3, len(dates))
    losses = np.random.poisson(2, len(dates))

    df = pd.DataFrame({
        "Date": dates,
        "Wins": wins,
        "Losses": losses,
        "Games": wins + losses
    })

    # Create the chart
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["Date"],
        y=df["Wins"],
        mode="lines+markers",
        name="Wins",
        line=dict(color="#2E8B57", width=3),
        marker=dict(size=6)
    ))

    fig.add_trace(go.Scatter(
        x=df["Date"],
        y=df["Losses"],
        mode="lines+markers",
        name="Losses",
        line=dict(color="#DC143C", width=3),
        marker=dict(size=6)
    ))

    fig.update_layout(
        title="Games Won vs Lost Over Time",
        xaxis_title="Date",
        yaxis_title="Number of Games",
        height=DEFAULT_CHART_HEIGHT,
        hovermode="x unified",
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig


def create_win_rate_chart(data: Dict[str, Any]) -> go.Figure:
    """Create a win rate chart."""
    # Sample data - replace with actual data processing
    teams = ["Team Alpha", "Team Beta", "Team Gamma", "Team Delta"]
    win_rates = [0.75, 0.68, 0.82, 0.59]

    fig = go.Figure(data=[
        go.Bar(
            x=teams,
            y=win_rates,
            marker_color=px.colors.qualitative.Set3,
            text=[f"{rate:.1%}" for rate in win_rates],
            textposition="auto"
        )
    ])

    fig.update_layout(
        title="Team Win Rates",
        xaxis_title="Team",
        yaxis_title="Win Rate",
        height=DEFAULT_CHART_HEIGHT,
        yaxis=dict(tickformat=".0%")
    )

    return fig


def create_score_distribution_chart(data: Dict[str, Any]) -> go.Figure:
    """Create a score distribution chart."""
    # Sample data
    scores = np.random.normal(15, 3, 1000)
    scores = scores[scores > 0]  # Remove negative scores

    fig = go.Figure(data=[
        go.Histogram(
            x=scores,
            nbinsx=20,
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


def create_player_performance_radar(player_stats: Dict[str, float]) -> go.Figure:
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
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=False,
        title="Player Performance Radar",
        height=DEFAULT_CHART_HEIGHT
    )

    return fig
