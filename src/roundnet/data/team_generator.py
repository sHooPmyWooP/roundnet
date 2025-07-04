"""Team generation algorithms for creating balanced teams."""

import random

from roundnet.data.models import Partnership, Player


class TeamGenerator:
    """Class for generating balanced teams using different algorithms."""

    def __init__(self, players: list[Player], partnerships: list[Partnership]):
        """Initialize with players and partnership data."""
        self.players = {p.id: p for p in players}
        self.partnerships = self._build_partnership_dict(partnerships)

    def _build_partnership_dict(self, partnerships: list[Partnership]) -> dict[tuple[str, str], Partnership]:
        """Build a dictionary for quick partnership lookup."""
        partnership_dict = {}
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

    def random_teams(self, player_ids: list[str]) -> list[list[str]]:
        """Generate random teams (2 players per team)."""
        if len(player_ids) % 2 != 0:
            raise ValueError("Number of players must be even for team generation")

        shuffled_players = player_ids.copy()
        random.shuffle(shuffled_players)

        teams = []
        for i in range(0, len(shuffled_players), 2):
            teams.append([shuffled_players[i], shuffled_players[i + 1]])

        return teams

    def skill_balanced_teams(self, player_ids: list[str]) -> list[list[str]]:
        """Generate teams balanced by skill level."""
        if len(player_ids) % 2 != 0:
            raise ValueError("Number of players must be even for team generation")

        # Sort players by skill level (descending)
        sorted_players = sorted(
            player_ids,
            key=lambda pid: self.players[pid].skill_level,
            reverse=True
        )

        teams = []
        # Pair highest with lowest, second highest with second lowest, etc.
        num_teams = len(sorted_players) // 2
        for i in range(num_teams):
            high_skill = sorted_players[i]
            low_skill = sorted_players[-(i + 1)]
            teams.append([high_skill, low_skill])

        return teams

    def partnership_balanced_teams(self, player_ids: list[str]) -> list[list[str]]:
        """Generate teams trying to minimize players who have played together frequently."""
        if len(player_ids) % 2 != 0:
            raise ValueError("Number of players must be even for team generation")

        available_players = player_ids.copy()
        teams = []

        # Try to pair players who have played together the least
        while len(available_players) >= 2:
            # Take first available player
            player_a = available_players.pop(0)

            # Find the player they've played with the least
            min_partnership_count = float('inf')
            best_partner = None

            for player_b in available_players:
                partnership_count = self.get_partnership_count(player_a, player_b)
                if partnership_count < min_partnership_count:
                    min_partnership_count = partnership_count
                    best_partner = player_b

            if best_partner:
                available_players.remove(best_partner)
                teams.append([player_a, best_partner])

        return teams

    def win_rate_balanced_teams(self, player_ids: list[str]) -> list[list[str]]:
        """Generate teams balanced by win rate."""
        if len(player_ids) % 2 != 0:
            raise ValueError("Number of players must be even for team generation")

        # Sort players by win rate (descending)
        sorted_players = sorted(
            player_ids,
            key=lambda pid: self.players[pid].win_rate,
            reverse=True
        )

        teams = []
        # Pair highest win rate with lowest win rate
        num_teams = len(sorted_players) // 2
        for i in range(num_teams):
            high_wr = sorted_players[i]
            low_wr = sorted_players[-(i + 1)]
            teams.append([high_wr, low_wr])

        return teams

    def generate_teams(self, player_ids: list[str], algorithm: str = "random") -> list[list[str]]:
        """Generate teams using the specified algorithm."""
        if len(player_ids) < 2:
            raise ValueError("Need at least 2 players to generate teams")

        if len(player_ids) % 2 != 0:
            raise ValueError("Number of players must be even for team generation")

        if algorithm == "random":
            return self.random_teams(player_ids)
        elif algorithm == "skill_balanced":
            return self.skill_balanced_teams(player_ids)
        elif algorithm == "partnership_balanced":
            return self.partnership_balanced_teams(player_ids)
        elif algorithm == "win_rate_balanced":
            return self.win_rate_balanced_teams(player_ids)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")

    def calculate_team_balance_score(self, teams: list[list[str]]) -> dict[str, float]:
        """Calculate various balance metrics for the generated teams."""
        metrics = {
            'skill_variance': 0.0,
            'win_rate_variance': 0.0,
            'partnership_variance': 0.0,
            'overall_score': 0.0
        }

        if not teams:
            return metrics

        # Calculate skill level variance between teams
        team_skills = []
        for team in teams:
            team_skill = sum(self.players[pid].skill_level for pid in team) / len(team)
            team_skills.append(team_skill)

        if len(team_skills) > 1:
            skill_mean = sum(team_skills) / len(team_skills)
            metrics['skill_variance'] = sum((skill - skill_mean) ** 2 for skill in team_skills) / len(team_skills)

        # Calculate win rate variance between teams
        team_win_rates = []
        for team in teams:
            team_wr = sum(self.players[pid].win_rate for pid in team) / len(team)
            team_win_rates.append(team_wr)

        if len(team_win_rates) > 1:
            wr_mean = sum(team_win_rates) / len(team_win_rates)
            metrics['win_rate_variance'] = sum((wr - wr_mean) ** 2 for wr in team_win_rates) / len(team_win_rates)

        # Calculate partnership familiarity variance
        team_partnership_counts = []
        for team in teams:
            if len(team) >= 2:
                partnership_count = self.get_partnership_count(team[0], team[1])
                team_partnership_counts.append(partnership_count)

        if len(team_partnership_counts) > 1:
            partnership_mean = sum(team_partnership_counts) / len(team_partnership_counts)
            metrics['partnership_variance'] = sum((count - partnership_mean) ** 2 for count in team_partnership_counts) / len(team_partnership_counts)

        # Calculate overall score as a weighted average of the variances
        # Lower variance = better balance, so we invert the score
        skill_weight = 0.4
        win_rate_weight = 0.4
        partnership_weight = 0.2

        overall_score = (
            skill_weight * (1 / (1 + metrics['skill_variance'])) +
            win_rate_weight * (1 / (1 + metrics['win_rate_variance'])) +
            partnership_weight * (1 / (1 + metrics['partnership_variance']))
        )
        metrics['overall_score'] = overall_score

        return metrics
