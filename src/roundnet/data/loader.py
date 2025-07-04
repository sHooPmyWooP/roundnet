"""Data loader for creating sample data in the roundnet system."""

import random
from datetime import date, timedelta

from roundnet.data.manager import (
    add_game,
    add_player,
    generate_teams,
    get_players,
)


def create_sample_data():
    """Create sample players and games for demonstration."""

    # Create sample players with different skill levels
    players = [
        ("Alice Johnson", 8),
        ("Bob Smith", 6),
        ("Charlie Brown", 7),
        ("Diana Prince", 9),
        ("Eve Adams", 5),
        ("Frank Miller", 8),
        ("Grace Lee", 6),
        ("Henry Ford", 7),
        ("Ivy Chen", 9),
        ("Jack Wilson", 5),
        ("Kelly Martin", 7),
        ("Liam Davis", 6),
    ]

    # Add all players
    player_ids = []
    for name, skill in players:
        player_id = add_player(name, skill)
        player_ids.append(player_id)

    # Create sample games with different team combinations
    algorithms = ["random", "skill_balanced", "win_rate_balanced", "partnership_balanced"]
    
    # Generate multiple sets of games
    for i in range(15):  # Create 15 games
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
                    
                    add_game(team_a, team_b, team_a_wins, team_b_wins, is_tie, 
                            duration, notes, algorithm)
