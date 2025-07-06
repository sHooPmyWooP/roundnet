"""Team generation algorithms for creating balanced teams."""

import random

from roundnet.data.models import Partnership, Player


class TeamGenerator:
    """Class for generating balanced teams using different algorithms."""

    def __init__(self, players: list[Player], partnerships: list[Partnership]):
        """Initialize with players and partnership data."""
        self.players = {p.id: p for p in players}
        self.partnerships = self._build_partnership_dict(partnerships)

    def _build_partnership_dict(
        self, partnerships: list[Partnership]
    ) -> dict[tuple[str, str], Partnership]:
        """Build a dictionary for quick partnership lookup."""
        partnership_dict: dict[tuple[str, str], Partnership] = {}
        for p in partnerships:
            # Store both directions for easy lookup
            key1 = (p.player_a_id, p.player_b_id)
            key2 = (p.player_b_id, p.player_a_id)
            partnership_dict[key1] = p
            partnership_dict[key2] = p
        return partnership_dict

    def get_partnership_count(self, player_a_id: str, player_b_id: str) -> int:
        """Get how many times two players have played together."""
        key = (player_a_id, player_b_id)
        if key in self.partnerships:
            return self.partnerships[key].times_together
        return 0

    def random_teams(self, player_ids: list[str], num_teams: int) -> list[list[str]]:
        """Generate random teams, distributing players as evenly as possible."""
        if num_teams < 2:
            raise ValueError("At least 2 teams required")
        if len(player_ids) < num_teams:
            raise ValueError("Not enough players for the number of teams")
        shuffled_players = player_ids.copy()
        random.shuffle(shuffled_players)
        teams: list[list[str]] = [[] for _ in range(num_teams)]
        for idx, pid in enumerate(shuffled_players):
            teams[idx % num_teams].append(pid)
        return teams

    def partnership_balanced_teams(
        self, player_ids: list[str], num_teams: int
    ) -> list[list[str]]:
        """Generate teams trying to minimize players who have played together frequently, distributing extra players evenly."""
        if num_teams < 2:
            raise ValueError("At least 2 teams required")
        if len(player_ids) < num_teams:
            raise ValueError("Not enough players for the number of teams")
        available_players = player_ids.copy()
        teams: list[list[str]] = [[] for _ in range(num_teams)]
        # Greedily assign pairs with least partnership, then fill remaining slots
        while len(available_players) >= num_teams:
            # For each team, pick the player with the least total partnership with current team
            for t in range(num_teams):
                if not available_players:
                    break
                if not teams[t]:
                    # Start with a random player
                    player = available_players.pop(0)
                    teams[t].append(player)
                else:
                    # Find player with least partnership with current team
                    min_partnership = float("inf")
                    best_player = None
                    for pid in available_players:
                        partnership_sum = sum(
                            self.get_partnership_count(pid, teammate)
                            for teammate in teams[t]
                        )
                        if partnership_sum < min_partnership:
                            min_partnership = partnership_sum
                            best_player = pid
                    if best_player:
                        available_players.remove(best_player)
                        teams[t].append(best_player)
        # Distribute any remaining players
        for idx, pid in enumerate(available_players):
            teams[idx % num_teams].append(pid)
        return teams

    def win_rate_balanced_teams(
        self, player_ids: list[str], num_teams: int
    ) -> list[list[str]]:
        """Generate teams balanced by win rate, distributing extra players evenly."""
        if num_teams < 2:
            raise ValueError("At least 2 teams required")
        if len(player_ids) < num_teams:
            raise ValueError("Not enough players for the number of teams")
        sorted_players = sorted(
            player_ids, key=lambda pid: self.players[pid].win_rate, reverse=True
        )
        teams: list[list[str]] = [[] for _ in range(num_teams)]
        # Distribute highest win rate to lowest win rate teams
        for idx, pid in enumerate(sorted_players):
            teams[idx % num_teams].append(pid)
        return teams

    def generate_teams(
        self, player_ids: list[str], algorithm: str = "random"
    ) -> list[list[str]]:
        """Generate teams using the specified algorithm and flexible team sizes."""
        n = len(player_ids)
        if n < 4:
            raise ValueError("Need at least 4 players to generate teams")
        # Determine number of teams
        if n == 4:
            num_teams = 2
        elif 5 <= n <= 7:
            num_teams = 2
        elif n >= 8:
            num_teams = 4
        else:
            num_teams = 2
        if algorithm == "random":
            return self.random_teams(player_ids, num_teams)
        elif algorithm == "partnership_balanced":
            return self.partnership_balanced_teams(player_ids, num_teams)
        elif algorithm == "win_rate_balanced":
            return self.win_rate_balanced_teams(player_ids, num_teams)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")

    def calculate_team_balance_score(self, teams: list[list[str]]) -> dict[str, float]:
        """Calculate various balance metrics for the generated teams."""
        metrics = {
            "win_rate_variance": 0.0,
            "partnership_variance": 0.0,
            "overall_score": 0.0,
        }

        if not teams:
            return metrics

        # Calculate win rate variance between teams
        team_win_rates: list[float] = []
        for team in teams:
            team_wr = sum(self.players[pid].win_rate for pid in team) / len(team)
            team_win_rates.append(team_wr)

        if len(team_win_rates) > 1:
            wr_mean = sum(team_win_rates) / len(team_win_rates)
            metrics["win_rate_variance"] = sum(
                (wr - wr_mean) ** 2 for wr in team_win_rates
            ) / len(team_win_rates)

        # Calculate partnership familiarity variance
        team_partnership_counts: list[int] = []
        for team in teams:
            if len(team) >= 2:
                partnership_count = self.get_partnership_count(team[0], team[1])
                team_partnership_counts.append(partnership_count)

        if len(team_partnership_counts) > 1:
            partnership_mean = sum(team_partnership_counts) / len(
                team_partnership_counts
            )
            metrics["partnership_variance"] = sum(
                (count - partnership_mean) ** 2 for count in team_partnership_counts
            ) / len(team_partnership_counts)

        # Calculate overall score as a weighted average of the variances
        # Lower variance = better balance, so we invert the score
        win_rate_weight = 0.7
        partnership_weight = 0.3

        overall_score = win_rate_weight * (
            1 / (1 + metrics["win_rate_variance"])
        ) + partnership_weight * (1 / (1 + metrics["partnership_variance"]))
        metrics["overall_score"] = overall_score

        return metrics
