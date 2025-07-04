"""Forms for creating players, teams, and games."""

import streamlit as st
from datetime import datetime, date
from typing import Optional

from roundnet.data.manager import (
    add_player, add_team, add_game, get_teams, get_players,
    update_player_team, delete_player, delete_team, delete_game
)


def create_player_form():
    """Form to create a new player."""
    st.subheader("Add New Player")

    with st.form("add_player_form"):
        player_name = st.text_input("Player Name", placeholder="Enter player name...")

        # Team selection
        teams = get_teams()
        team_options = ["No Team"] + [team['name'] for team in teams]
        selected_team = st.selectbox("Select Team", team_options)

        submitted = st.form_submit_button("Add Player")

        if submitted:
            if player_name.strip():
                team_id = None
                if selected_team != "No Team":
                    # Find team ID
                    for team in teams:
                        if team['name'] == selected_team:
                            team_id = team['id']
                            break

                player_id = add_player(player_name.strip(), team_id)
                st.success(f"Player '{player_name}' added successfully!")
                st.rerun()
            else:
                st.error("Please enter a player name.")


def create_team_form():
    """Form to create a new team."""
    st.subheader("Add New Team")

    with st.form("add_team_form"):
        team_name = st.text_input("Team Name", placeholder="Enter team name...")
        team_description = st.text_area("Description (optional)",
                                       placeholder="Enter team description...")

        submitted = st.form_submit_button("Add Team")

        if submitted:
            if team_name.strip():
                team_id = add_team(team_name.strip(), team_description.strip())
                st.success(f"Team '{team_name}' added successfully!")
                st.rerun()
            else:
                st.error("Please enter a team name.")


def create_game_form():
    """Form to create a new game."""
    st.subheader("Add New Game")

    teams = get_teams()
    if len(teams) < 2:
        st.warning("You need at least 2 teams to create a game.")
        return

    team_options = [team['name'] for team in teams]

    with st.form("add_game_form"):
        col1, col2 = st.columns(2)

        with col1:
            st.write("**Team A**")
            team_a_name = st.selectbox("Select Team A", team_options, key="team_a")
            score_a = st.number_input("Team A Score", min_value=0, max_value=50, value=15, key="score_a")

        with col2:
            st.write("**Team B**")
            team_b_name = st.selectbox("Select Team B", team_options, key="team_b")
            score_b = st.number_input("Team B Score", min_value=0, max_value=50, value=15, key="score_b")

        col3, col4 = st.columns(2)
        with col3:
            game_date = st.date_input("Game Date", value=date.today())
            game_type = st.selectbox("Game Type", ["Practice", "Tournament", "Casual", "League"])

        with col4:
            duration = st.number_input("Duration (minutes)", min_value=10, max_value=120, value=30)
            location = st.text_input("Location (optional)", placeholder="Court 1")

        submitted = st.form_submit_button("Add Game")

        if submitted:
            if team_a_name == team_b_name:
                st.error("Team A and Team B must be different teams.")
            else:
                # Find team IDs
                team_a_id = None
                team_b_id = None
                for team in teams:
                    if team['name'] == team_a_name:
                        team_a_id = team['id']
                    if team['name'] == team_b_name:
                        team_b_id = team['id']

                if team_a_id and team_b_id:
                    game_id = add_game(
                        team_a_id=team_a_id,
                        team_b_id=team_b_id,
                        score_a=score_a,
                        score_b=score_b,
                        game_date=game_date,
                        duration_minutes=duration,
                        location=location,
                        game_type=game_type
                    )

                    winner = team_a_name if score_a > score_b else team_b_name if score_b > score_a else "Draw"
                    st.success(f"Game added successfully! Winner: {winner}")
                    st.rerun()
                else:
                    st.error("Error finding team IDs.")


def manage_players_section():
    """Section for managing existing players."""
    st.subheader("Manage Players")

    players = get_players()
    teams = get_teams()

    if not players:
        st.info("No players added yet.")
        return

    for i, player in enumerate(players):
        with st.expander(f"{player['name']}", expanded=False):
            col1, col2, col3 = st.columns([2, 2, 1])

            with col1:
                st.write(f"**Name:** {player['name']}")
                current_team = "No Team"
                if player.get('team_id'):
                    for team in teams:
                        if team['id'] == player['team_id']:
                            current_team = team['name']
                            break
                st.write(f"**Current Team:** {current_team}")

            with col2:
                # Team reassignment
                team_options = ["No Team"] + [team['name'] for team in teams]
                new_team = st.selectbox(
                    "Change Team",
                    team_options,
                    index=team_options.index(current_team) if current_team in team_options else 0,
                    key=f"team_select_{i}"
                )

                if st.button("Update Team", key=f"update_{i}"):
                    new_team_id = None
                    if new_team != "No Team":
                        for team in teams:
                            if team['name'] == new_team:
                                new_team_id = team['id']
                                break

                    update_player_team(player['id'], new_team_id)
                    st.success(f"Updated {player['name']}'s team!")
                    st.rerun()

            with col3:
                if st.button("Delete", key=f"delete_player_{i}", type="secondary"):
                    delete_player(player['id'])
                    st.success(f"Deleted player {player['name']}")
                    st.rerun()


def manage_teams_section():
    """Section for managing existing teams."""
    st.subheader("Manage Teams")

    teams = get_teams()

    if not teams:
        st.info("No teams added yet.")
        return

    for i, team in enumerate(teams):
        with st.expander(f"{team['name']}", expanded=False):
            col1, col2 = st.columns([3, 1])

            with col1:
                st.write(f"**Name:** {team['name']}")
                if team.get('description'):
                    st.write(f"**Description:** {team['description']}")

                # Show team members
                players = get_players()
                team_players = [p['name'] for p in players if p.get('team_id') == team['id']]
                if team_players:
                    st.write(f"**Players:** {', '.join(team_players)}")
                else:
                    st.write("**Players:** No players assigned")

            with col2:
                if st.button("Delete Team", key=f"delete_team_{i}", type="secondary"):
                    delete_team(team['id'])
                    st.success(f"Deleted team {team['name']}")
                    st.rerun()


def manage_games_section():
    """Section for managing existing games."""
    st.subheader("Recent Games")

    from roundnet.data.manager import get_recent_games
    games = get_recent_games(30)  # Last 30 days

    if not games:
        st.info("No games recorded yet.")
        return

    for i, game in enumerate(games):
        game_date_str = game['date'].strftime('%Y-%m-%d') if hasattr(game['date'], 'strftime') else str(game['date'])
        winner_text = ""
        if game['score_a'] > game['score_b']:
            winner_text = f" (Winner: {game['team_a_name']})"
        elif game['score_b'] > game['score_a']:
            winner_text = f" (Winner: {game['team_b_name']})"
        else:
            winner_text = " (Draw)"

        with st.expander(f"{game['team_a_name']} vs {game['team_b_name']} - {game_date_str}{winner_text}", expanded=False):
            col1, col2 = st.columns([3, 1])

            with col1:
                st.write(f"**Date:** {game_date_str}")
                st.write(f"**Score:** {game['team_a_name']} {game['score_a']} - {game['score_b']} {game['team_b_name']}")
                st.write(f"**Type:** {game['game_type']}")
                st.write(f"**Duration:** {game['duration_minutes']} minutes")
                if game.get('location'):
                    st.write(f"**Location:** {game['location']}")

            with col2:
                if st.button("Delete Game", key=f"delete_game_{i}", type="secondary"):
                    delete_game(game['id'])
                    st.success("Game deleted!")
                    st.rerun()
