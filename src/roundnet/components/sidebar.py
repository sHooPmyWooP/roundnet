"""Sidebar components for the Streamlit app."""

from typing import Any

import streamlit as st

from roundnet.data.manager import get_games, get_players


def render_sidebar() -> dict[str, Any]:
    """Render the sidebar and return selected options."""
    st.sidebar.header("🧭 Navigation")

    # Main navigation
    page = st.sidebar.selectbox(
        "Go to",
        ["🏐 Quick Games", "📊 Dashboard", "👥 Manage Players", "📈 Statistics"],
        key="navigation"
    )

    st.sidebar.markdown("---")

    # Quick stats section
    st.sidebar.header("📊 Quick Stats")

    players = get_players()
    games = get_games()

    st.sidebar.metric("Total Players", len(players))
    st.sidebar.metric("Total Games", len(games))

    # Return all selections
    return {
        "page": page,
    }
