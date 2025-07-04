"""Sidebar components for the Streamlit app."""

import streamlit as st
from typing import Dict, Any, Optional
from datetime import datetime, date

from roundnet.data.manager import get_teams, get_players


def render_sidebar() -> Dict[str, Any]:
    """Render the sidebar and return selected options."""
    st.sidebar.header("Navigation")

    # Main navigation
    page = st.sidebar.selectbox(
        "Go to",
        ["Dashboard", "Add Data", "Manage Data", "Statistics"],
        key="navigation"
    )

    st.sidebar.markdown("---")

    # Filters section
    st.sidebar.header("Filters")

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
    teams = get_teams()
    players = get_players()

    team_options = ["All Teams"] + [team['name'] for team in teams]
    selected_team = st.sidebar.selectbox("Select Team", team_options)

    player_options = ["All Players"] + [player['name'] for player in players]
    selected_player = st.sidebar.selectbox("Select Player", player_options)

    # Game type filter
    game_types = ["All Games", "Tournament", "Practice", "Casual", "League"]
    selected_game_types = st.sidebar.multiselect(
        "Game Types",
        game_types[1:],  # Exclude "All Games" from multiselect
        default=["Tournament", "Practice"]
    )

    # If nothing selected, show all
    if not selected_game_types:
        selected_game_types = game_types[1:]

    # Additional options
    st.sidebar.subheader("Display Options")
    show_advanced_stats = st.sidebar.checkbox("Show Advanced Statistics", value=True)

    # Quick stats in sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader("Quick Stats")

    total_teams = len(teams)
    total_players = len(players)

    from roundnet.data.manager import get_games
    games = get_games()
    total_games = len(games)

    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric("Teams", total_teams)
        st.metric("Games", total_games)
    with col2:
        st.metric("Players", total_players)
        if total_games > 0:
            # Calculate recent games (last 7 days)
            from roundnet.data.manager import get_recent_games
            recent = len(get_recent_games(7))
            st.metric("Recent", recent)

    # Return all selections
    return {
        "page": page,
        "start_date": start_date,
        "end_date": end_date,
        "selected_team": selected_team,
        "selected_player": selected_player,
        "selected_game_types": selected_game_types,
        "show_advanced_stats": show_advanced_stats,
    }
