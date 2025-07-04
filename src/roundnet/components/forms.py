"""Forms for creating players and managing teams."""

from datetime import date, datetime

import streamlit as st

from roundnet.data.manager import (
    add_game,
    add_player,
    delete_player,
    generate_teams,
    get_partnerships,
    get_player_by_id,
    get_players,
    get_recent_games,
)


def create_player_form():
    """Form to create a new player."""
    st.subheader("👤 Add New Player")

    with st.form("add_player_form"):
        name = st.text_input("Player Name", placeholder="Enter player name...")

        submitted = st.form_submit_button("Add Player")

        if submitted:
            if name.strip():
                add_player(name.strip())
                st.success(f"Player '{name}' added successfully!")
                st.rerun()
            else:
                st.error("Please enter a player name.")


def manage_current_players():
    """Interface to select current active players for team generation."""
    st.subheader("🎯 Select Active Players")

    players = get_players()

    if not players:
        st.warning("No players available. Add some players first.")
        return

    # Initialize current players in session state if not exists
    if 'current_player_ids' not in st.session_state:
        st.session_state.current_player_ids = []
    if 'show_player_selector' not in st.session_state:
        st.session_state.show_player_selector = True

    # Show currently selected players
    current_players = [p for p in players if p['id'] in st.session_state.current_player_ids]
    if current_players:
        st.write("**Currently Selected Players:**")
        
        # Display current players in a more organized way
        cols = st.columns(min(len(current_players), 3))
        for i, player in enumerate(current_players):
            with cols[i % 3]:
                st.info(f"👤 {player['name']}")
        
        # Add a prominent button to change/update player selection
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🔄 Change Player Selection", type="secondary"):
                # Show the selection interface below
                st.session_state.show_player_selector = True
        with col2:
            if st.button("✅ Keep Current Players", type="primary"):
                st.success("Current player selection confirmed!")
                st.session_state.show_player_selector = False
                return
    else:
        st.info("No players selected yet.")
        st.session_state.show_player_selector = True

    # Show player selection interface when needed
    if current_players and not st.session_state.get('show_player_selector', False):
        return  # Don't show selector if players are already chosen and user hasn't clicked to change

    # Multi-select for player selection (only show when needed)
    st.write("**Select Players:**")
    player_options = {player['name']: player['id'] for player in players}
    selected_players = st.multiselect(
        "Choose active players for this session",
        list(player_options.keys()),
        default=[
            player['name'] for player in players
            if player['id'] in st.session_state.current_player_ids
        ],
        help="Select all players who will be playing in this session"
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🎯 Update Player Selection", type="primary"):
            st.session_state.current_player_ids = [player_options[name] for name in selected_players]
            st.session_state.show_player_selector = False
            # Clear generated teams when players change
            if 'generated_teams' in st.session_state:
                st.session_state.generated_teams = []
            st.success("Player selection updated!")
            st.rerun()
    
    with col2:
        if current_players and st.button("❌ Cancel Changes", type="secondary"):
            st.session_state.show_player_selector = False
            st.rerun()


def generate_teams_interface():
    """Interface to generate teams for current players."""
    st.subheader("⚖️ Generate Teams")

    # Initialize current players in session state if not exists
    if 'current_player_ids' not in st.session_state:
        st.session_state.current_player_ids = []

    if 'generated_teams' not in st.session_state:
        st.session_state.generated_teams = []

    if 'team_algorithm' not in st.session_state:
        st.session_state.team_algorithm = "random"

    current_player_ids = st.session_state.current_player_ids

    if len(current_player_ids) < 2:
        st.warning("Need at least 2 players selected to generate teams. Go to 'Select Active Players' first.")
        return

    if len(current_player_ids) % 2 != 0:
        st.warning("Need an even number of players to generate teams.")
        return

    # Show current players
    st.write(f"**Current Players ({len(current_player_ids)}):**")
    for player_id in current_player_ids:
        player = get_player_by_id(player_id)
        if player:
            st.write(f"- {player['name']}")

    # Algorithm selection
    algorithm = st.selectbox(
        "Team Generation Algorithm",
        ["random", "win_rate_balanced", "partnership_balanced"],
        format_func=lambda x: {
            "random": "Random",
            "win_rate_balanced": "Win Rate Balanced",
            "partnership_balanced": "Partnership Balanced"
        }[x],
        key="team_generation_algorithm"
    )

    if st.button("Generate Teams"):
        generated_teams = generate_teams(current_player_ids, algorithm)
        st.session_state.generated_teams = generated_teams
        st.session_state.team_algorithm = algorithm
        st.success(f"Teams generated using {algorithm} algorithm!")
        st.rerun()

    # Display generated teams
    if st.session_state.generated_teams:
        st.write("### Generated Teams")
        
        teams = st.session_state.generated_teams
        team_names = []
        
        for i, team in enumerate(teams, 1):
            team_players = []
            for player_id in team:
                player = get_player_by_id(player_id)
                if player:
                    team_players.append(player['name'])
            
            team_name = f"Team {i}"
            team_names.append(team_name)
            st.write(f"**{team_name}:** {', '.join(team_players)}")

        # Quick game recording interface
        if len(teams) >= 2:
            st.write("### Quick Game Recording")
            
            # Show all possible matchups
            for i in range(len(teams)):
                for j in range(i + 1, len(teams)):
                    col1, col2, col3, col4 = st.columns([2, 1, 2, 1])
                    
                    with col1:
                        st.write(f"**{team_names[i]}**")
                    
                    with col2:
                        if st.button(f"{team_names[i]} Wins", key=f"win_{i}_{j}"):
                            add_game(
                                teams[i], teams[j], True, False, False, 30, 
                                f"Quick record: {team_names[i]} vs {team_names[j]} - {team_names[i]} wins",
                                st.session_state.team_algorithm
                            )
                            st.success(f"{team_names[i]} victory recorded!")
                            st.rerun()
                    
                    with col3:
                        st.markdown('<div style="text-align: center;"><strong>🆚</strong></div>', unsafe_allow_html=True)
                        st.write(f"**{team_names[j]}**")
                    
                    with col4:
                        if st.button(f"{team_names[j]} Wins", key=f"win_{j}_{i}"):
                            add_game(
                                teams[i], teams[j], False, True, False, 30,
                                f"Quick record: {team_names[i]} vs {team_names[j]} - {team_names[j]} wins",
                                st.session_state.team_algorithm
                            )
                            st.success(f"{team_names[j]} victory recorded!")
                            st.rerun()
                    
                    # Tie button on new row
                    col_tie1, col_tie2, col_tie3 = st.columns([2, 1, 2])
                    with col_tie2:
                        if st.button(f"Tie Game", key=f"tie_{i}_{j}"):
                            add_game(
                                teams[i], teams[j], False, False, True, 30,
                                f"Quick record: {team_names[i]} vs {team_names[j]} - Tie",
                                st.session_state.team_algorithm
                            )
                            st.success("Tie game recorded!")
                            st.rerun()

                    st.write("")  # Add some spacing

        # Show team balance info
        with st.expander("Team Balance Analysis"):
            from roundnet.data.file_manager import FileDataManager
            from roundnet.data.team_generator import TeamGenerator

            dm = FileDataManager()
            players_objs = dm.get_players()
            partnerships = dm.get_partnerships()
            generator = TeamGenerator(players_objs, partnerships)

            balance_metrics = generator.calculate_team_balance_score(teams)

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Win Rate Variance", f"{balance_metrics['win_rate_variance']:.4f}",
                         help="Lower values indicate better experience balance")
            with col2:
                st.metric("Overall Score", f"{balance_metrics['overall_score']:.2f}",
                         help="Higher values indicate better overall balance")


def create_game_form():
    """Form to record game results manually."""
    st.subheader("🎯 Record Game Result")

    players = get_players()

    if len(players) < 4:
        st.warning("Need at least 4 players to record a game.")
        return

    with st.form("add_game_form"):
        # Team A selection
        st.write("**Team A Players:**")
        team_a_options = {player['name']: player['id'] for player in players}
        team_a_players = st.multiselect(
            "Select Team A Players",
            list(team_a_options.keys()),
            key="team_a_players"
        )

        # Team B selection
        st.write("**Team B Players:**")
        remaining_players = {name: pid for name, pid in team_a_options.items() 
                           if name not in team_a_players}
        team_b_players = st.multiselect(
            "Select Team B Players",
            list(remaining_players.keys()),
            key="team_b_players"
        )

        # Game result
        result = st.radio(
            "Game Result",
            ["Team A Wins", "Team B Wins", "Tie"],
            key="game_result"
        )

        # Additional details
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=120, value=30)
        notes = st.text_area("Notes (optional)", placeholder="Any additional notes about the game...")

        submitted = st.form_submit_button("Record Game")

        if submitted:
            if len(team_a_players) < 1 or len(team_b_players) < 1:
                st.error("Both teams must have at least one player.")
            elif set(team_a_players) & set(team_b_players):
                st.error("A player cannot be on both teams.")
            else:
                team_a_ids = [team_a_options[name] for name in team_a_players]
                team_b_ids = [remaining_players[name] for name in team_b_players]
                
                team_a_wins = result == "Team A Wins"
                team_b_wins = result == "Team B Wins"
                is_tie = result == "Tie"
                
                add_game(team_a_ids, team_b_ids, team_a_wins, team_b_wins, is_tie, 
                        duration, notes.strip(), "manual")
                st.success("Game recorded successfully!")
                st.rerun()


def manage_players_section():
    """Section to manage existing players."""
    st.subheader("👥 Manage Players")

    players = get_players()

    if not players:
        st.info("No players available.")
        return

    for player in sorted(players, key=lambda x: x['name']):
        with st.expander(f"{player['name']}"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**Games Played:** {player['total_games']}")
                st.write(f"**Wins:** {player['total_wins']}")
                st.write(f"**Win Rate:** {player['win_rate']:.1%}")

            with col2:
                if st.button("Delete", key=f"delete_{player['id']}", type="secondary"):
                    delete_player(player['id'])
                    st.success(f"Player '{player['name']}' deleted!")
                    st.rerun()


def quick_game_interface():
    """Quick interface for creating and playing games with minimal setup."""
    st.subheader("🎮 Quick Game Setup")
    
    # Check if we have current players selected
    if 'current_player_ids' not in st.session_state or not st.session_state.current_player_ids:
        st.info("🎯 First, select some active players to get started!")
        manage_current_players()
        return
    
    # Check if we have generated teams
    if 'generated_teams' not in st.session_state or not st.session_state.generated_teams:
        st.info("⚖️ Next, generate some teams!")
        generate_teams_interface()
        return
    
    # If we have everything, show the quick game interface
    st.success("✅ Ready to play! Teams are generated and ready for games.")
    
    # Show current setup
    current_players = []
    for player_id in st.session_state.current_player_ids:
        player = get_player_by_id(player_id)
        if player:
            current_players.append(player['name'])
    
    st.write(f"**Active Players:** {', '.join(current_players)}")
    st.write(f"**Algorithm Used:** {st.session_state.get('team_algorithm', 'random').title()}")
    
    # Show teams and quick recording
    generate_teams_interface()
