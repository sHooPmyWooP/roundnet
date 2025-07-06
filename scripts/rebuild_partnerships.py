"""
Script to rebuild partnerships.json from all games, ensuring only one entry per unordered pair.
Run this script once to fix partnership stats after code changes.
"""

import json
from itertools import combinations
from pathlib import Path

GAMES_FILE = Path("data/games.json")
PARTNERSHIPS_FILE = Path("data/partnerships.json")


# Load all games
def load_games():
    with open(GAMES_FILE) as f:
        return json.load(f)


# Build partnerships from all games
def rebuild_partnerships():
    games = load_games()
    partnership_dict = {}
    for game in games:
        # Team A
        team_a = game["team_a_player_ids"]
        if len(team_a) >= 2:
            for p1, p2 in combinations(sorted(team_a), 2):
                key = tuple(sorted([p1, p2]))
                if key not in partnership_dict:
                    partnership_dict[key] = {
                        "player_a_id": key[0],
                        "player_b_id": key[1],
                        "times_together": 0,
                        "wins_together": 0,
                    }
                partnership_dict[key]["times_together"] += 1
                if game["team_a_wins"]:
                    partnership_dict[key]["wins_together"] += 1
        # Team B
        team_b = game["team_b_player_ids"]
        if len(team_b) >= 2:
            for p1, p2 in combinations(sorted(team_b), 2):
                key = tuple(sorted([p1, p2]))
                if key not in partnership_dict:
                    partnership_dict[key] = {
                        "player_a_id": key[0],
                        "player_b_id": key[1],
                        "times_together": 0,
                        "wins_together": 0,
                    }
                partnership_dict[key]["times_together"] += 1
                if game["team_b_wins"]:
                    partnership_dict[key]["wins_together"] += 1
    return list(partnership_dict.values())


# Save partnerships
if __name__ == "__main__":
    partnerships = rebuild_partnerships()
    with open(PARTNERSHIPS_FILE, "w") as f:
        json.dump(partnerships, f, indent=2)
    print(f"Rebuilt {len(partnerships)} partnerships and saved to {PARTNERSHIPS_FILE}")
