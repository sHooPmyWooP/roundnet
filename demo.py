#!/usr/bin/env python3
"""
Demo script showing the refactored roundnet system capabilities.
Run this to see the new player-centric, playing day-based system in action.
"""

from datetime import date, timedelta
import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from roundnet.data.file_manager import FileDataManager
from roundnet.data.team_generator import TeamGenerator

def main():
    """Demo the new roundnet system."""
    print("🏐 Roundnet Player Management System Demo")
    print("=" * 50)

    # Initialize data manager
    dm = FileDataManager("demo_data")

    # Create players
    print("\n1. Creating Players...")
    players = [
        ("Alice", 8), ("Bob", 6), ("Charlie", 7), ("Diana", 9),
        ("Eve", 5), ("Frank", 6), ("Grace", 7), ("Henry", 8)
    ]

    player_ids = []
    for name, skill in players:
        player = dm.add_player(name, skill)
        player_ids.append(player.id)
        print(f"   ✅ {name} (Skill: {skill})")

    # Create a playing day
    print("\n2. Creating Playing Day...")
    today = date.today()
    playing_day = dm.add_playing_day(today, "Demo Court", "System demonstration")
    print(f"   📅 {today} at Demo Court")

    # Assign players to playing day
    print("\n3. Assigning Players to Playing Day...")
    dm.assign_players_to_playing_day(playing_day.id, player_ids)
    print(f"   👥 Assigned {len(player_ids)} players")

    # Demonstrate different team generation algorithms
    algorithms = ["random", "skill_balanced", "win_rate_balanced", "partnership_balanced"]

    for algorithm in algorithms:
        print(f"\n4. Generating Teams with '{algorithm}' algorithm...")
        teams = dm.generate_teams_for_playing_day(playing_day.id, algorithm)

        print(f"   🔀 Generated {len(teams)} teams:")
        for i, team in enumerate(teams, 1):
            team_names = []
            team_skills = []
            for player_id in team:
                player = dm.get_player_by_id(player_id)
                if player:
                    team_names.append(player.name)
                    team_skills.append(player.skill_level)

            avg_skill = sum(team_skills) / len(team_skills)
            print(f"      Team {i}: {' & '.join(team_names)} (Avg Skill: {avg_skill:.1f})")

    # Simulate some games
    print("\n5. Recording Sample Games...")
    final_teams = dm.get_playing_day_by_id(playing_day.id).generated_teams

    if len(final_teams) >= 2:
        # Game 1: Team 1 vs Team 2
        game1 = dm.add_game(
            playing_day.id,
            final_teams[0],
            final_teams[1],
            team_a_wins=True,
            duration_minutes=25,
            notes="Exciting first game!"
        )

        team1_names = [dm.get_player_by_id(pid).name for pid in final_teams[0]]
        team2_names = [dm.get_player_by_id(pid).name for pid in final_teams[1]]
        print(f"   🏆 {' & '.join(team1_names)} beat {' & '.join(team2_names)}")

        if len(final_teams) >= 3:
            # Game 2: Team 2 vs Team 3
            game2 = dm.add_game(
                playing_day.id,
                final_teams[1],
                final_teams[2],
                team_b_wins=True,
                duration_minutes=30,
                notes="Close second game!"
            )

            team3_names = [dm.get_player_by_id(pid).name for pid in final_teams[2]]
            print(f"   🏆 {' & '.join(team3_names)} beat {' & '.join(team2_names)}")

    # Show updated statistics
    print("\n6. Player Statistics After Games...")
    players_list = dm.get_players()
    for player in players_list:
        if player.total_games > 0:
            print(f"   📊 {player.name}: {player.total_wins}/{player.total_games} games ({player.win_rate:.1%} win rate)")

    # Show partnerships
    print("\n7. Partnership Statistics...")
    partnerships = dm.get_partnerships()
    if partnerships:
        for partnership in partnerships:
            player_a = dm.get_player_by_id(partnership.player_a_id)
            player_b = dm.get_player_by_id(partnership.player_b_id)
            if player_a and player_b:
                print(f"   🤝 {player_a.name} & {player_b.name}: {partnership.times_together} games together ({partnership.win_rate_together:.1%} win rate)")

    print(f"\n✨ Demo complete! Data saved to 'demo_data/' directory.")
    print("   Run the Streamlit app to see the full interface:")
    print("   uv run streamlit run src/roundnet/main.py")


if __name__ == "__main__":
    main()
