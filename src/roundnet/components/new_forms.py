"""New forms for creating players, playing days, and managing teams."""

import streamlit as st
from datetime import datetime, date
from typing import List

from roundnet.data.manager import (
    add_player, add_playing_day, add_game, get_players, get_playing_days,
    assign_players_to_playing_day, generate_teams_for_playing_day,
    delete_player, delete_playing_day, delete_game, update_player_skill,
    get_games_for_playing_day, get_player_by_id, get_playing_day_by_id
)


def create_player_form():
    """Form to create a new player."""
    st.subheader("Add New Player")

    with st.form("add_player_form"):
        player_name = st.text_input("Player Name", placeholder="Enter player name...")
        skill_level = st.slider("Skill Level (1-10)", min_value=1, max_value=10, value=5, 
                               help="1 = Beginner, 10 = Expert")

        submitted = st.form_submit_button("Add Player")

        if submitted:
            if player_name.strip():
                player_id = add_player(player_name.strip(), skill_level)
                st.success(f"Player '{player_name}' added successfully with skill level {skill_level}!")
                st.rerun()
            else:
                st.error("Please enter a player name.")


def create_playing_day_form():
    """Form to create a new playing day."""
    st.subheader("Add New Playing Day")

    with st.form("add_playing_day_form"):
        play_date = st.date_input("Playing Date", value=date.today())
        location = st.text_input("Location", placeholder="e.g., Central Park, Gym A...")
        description = st.text_area("Description (optional)", 
                                 placeholder="Any additional notes about this playing session...")

        submitted = st.form_submit_button("Create Playing Day")

        if submitted:
            playing_day_id = add_playing_day(play_date, location.strip(), description.strip())
            st.success(f"Playing day created successfully for {play_date}!")
            st.rerun()


def manage_playing_day_players():
    """Interface to assign players to playing days."""
    st.subheader("Manage Playing Day Players")

    playing_days = get_playing_days()
    players = get_players()

    if not playing_days:
        st.warning("No playing days available. Create a playing day first.")
        return

    if not players:
        st.warning("No players available. Add some players first.")
        return

    # Select playing day
    playing_day_options = {
        f"{pd['date']} - {pd['location']}" if pd['location'] else pd['date']: pd['id'] 
        for pd in playing_days
    }
    
    selected_playing_day_display = st.selectbox(
        "Select Playing Day", 
        list(playing_day_options.keys())
    )
    
    if selected_playing_day_display:
        playing_day_id = playing_day_options[selected_playing_day_display]
        playing_day = get_playing_day_by_id(playing_day_id)
        
        if playing_day:
            # Show current assigned players
            assigned_player_ids = playing_day['player_ids']
            if assigned_player_ids:
                st.write("**Currently Assigned Players:**")
                assigned_players = [get_player_by_id(pid) for pid in assigned_player_ids]
                assigned_players = [p for p in assigned_players if p]
                for player in assigned_players:
                    st.write(f"- {player['name']} (Skill: {player['skill_level']})")
            else:
                st.info("No players assigned yet.")

            # Multi-select for player assignment
            player_options = {player['name']: player['id'] for player in players}
            selected_players = st.multiselect(
                "Assign Players", 
                list(player_options.keys()),
                default=[
                    player['name'] for player in players 
                    if player['id'] in assigned_player_ids
                ]
            )

            if st.button("Update Player Assignment"):
                selected_player_ids = [player_options[name] for name in selected_players]
                assign_players_to_playing_day(playing_day_id, selected_player_ids)
                st.success("Player assignment updated!")
                st.rerun()


def generate_teams_interface():
    """Interface to generate teams for playing days."""
    st.subheader("Generate Teams")

    playing_days = get_playing_days()

    if not playing_days:
        st.warning("No playing days available. Create a playing day first.")
        return

    # Select playing day
    playing_day_options = {
        f"{pd['date']} - {pd['location']}" if pd['location'] else pd['date']: pd['id'] 
        for pd in playing_days
    }
    
    selected_playing_day_display = st.selectbox(
        "Select Playing Day", 
        list(playing_day_options.keys()),
        key="team_gen_playing_day"
    )
    
    if selected_playing_day_display:
        playing_day_id = playing_day_options[selected_playing_day_display]
        playing_day = get_playing_day_by_id(playing_day_id)
        
        if playing_day:
            assigned_player_ids = playing_day['player_ids']
            
            if len(assigned_player_ids) < 2:
                st.warning("Need at least 2 players assigned to generate teams.")
                return
            
            if len(assigned_player_ids) % 2 != 0:
                st.warning("Need an even number of players to generate teams.")
                return

            # Show assigned players
            st.write(f"**Assigned Players ({len(assigned_player_ids)}):**")
            for player_id in assigned_player_ids:
                player = get_player_by_id(player_id)
                if player:
                    st.write(f"- {player['name']} (Skill: {player['skill_level']}, Win Rate: {player['win_rate']:.1%})")

            # Algorithm selection
            algorithm = st.selectbox(
                "Team Generation Algorithm",
                ["random", "skill_balanced", "win_rate_balanced", "partnership_balanced"],
                format_func=lambda x: {
                    "random": "Random Assignment",
                    "skill_balanced": "Skill Level Balanced",
                    "win_rate_balanced": "Win Rate Balanced", 
                    "partnership_balanced": "Minimize Frequent Partnerships"
                }[x]
            )

            algorithm_descriptions = {
                "random": "Teams are assigned completely randomly.",
                "skill_balanced": "Pairs high-skill players with low-skill players for balance.",
                "win_rate_balanced": "Pairs players with high win rates with those with low win rates.",
                "partnership_balanced": "Tries to pair players who haven't played together often."
            }
            
            st.info(f"**{algorithm_descriptions[algorithm]}**")

            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Generate Teams", type="primary"):
                    try:
                        teams = generate_teams_for_playing_day(playing_day_id, algorithm)
                        st.success("Teams generated successfully!")
                        st.rerun()
                    except ValueError as e:
                        st.error(f"Error generating teams: {e}")

            # Show generated teams if they exist
            if playing_day['generated_teams']:
                st.write("**Generated Teams:**")
                for i, team in enumerate(playing_day['generated_teams'], 1):
                    st.write(f"**Team {i}:**")
                    for player_id in team:
                        player = get_player_by_id(player_id)
                        if player:
                            st.write(f"  - {player['name']} (Skill: {player['skill_level']})")
                
                # Show team balance info
                with st.expander("Team Balance Analysis"):
                    from roundnet.data.file_manager import FileDataManager
                    from roundnet.data.team_generator import TeamGenerator
                    
                    dm = FileDataManager()
                    players_objs = dm.get_players()
                    partnerships = dm.get_partnerships()
                    generator = TeamGenerator(players_objs, partnerships)
                    
                    balance_metrics = generator.calculate_team_balance_score(playing_day['generated_teams'])
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Skill Variance", f"{balance_metrics['skill_variance']:.2f}")
                    with col2:
                        st.metric("Win Rate Variance", f"{balance_metrics['win_rate_variance']:.4f}")
                    with col3:
                        st.metric("Partnership Variance", f"{balance_metrics['partnership_variance']:.2f}")
                    
                    st.caption("Lower variance indicates more balanced teams")


def create_game_form():
    """Form to record game results."""
    st.subheader("Record Game Result")

    playing_days = get_playing_days()

    if not playing_days:
        st.warning("No playing days available. Create a playing day first.")
        return

    # Select playing day
    playing_day_options = {
        f"{pd['date']} - {pd['location']}" if pd['location'] else pd['date']: pd['id'] 
        for pd in playing_days
    }
    
    selected_playing_day_display = st.selectbox(
        "Select Playing Day", 
        list(playing_day_options.keys()),
        key="game_playing_day"
    )
    
    if selected_playing_day_display:
        playing_day_id = playing_day_options[selected_playing_day_display]
        playing_day = get_playing_day_by_id(playing_day_id)
        
        if playing_day and playing_day['generated_teams']:
            with st.form("add_game_form"):
                # Select teams from generated teams
                team_options = {}
                for i, team in enumerate(playing_day['generated_teams'], 1):
                    team_names = []
                    for player_id in team:
                        player = get_player_by_id(player_id)
                        if player:
                            team_names.append(player['name'])
                    team_display = f"Team {i}: {' & '.join(team_names)}"
                    team_options[team_display] = team

                if len(team_options) < 2:
                    st.warning("Need at least 2 teams to record a game.")
                    return

                col1, col2 = st.columns(2)

                with col1:
                    st.write("**Team A**")
                    team_a_display = st.selectbox("Select Team A", list(team_options.keys()), key="team_a")

                with col2:
                    st.write("**Team B**")
                    team_b_display = st.selectbox("Select Team B", list(team_options.keys()), key="team_b")

                # Game result
                result = st.radio(
                    "Game Result", 
                    ["Team A Wins", "Team B Wins", "Tie"],
                    horizontal=True
                )

                col3, col4 = st.columns(2)
                with col3:
                    duration = st.number_input("Duration (minutes)", min_value=5, max_value=120, value=30)
                with col4:
                    notes = st.text_area("Notes (optional)", placeholder="Any notes about the game...")

                submitted = st.form_submit_button("Record Game")

                if submitted:
                    if team_a_display == team_b_display:
                        st.error("Please select different teams.")
                        return

                    team_a_players = team_options[team_a_display]
                    team_b_players = team_options[team_b_display]

                    team_a_wins = result == "Team A Wins"
                    team_b_wins = result == "Team B Wins"
                    is_tie = result == "Tie"

                    game_id = add_game(
                        playing_day_id, team_a_players, team_b_players,
                        team_a_wins, team_b_wins, is_tie, duration, notes
                    )
                    
                    st.success("Game recorded successfully!")
                    st.rerun()

        elif playing_day:
            st.warning("No teams generated yet for this playing day. Generate teams first.")


def manage_players_section():
    """Section to manage existing players."""
    st.subheader("Manage Players")

    players = get_players()

    if not players:
        st.info("No players available.")
        return

    # Display players in a table format
    for player in players:
        with st.expander(f"{player['name']} (Skill: {player['skill_level']}, Win Rate: {player['win_rate']:.1%})"):
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                new_skill = st.slider(
                    "Skill Level", 
                    min_value=1, 
                    max_value=10, 
                    value=player['skill_level'],
                    key=f"skill_{player['id']}"
                )
                
                if st.button("Update Skill", key=f"update_{player['id']}"):
                    update_player_skill(player['id'], new_skill)
                    st.success("Skill level updated!")
                    st.rerun()
            
            with col2:
                st.metric("Games Played", player['total_games'])
                st.metric("Wins", player['total_wins'])
            
            with col3:
                if st.button("Delete Player", key=f"delete_{player['id']}", type="secondary"):
                    delete_player(player['id'])
                    st.success("Player deleted!")
                    st.rerun()


def manage_playing_days_section():
    """Section to manage existing playing days."""
    st.subheader("Manage Playing Days")

    playing_days = get_playing_days()

    if not playing_days:
        st.info("No playing days available.")
        return

    for playing_day in sorted(playing_days, key=lambda x: x['date'], reverse=True):
        date_str = playing_day['date'] if isinstance(playing_day['date'], str) else playing_day['date'].strftime('%Y-%m-%d')
        location_str = f" - {playing_day['location']}" if playing_day['location'] else ""
        
        with st.expander(f"{date_str}{location_str} ({len(playing_day['player_ids'])} players)"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                if playing_day['description']:
                    st.write(f"**Description:** {playing_day['description']}")
                
                if playing_day['player_ids']:
                    st.write("**Assigned Players:**")
                    for player_id in playing_day['player_ids']:
                        player = get_player_by_id(player_id)
                        if player:
                            st.write(f"- {player['name']}")
                
                if playing_day['generated_teams']:
                    st.write("**Generated Teams:**")
                    for i, team in enumerate(playing_day['generated_teams'], 1):
                        team_names = []
                        for player_id in team:
                            player = get_player_by_id(player_id)
                            if player:
                                team_names.append(player['name'])
                        st.write(f"Team {i}: {', '.join(team_names)}")
                
                # Show games for this playing day
                games = get_games_for_playing_day(playing_day['id'])
                if games:
                    st.write(f"**Games Played ({len(games)}):**")
                    for game in games:
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
                        
                        result = ""
                        if game['team_a_wins']:
                            result = f"**{' & '.join(team_a_names)}** beat {' & '.join(team_b_names)}"
                        elif game['team_b_wins']:
                            result = f"**{' & '.join(team_b_names)}** beat {' & '.join(team_a_names)}"
                        else:
                            result = f"{' & '.join(team_a_names)} tied with {' & '.join(team_b_names)}"
                        
                        st.write(f"- {result}")
            
            with col2:
                if st.button("Delete", key=f"delete_pd_{playing_day['id']}", type="secondary"):
                    delete_playing_day(playing_day['id'])
                    st.success("Playing day deleted!")
                    st.rerun()
