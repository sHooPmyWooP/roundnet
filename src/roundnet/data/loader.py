"""Data loader for creating sample data in the roundnet system."""

import random

from roundnet.data.manager import (
    add_game,
    add_player,
    generate_teams,
)


def create_sample_data() -> None:
    """Create sample players and games for demonstration."""

    # Create sample players
    players = [
        "Alice Johnson",
        "Bob Smith",
        "Charlie Brown",
        "Diana Prince",
        "Eve Adams",
        "Frank Miller",
        "Grace Lee",
        "Henry Ford",
        "Ivy Chen",
        "Jack Wilson",
        "Kelly Martin",
        "Liam Davis",
    ]

    # Add all players
    player_ids = []
    for name in players:
        player_id = add_player(name)
        player_ids.append(player_id)

    # Create sample games with different team combinations
    algorithms = ["random", "win_rate_balanced", "partnership_balanced"]

    # Generate multiple sets of games
    for _ in range(15):  # Create 15 games
        # Select random subset of players (4-8 players)
        num_players = random.choice([4, 6, 8])
        selected_players = random.sample(player_ids, num_players)

        # Generate teams
        algorithm = random.choice(algorithms)
        teams = generate_teams(selected_players, algorithm)

        if len(teams) >= 2:
            # Create games between teams
            for j in range(len(teams)):
                for k in range(j + 1, len(teams)):
                    team_a = teams[j]
                    team_b = teams[k]

                    # Random game outcome
                    outcome = random.choice(["team_a_wins", "team_b_wins", "tie"])
                    team_a_wins = outcome == "team_a_wins"
                    team_b_wins = outcome == "team_b_wins"
                    is_tie = outcome == "tie"

                    # Random duration between 15-45 minutes
                    duration = random.randint(15, 45)

                    notes = f"Sample game using {algorithm} algorithm"

                    add_game(
                        team_a,
                        team_b,
                        team_a_wins,
                        team_b_wins,
                        is_tie,
                        duration,
                        notes,
                        algorithm,
                    )
