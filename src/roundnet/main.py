"""Main Streamlit application for roundnet player and playing day management."""

import streamlit as st
import pandas as pd
from typing import Optional

from roundnet.components.sidebar import render_sidebar
from roundnet.components.new_forms import (
    create_player_form,
    create_playing_day_form,
    create_game_form,
    manage_players_section,
    manage_playing_days_section,
    manage_playing_day_players,
    generate_teams_interface
)
from roundnet.config.settings import APP_TITLE, APP_DESCRIPTION
from roundnet.data.manager import (
    initialize_session_state,
    get_players,
    get_playing_days,
    get_recent_games,
    get_player_stats,
    get_partnership_stats,
    get_games_for_playing_day,
    get_player_by_id
)


def show_dashboard():
    """Display the main dashboard."""
    st.header("📊 Dashboard")

    # Get current data for metrics
    players = get_players()
    playing_days = get_playing_days()
    recent_games = get_recent_games(7)

    # Welcome section for new users
    if not players and not playing_days:
        st.info("👋 **Welcome to Roundnet Player Management!** Start by adding players and creating playing days.")

        # Offer to create sample data
        st.subheader("🚀 Quick Start")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("📚 Create Sample Data", help="Add some sample players and playing days"):
                from roundnet.data.new_loader import create_sample_data
                create_sample_data()
                st.success("Sample data created! Refresh the page or navigate to see the changes.")
                st.rerun()

        with col2:
            if st.button("➕ Start Fresh", help="Begin by adding your own players and playing days"):
                st.info("💡 Use the sidebar to navigate to 'Add Data' to start adding players and playing days!")

        return

    # Top metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Players", len(players))
    with col2:
        st.metric("Playing Days", len(playing_days))
    with col3:
        total_games = sum(len(get_games_for_playing_day(pd['id'])) for pd in playing_days)
        st.metric("Total Games", total_games)
    with col4:
        st.metric("Recent Games", len(recent_games))

    # Player statistics section
    st.subheader("� Player Performance")
    player_stats = get_player_stats()
    
    if not player_stats.empty:
        # Show top performers
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Top Players by Win Rate:**")
            top_players = player_stats.head(5)
            for _, player in top_players.iterrows():
                if player['games_played'] > 0:
                    st.write(f"🏆 {player['player_name']}: {player['win_rate']:.1%} ({player['wins']}/{player['games_played']})")
        
        with col2:
            st.write("**Most Active Players:**")
            most_active = player_stats.nlargest(5, 'games_played')
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
            for _, partnership in top_partnerships.iterrows():
                st.write(f"👥 {partnership['player_a_name']} & {partnership['player_b_name']}: {partnership['times_together']} games")
        
        with col2:
            st.write("**Best Partnerships by Win Rate:**")
            best_partnerships = partnership_stats[partnership_stats['times_together'] >= 2].nlargest(5, 'win_rate_together')
            for _, partnership in best_partnerships.iterrows():
                st.write(f"🏅 {partnership['player_a_name']} & {partnership['player_b_name']}: {partnership['win_rate_together']:.1%}")

    # Recent activity
    st.subheader("🏐 Recent Activity")

    if recent_games:
        for game in recent_games[:5]:  # Show last 5 games
            date_str = game['playing_day_date']
            if hasattr(date_str, 'strftime'):
                date_str = date_str.strftime('%Y-%m-%d')
            else:
                date_str = str(date_str)

            # Get player names
            
            team_a_names = []
            team_b_names = []
            
            for player_id in game['team_a_player_ids']:
                player = get_player_by_id(player_id)
                if player:
                    team_a_names.append(player['name'])
            
            for player_id in game['team_b_player_ids']:
                player = get_player_by_id(player_id)
                if player:
                    team_b_names.append(player['name'])

            if game['team_a_wins']:
                result_text = f"🏆 **{' & '.join(team_a_names)}** defeated {' & '.join(team_b_names)}"
            elif game['team_b_wins']:
                result_text = f"🏆 **{' & '.join(team_b_names)}** defeated {' & '.join(team_a_names)}"
            else:
                result_text = f"🤝 **{' & '.join(team_a_names)}** tied with **{' & '.join(team_b_names)}**"

            location_str = f" at {game['playing_day_location']}" if game['playing_day_location'] else ""
            st.info(f"{date_str}{location_str}: {result_text}")
    else:
        st.info("No recent games to display.")


def show_add_data():
    """Display forms for adding new data."""
    st.header("➕ Add New Data")

    tab1, tab2, tab3 = st.tabs(["👤 Add Player", "� Add Playing Day", "🎯 Record Game"])

    with tab1:
        create_player_form()

    with tab2:
        create_playing_day_form()

    with tab3:
        create_game_form()


def show_manage_data():
    """Display management interface for existing data."""
    st.header("⚙️ Manage Data")

    tab1, tab2, tab3, tab4 = st.tabs([
        "👥 Manage Players", 
        "📅 Manage Playing Days", 
        "🎯 Assign Players",
        "� Generate Teams"
    ])

    with tab1:
        manage_players_section()

    with tab2:
        manage_playing_days_section()

    with tab3:
        manage_playing_day_players()
    
    with tab4:
        generate_teams_interface()


def show_statistics():
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
                "win_rate": st.column_config.NumberColumn(
                    "Win Rate",
                    format="%.1%"
                ),
                "skill_level": st.column_config.NumberColumn(
                    "Skill Level",
                    format="%d"
                )
            }
        )
    else:
        st.info("No player statistics available yet. Add some players and record games to see statistics.")

    # Partnership statistics
    st.subheader("🤝 Partnership Statistics")
    partnership_stats = get_partnership_stats()

    if not partnership_stats.empty:
        st.dataframe(
            partnership_stats,
            use_container_width=True,
            column_config={
                "win_rate_together": st.column_config.NumberColumn(
                    "Win Rate Together",
                    format="%.1%"
                )
            }
        )
    else:
        st.info("No partnership statistics available yet. Record some games to see partnership data.")

    # Playing day summary
    st.subheader("📅 Playing Day Summary")
    playing_days = get_playing_days()
    
    if playing_days:
        summary_data = []
        
        for pd in playing_days:
            games = get_games_for_playing_day(pd['id'])
            summary_data.append({
                'date': pd['date'],
                'location': pd['location'] or 'No location',
                'players': len(pd['player_ids']),
                'teams_generated': len(pd['generated_teams']),
                'games_played': len(games),
                'algorithm_used': pd['team_generation_algorithm'] if pd['generated_teams'] else 'None'
            })
        
        summary_df = pd.DataFrame(summary_data)
        summary_df = summary_df.sort_values('date', ascending=False)
        
        st.dataframe(
            summary_df,
            use_container_width=True,
            column_config={
                "date": st.column_config.DateColumn("Date"),
                "location": st.column_config.TextColumn("Location"),
                "players": st.column_config.NumberColumn("Players"),
                "teams_generated": st.column_config.NumberColumn("Teams"),
                "games_played": st.column_config.NumberColumn("Games"),
                "algorithm_used": st.column_config.TextColumn("Algorithm")
            }
        )
    else:
        st.info("No playing days available yet.")


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
