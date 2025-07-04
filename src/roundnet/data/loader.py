"""Data loader for creating sample data in the roundnet system."""

from datetime import date, timedelta

from roundnet.data.manager import (
    add_game,
    add_player,
    add_playing_day,
    assign_players_to_playing_day,
    generate_teams_for_playing_day,
)


def create_sample_data():
    """Create sample players, playing days, and games for demonstration."""

    # Create sample players with different skill levels
    players = [
        ("Alice Johnson", 8),
        ("Bob Smith", 6),
        ("Charlie Brown", 7),
        ("Diana Prince", 9),
        ("Eve Wilson", 5),
        ("Frank Miller", 6),
        ("Grace Lee", 7),
        ("Henry Davis", 8)
    ]

    player_ids = []
    for name, skill in players:
        player_id = add_player(name, skill)
        player_ids.append(player_id)

    # Create sample playing days
    today = date.today()

    # Playing day 1 - Last week
    pd1_date = today - timedelta(days=7)
    pd1_id = add_playing_day(pd1_date, "Stadtpark Norderstedt 🤘", "Entspannte Runde")
    assign_players_to_playing_day(pd1_id, player_ids[:6])  # 6 players
    generate_teams_for_playing_day(pd1_id, "skill_balanced")

    # Add some games for this playing day
    # Get the generated teams and simulate some games
    from roundnet.data.manager import get_playing_day_by_id
    pd1 = get_playing_day_by_id(pd1_id)
    if pd1 and pd1['generated_teams']:
        teams = pd1['generated_teams']
        if len(teams) >= 2:
            # Game 1: Team 1 vs Team 2
            add_game(pd1_id, teams[0], teams[1], team_a_wins=True, duration_minutes=25)
            # Game 2: Team 1 vs Team 3 (if exists)
            if len(teams) >= 3:
                add_game(pd1_id, teams[0], teams[2], team_b_wins=True, duration_minutes=30)

    # Playing day 2 - Few days ago
    pd2_date = today - timedelta(days=3)
    pd2_id = add_playing_day(pd2_date, "Beach Court", "Weekend beach roundnet")
    assign_players_to_playing_day(pd2_id, player_ids[2:8])  # Different 6 players
    generate_teams_for_playing_day(pd2_id, "partnership_balanced")

    # Add games for playing day 2
    pd2 = get_playing_day_by_id(pd2_id)
    if pd2 and pd2['generated_teams']:
        teams = pd2['generated_teams']
        if len(teams) >= 2:
            add_game(pd2_id, teams[0], teams[1], is_tie=True, duration_minutes=35)
            if len(teams) >= 3:
                add_game(pd2_id, teams[1], teams[2], team_a_wins=True, duration_minutes=28)

    # Playing day 3 - Today
    pd3_id = add_playing_day(today, "Gym A", "Indoor session")
    assign_players_to_playing_day(pd3_id, player_ids)  # All players
    generate_teams_for_playing_day(pd3_id, "random")


def create_sample_teams_and_games():
    """Legacy function for backward compatibility."""
    create_sample_data()
