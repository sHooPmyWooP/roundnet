"""Data utilities for the interactive roundnet app."""


import pandas as pd
import streamlit as st

# Note: This file previously contained file upload and API functionality.
# The app now uses interactive forms and in-memory storage via manager.py


def create_sample_teams_and_games():
    """Create some sample data for demonstration purposes."""
    from datetime import date, timedelta

    from roundnet.data.manager import add_game, add_player, add_team

    if st.session_state.get('sample_data_created'):
        return

    # Create sample teams
    team_ids = []
    team_names = ["Spike Squad", "Net Ninjas", "Bounce Brothers", "Rally Rebels"]

    for team_name in team_names:
        team_id = add_team(team_name, f"Sample team: {team_name}")
        team_ids.append(team_id)

    # Create sample players
    player_names = [
        ["Alice", "Bob"],
        ["Charlie", "Diana"],
        ["Eve", "Frank"],
        ["Grace", "Henry"]
    ]

    for i, team_id in enumerate(team_ids):
        for player_name in player_names[i]:
            add_player(player_name, team_id)

    # Create sample games
    import random
    game_date = date.today() - timedelta(days=30)

    for _ in range(15):  # Create 15 sample games
        team_a_id = random.choice(team_ids)
        team_b_id = random.choice([t for t in team_ids if t != team_a_id])

        score_a = random.randint(12, 21)
        score_b = random.randint(12, 21)

        # Make sure there's usually a winner
        if abs(score_a - score_b) < 2:
            if random.choice([True, False]):
                score_a = max(score_a, score_b) + random.randint(1, 3)
            else:
                score_b = max(score_a, score_b) + random.randint(1, 3)

        add_game(
            team_a_id=team_a_id,
            team_b_id=team_b_id,
            score_a=score_a,
            score_b=score_b,
            game_date=game_date,
            duration_minutes=random.randint(20, 45),
            location=f"Court {random.randint(1, 3)}",
            game_type=random.choice(["Tournament", "Practice", "Casual"])
        )

        game_date += timedelta(days=random.randint(1, 3))

    st.session_state.sample_data_created = True


def validate_data(df: pd.DataFrame, required_columns: list[str]) -> bool:
    """Validate that DataFrame has required columns."""
    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        st.error(f"Missing required columns: {missing_columns}")
        return False
    return True
