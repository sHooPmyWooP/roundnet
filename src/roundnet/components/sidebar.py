"""Sidebar components for the Streamlit app."""

import streamlit as st
from typing import Dict, Any, Optional
from datetime import datetime, date

from roundnet.data.manager import get_players, get_playing_days


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

    # Quick stats section
    st.sidebar.header("Quick Stats")
    
    players = get_players()
    playing_days = get_playing_days()
    
    st.sidebar.metric("Total Players", len(players))
    st.sidebar.metric("Playing Days", len(playing_days))

    st.sidebar.markdown("---")

    # Filters section (for future use)
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

    # Player selector
    player_options = ["All Players"] + [player['name'] for player in players]
    selected_player = st.sidebar.selectbox("Select Player", player_options)

    # Playing day selector
    playing_day_options = ["All Playing Days"] + [
        f"{pd['date']} - {pd['location']}" if pd['location'] else str(pd['date'])
        for pd in playing_days
    ]
    selected_playing_day = st.sidebar.selectbox("Select Playing Day", playing_day_options)

    # Additional options
    st.sidebar.subheader("Display Options")
    show_advanced_stats = st.sidebar.checkbox("Show Advanced Statistics", value=True)

    # Return all selections
    return {
        "page": page,
        "start_date": start_date,
        "end_date": end_date,
        "selected_player": selected_player,
        "selected_playing_day": selected_playing_day,
        "show_advanced_stats": show_advanced_stats,
    }
