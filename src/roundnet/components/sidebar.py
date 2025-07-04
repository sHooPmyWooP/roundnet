"""Sidebar components for the Streamlit app."""

import streamlit as st
from typing import Dict, Any
from datetime import datetime, date


def render_sidebar() -> Dict[str, Any]:
    """Render the sidebar and return selected options."""
    st.sidebar.header("Controls")

    # Date range selector
    st.sidebar.subheader("Date Range")
    start_date = st.sidebar.date_input(
        "Start Date",
        value=date.today().replace(month=1, day=1),  # Start of current year
        key="start_date"
    )
    end_date = st.sidebar.date_input(
        "End Date",
        value=date.today(),
        key="end_date"
    )

    # Team/Player selector
    st.sidebar.subheader("Filters")
    teams = ["All Teams", "Team Alpha", "Team Beta", "Team Gamma", "Team Delta"]
    selected_team = st.sidebar.selectbox("Select Team", teams)

    players = ["All Players", "Alice", "Bob", "Charlie", "Diana", "Eve"]
    selected_player = st.sidebar.selectbox("Select Player", players)

    # Game type filter
    game_types = ["All Games", "Tournament", "Practice", "Casual"]
    selected_game_type = st.sidebar.multiselect(
        "Game Types",
        game_types,
        default=["Tournament", "Practice"]
    )

    # Additional options
    st.sidebar.subheader("Options")
    show_advanced_stats = st.sidebar.checkbox("Show Advanced Statistics", value=True)
    auto_refresh = st.sidebar.checkbox("Auto Refresh Data", value=False)

    if auto_refresh:
        refresh_interval = st.sidebar.slider(
            "Refresh Interval (seconds)",
            min_value=10,
            max_value=300,
            value=60,
            step=10
        )
    else:
        refresh_interval = None

    # Export options
    st.sidebar.subheader("Export")
    if st.sidebar.button("Export Data"):
        st.sidebar.success("Data exported successfully!")

    # Return all selections
    return {
        "start_date": start_date,
        "end_date": end_date,
        "selected_team": selected_team,
        "selected_player": selected_player,
        "selected_game_types": selected_game_type,
        "show_advanced_stats": show_advanced_stats,
        "auto_refresh": auto_refresh,
        "refresh_interval": refresh_interval,
    }
