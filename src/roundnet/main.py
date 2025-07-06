"""Main Streamlit application for roundnet game management and tracking."""

from datetime import datetime

import streamlit as st

from roundnet.components.forms import (
    create_game_form,
    create_player_form,
    generate_teams_interface,
    manage_current_players,
    manage_players_section,
    quick_game_interface,
)
from roundnet.components.sidebar import render_sidebar
from roundnet.config.settings import APP_DESCRIPTION, APP_TITLE
from roundnet.data.manager import (
    get_partnership_stats,
    get_player_by_id,
    get_player_stats,
    get_players,
    get_recent_games,
    initialize_session_state,
)


def show_quick_games() -> None:
    """Display the quick game creation interface - the new main page."""
    st.header("🏐 Quick Game Setup")

    players = get_players()

    if len(players) < 4:
        st.warning("⚠️ You need at least 4 players to create games.")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("➕ Add Players", help="Navigate to add new players"):
                st.session_state.navigation = "Manage Players"
                st.rerun()

        with col2:
            if st.button(
                "📚 Create Sample Data", help="Add sample players to get started"
            ):
                from roundnet.data.loader import create_sample_data

                create_sample_data()
                st.success("Sample data created!")
                st.rerun()
        return

    # Quick game interface
    quick_game_interface()


def show_dashboard() -> None:
    """Display the main dashboard."""
    st.header("📊 Dashboard")

    # Get current data for metrics
    players = get_players()
    recent_games = get_recent_games(7)

    # Welcome section for new users
    if not players:
        st.info(
            "👋 **Welcome to Roundnet Player Management!** Start by adding players."
        )

        # Offer to create sample data
        st.subheader("🚀 Quick Start")
        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                "📚 Create Sample Data", help="Add some sample players and games"
            ):
                from roundnet.data.loader import create_sample_data

                create_sample_data()
                st.success(
                    "Sample data created! Refresh the page or navigate to see the changes."
                )
                st.rerun()

        with col2:
            if st.button("➕ Start Fresh", help="Begin by adding your own players"):
                st.info(
                    "💡 Use the sidebar to navigate to 'Add Data' to start adding players!"
                )

        return

    # Top metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Players", len(players))
    with col2:
        from roundnet.data.manager import get_games

        all_games = get_games()
        st.metric("Total Games", len(all_games))
    with col3:
        st.metric("Recent Games", len(recent_games))

    # Player statistics section
    st.subheader("🏆 Player Performance")
    player_stats = get_player_stats()

    if not player_stats.empty:
        # Show top performers
        col1, col2 = st.columns(2)

        with col1:
            st.write("**Top Players by Win Rate:**")
            top_players = player_stats.head(5)
            for _, player in top_players.iterrows():
                if player["games_played"] > 0:
                    st.write(
                        f"🏆 {player['player_name']}: {player['win_rate']:.1%} ({player['wins']}/{player['games_played']})"
                    )

        with col2:
            st.write("**Most Active Players:**")
            most_active = player_stats.nlargest(5, "games_played")
            for _, player in most_active.iterrows():
                st.write(f"🎯 {player['player_name']}: {player['games_played']} games")

    # Partnership statistics
    partnership_stats = get_partnership_stats()
    if not partnership_stats.empty:
        st.subheader("🤝 Partnership Statistics")
        col1, col2 = st.columns(2)

        with col1:
            st.write("**Most Frequent Partnerships:**")
            top_partnerships = partnership_stats.head(5)
            if len(top_partnerships) > 0:
                for _, partnership in top_partnerships.iterrows():
                    games_text = (
                        "game" if partnership["times_together"] == 1 else "games"
                    )
                    st.write(
                        f"👥 {partnership['player_a_name']} & {partnership['player_b_name']}: {partnership['times_together']} {games_text}"
                    )
            else:
                st.info("No partnership data available yet.")

        with col2:
            st.write("**Best Partnerships by Win Rate:**")
            # Show partnerships with at least 3 games together
            best_partnerships = partnership_stats[
                partnership_stats["times_together"] >= 3
            ].nlargest(5, "win_rate_together")
            if len(best_partnerships) > 0:
                for _, partnership in best_partnerships.iterrows():
                    games_text = (
                        "game" if partnership["times_together"] == 1 else "games"
                    )
                    st.write(
                        f"🏅 {partnership['player_a_name']} & {partnership['player_b_name']}: {partnership['win_rate_together']:.1%} ({partnership['wins_together']}/{partnership['times_together']} {games_text})"
                    )
            else:
                st.info("No partnership data available yet.")
    else:
        st.subheader("🤝 Partnership Statistics")
        st.info(
            "No partnerships recorded yet. Play some games to see partnership statistics!"
        )

    # Recent activity
    st.subheader("🏐 Recent Activity")

    if recent_games:
        for game in recent_games[:5]:  # Show last 5 games
            date_str = game["created_at"]
            if isinstance(date_str, str):
                try:
                    date_obj = datetime.fromisoformat(date_str)
                    date_str = date_obj.strftime("%Y-%m-%d %H:%M")
                except (ValueError, TypeError):
                    date_str = str(date_str)
            else:
                date_str = date_str.strftime("%Y-%m-%d %H:%M")

            # Get player names
            team_a_names: list[str] = []
            team_b_names: list[str] = []

            for player_id in game["team_a_player_ids"]:
                player = get_player_by_id(player_id)
                if player:
                    team_a_names.append(player["name"])

            for player_id in game["team_b_player_ids"]:
                player = get_player_by_id(player_id)
                if player:
                    team_b_names.append(player["name"])

            if game["team_a_wins"]:
                result_text = f"🏆 **{' & '.join(team_a_names)}** defeated {' & '.join(team_b_names)}"
            elif game["team_b_wins"]:
                result_text = f"🏆 **{' & '.join(team_b_names)}** defeated {' & '.join(team_a_names)}"
            else:
                result_text = f"🤝 **{' & '.join(team_a_names)}** tied with **{' & '.join(team_b_names)}**"

            st.info(f"{date_str}: {result_text}")
    else:
        st.info("No recent games to display.")


def show_add_data() -> None:
    """Display forms for adding new data."""
    st.header("➕ Add New Data")

    tab1, tab2, tab3 = st.tabs(["👤 Add Player", "🎯 Select Players", "� Record Game"])

    with tab1:
        create_player_form()

    with tab2:
        manage_current_players()

    with tab3:
        create_game_form()


def show_manage_players() -> None:
    """Display player management interface."""
    st.header("👥 Manage Players")

    tab1, tab2 = st.tabs(["➕ Add Player", "⚙️ Manage Existing"])

    with tab1:
        create_player_form()

    with tab2:
        manage_players_section()


def show_manage_data() -> None:
    """Display management interface for existing data."""
    st.header("⚙️ Manage Data")

    tab1, tab2, tab3 = st.tabs(
        ["👥 Manage Players", "🎯 Select Players", "⚖️ Generate Teams"]
    )

    with tab1:
        manage_players_section()

    with tab2:
        manage_current_players()

    with tab3:
        generate_teams_interface()


def show_statistics() -> None:
    """Display detailed statistics."""
    st.header("📊 Detailed Statistics")

    # Player statistics
    st.subheader("👤 Player Statistics")
    player_stats = get_player_stats()

    if not player_stats.empty:
        st.dataframe(
            player_stats,
            use_container_width=True,
            column_config={
                "win_rate": st.column_config.NumberColumn("Win Rate", format="%.1%")
            },
        )
    else:
        st.info(
            "No player statistics available yet. Add some players and record games to see statistics."
        )

    # Partnership statistics
    st.subheader("🤝 Partnership Statistics")
    partnership_stats = get_partnership_stats()

    if not partnership_stats.empty:
        st.dataframe(
            partnership_stats,
            use_container_width=True,
            column_config={
                "win_rate_together": st.column_config.NumberColumn(
                    "Win Rate Together", format="%.1%"
                )
            },
        )
    else:
        st.info(
            "No partnership statistics available yet. Record some games to see partnership data."
        )


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
    page = sidebar_data.get("page", "🏐 Quick Games")

    if page == "🏐 Quick Games":
        show_quick_games()
    elif page == "📊 Dashboard":
        show_dashboard()
    elif page == "Add Data":
        show_add_data()
    elif page == "👥 Manage Players":
        show_manage_players()
    elif page == "Manage Data":
        show_manage_data()
    elif page == "📈 Statistics":
        show_statistics()

    # Footer
    st.markdown("---")
    st.markdown("🏐 Interactive Roundnet Management")


if __name__ == "__main__":
    main()
