"""Main Streamlit application for roundnet analysis."""

import streamlit as st
import pandas as pd
from typing import Optional

from roundnet.components.sidebar import render_sidebar
from roundnet.components.charts import (
    create_games_over_time_chart,
    create_win_rate_chart,
    create_score_distribution_chart,
    create_team_performance_chart
)
from roundnet.components.forms import (
    create_player_form,
    create_team_form,
    create_game_form,
    manage_players_section,
    manage_teams_section,
    manage_games_section
)
from roundnet.config.settings import APP_TITLE, APP_DESCRIPTION
from roundnet.data.manager import (
    initialize_session_state,
    get_team_stats,
    get_player_stats,
    get_recent_games,
    get_teams,
    get_players,
    get_games
)


def show_dashboard():
    """Display the main dashboard."""
    st.header("📊 Dashboard")

    # Get current data for metrics
    teams = get_teams()
    players = get_players()
    games = get_games()
    recent_games = get_recent_games(7)

    # Welcome section for new users
    if not teams and not players and not games:
        st.info("👋 **Welcome to Roundnet Analytics!** Start by adding teams and players, then record some games to see your statistics here.")

        # Offer to create sample data
        st.subheader("🚀 Quick Start")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("📚 Create Sample Data", help="Add some sample teams, players, and games to explore the app"):
                from roundnet.data.loader import create_sample_teams_and_games
                create_sample_teams_and_games()
                st.success("Sample data created! Refresh the page or navigate to see the changes.")
                st.rerun()

        with col2:
            if st.button("➕ Start Fresh", help="Begin by adding your own teams and players"):
                st.info("💡 Use the sidebar to navigate to 'Add Data' to start adding your teams and players!")

        return

    # Top metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Teams", len(teams))
    with col2:
        st.metric("Total Players", len(players))
    with col3:
        st.metric("Total Games", len(games))
    with col4:
        st.metric("Games This Week", len(recent_games))

    # Charts section
    st.subheader("📈 Analytics")

    col1, col2 = st.columns(2)

    with col1:
        # Games over time chart
        games_chart = create_games_over_time_chart()
        st.plotly_chart(games_chart, use_container_width=True)

        # Score distribution
        score_chart = create_score_distribution_chart()
        st.plotly_chart(score_chart, use_container_width=True)

    with col2:
        # Win rate chart
        winrate_chart = create_win_rate_chart()
        st.plotly_chart(winrate_chart, use_container_width=True)

        # Team performance overview
        performance_chart = create_team_performance_chart()
        st.plotly_chart(performance_chart, use_container_width=True)

    # Recent activity
    st.subheader("🏐 Recent Activity")

    if recent_games:
        for game in recent_games[:5]:  # Show last 5 games
            game_date = game['date']
            if hasattr(game_date, 'strftime'):
                date_str = game_date.strftime('%Y-%m-%d')
            else:
                date_str = str(game_date)

            winner_emoji = "🏆" if game['score_a'] != game['score_b'] else "🤝"

            if game['score_a'] > game['score_b']:
                result_text = f"{winner_emoji} **{game['team_a_name']}** defeated {game['team_b_name']} ({game['score_a']}-{game['score_b']})"
            elif game['score_b'] > game['score_a']:
                result_text = f"{winner_emoji} **{game['team_b_name']}** defeated {game['team_a_name']} ({game['score_b']}-{game['score_a']})"
            else:
                result_text = f"{winner_emoji} **{game['team_a_name']}** and **{game['team_b_name']}** tied ({game['score_a']}-{game['score_b']})"

            st.info(f"{date_str}: {result_text}")
    else:
        st.info("No recent games to display.")


def show_add_data():
    """Display forms for adding new data."""
    st.header("➕ Add New Data")

    tab1, tab2, tab3 = st.tabs(["🏐 Add Team", "👤 Add Player", "🎯 Add Game"])

    with tab1:
        create_team_form()

    with tab2:
        create_player_form()

    with tab3:
        create_game_form()


def show_manage_data():
    """Display management interface for existing data."""
    st.header("⚙️ Manage Data")

    tab1, tab2, tab3 = st.tabs(["👥 Manage Players", "🏐 Manage Teams", "📊 Manage Games"])

    with tab1:
        manage_players_section()

    with tab2:
        manage_teams_section()

    with tab3:
        manage_games_section()


def show_statistics():
    """Display detailed statistics."""
    st.header("📊 Detailed Statistics")

    # Team statistics
    st.subheader("🏐 Team Statistics")
    team_stats = get_team_stats()

    if not team_stats.empty:
        st.dataframe(
            team_stats,
            use_container_width=True,
            column_config={
                "win_rate": st.column_config.NumberColumn(
                    "Win Rate",
                    format="%.1%"
                ),
                "point_differential": st.column_config.NumberColumn(
                    "Point Differential",
                    format="%+d"
                )
            }
        )
    else:
        st.info("No team statistics available yet. Add some teams and games to see statistics.")

    # Player statistics
    st.subheader("👤 Player Statistics")
    player_stats = get_player_stats()

    if not player_stats.empty:
        st.dataframe(
            player_stats,
            use_container_width=True,
            column_config={
                "win_rate": st.column_config.NumberColumn(
                    "Win Rate",
                    format="%.1%"
                )
            }
        )
    else:
        st.info("No player statistics available yet. Add some players and assign them to teams.")


def main() -> None:
    """Main function to run the Streamlit app."""
    # Initialize session state
    initialize_session_state()

    # Page configuration
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon="🏐",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # App header
    st.title(APP_TITLE)
    st.markdown(APP_DESCRIPTION)

    # Sidebar
    sidebar_data = render_sidebar()

    # Main content based on navigation
    page = sidebar_data.get("page", "Dashboard")

    if page == "Dashboard":
        show_dashboard()
    elif page == "Add Data":
        show_add_data()
    elif page == "Manage Data":
        show_manage_data()
    elif page == "Statistics":
        show_statistics()

    # Footer
    st.markdown("---")
    st.markdown("Built with ❤️ using Streamlit | 🏐 Interactive Roundnet Management")


if __name__ == "__main__":
    main()
