"""File-based data manager for persistent storage."""

import json
from datetime import datetime
from itertools import combinations
from pathlib import Path
from typing import Any

from roundnet.data.models import Game, Partnership, Player
from roundnet.data.team_generator import TeamGenerator


class FileDataManager:
    """Manager for file-based data persistence."""

    def __init__(self, data_dir: str = "data") -> None:
        """Initialize with data directory."""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

        self.players_file = self.data_dir / "players.json"
        self.games_file = self.data_dir / "games.json"
        self.partnerships_file = self.data_dir / "partnerships.json"

    def _load_json_file(self, file_path: Path) -> list[dict[str, Any]]:
        """Load data from JSON file."""
        if not file_path.exists():
            return []

        try:
            with open(file_path) as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError):
            return []

    def _save_json_file(self, file_path: Path, data: list[dict[str, Any]]) -> None:
        """Save data to JSON file."""
        try:
            with open(file_path, "w") as f:
                json.dump(data, f, indent=2, default=str)
        except OSError:
            pass  # Silent fail for now, could add logging

    # Player methods
    def get_players(self) -> list[Player]:
        """Get all players."""
        data = self._load_json_file(self.players_file)
        return [Player.from_dict(item) for item in data]

    def add_player(self, name: str) -> Player:
        """Add a new player."""
        player = Player(name=name)
        players = self.get_players()
        players.append(player)

        data = [p.to_dict() for p in players]
        self._save_json_file(self.players_file, data)
        return player

    def update_player(self, player: Player) -> None:
        """Update an existing player."""
        players = self.get_players()
        for i, p in enumerate(players):
            if p.id == player.id:
                players[i] = player
                break

        data = [p.to_dict() for p in players]
        self._save_json_file(self.players_file, data)

    def delete_player(self, player_id: str) -> None:
        """Delete a player."""
        players = self.get_players()
        players = [p for p in players if p.id != player_id]

        data = [p.to_dict() for p in players]
        self._save_json_file(self.players_file, data)

    def get_player_by_id(self, player_id: str) -> Player | None:
        """Get player by ID."""
        players = self.get_players()
        for player in players:
            if player.id == player_id:
                return player
        return None

    # Team generation methods
    def generate_teams(
        self, player_ids: list[str], algorithm: str = "random"
    ) -> list[list[str]]:
        """Generate teams for the given players using the specified algorithm."""
        if len(player_ids) < 2:
            return []

        players = self.get_players()
        partnerships = self.get_partnerships()

        generator = TeamGenerator(players, partnerships)
        teams = generator.generate_teams(player_ids, algorithm)
        return teams

    # Game methods
    def get_games(self) -> list[Game]:
        """Get all games."""
        data = self._load_json_file(self.games_file)
        return [Game.from_dict(item) for item in data]

    def add_game(
        self,
        team_a_player_ids: list[str],
        team_b_player_ids: list[str],
        team_a_wins: bool = False,
        team_b_wins: bool = False,
        is_tie: bool = False,
        duration_minutes: int = 30,
        notes: str = "",
        algorithm_used: str = "random",
    ) -> Game:
        """Add a new game."""
        game = Game(
            team_a_player_ids=team_a_player_ids,
            team_b_player_ids=team_b_player_ids,
            team_a_wins=team_a_wins,
            team_b_wins=team_b_wins,
            is_tie=is_tie,
            duration_minutes=duration_minutes,
            notes=notes,
            algorithm_used=algorithm_used,
        )

        games = self.get_games()
        games.append(game)

        data = [g.to_dict() for g in games]
        self._save_json_file(self.games_file, data)

        # Update player statistics
        self._update_player_stats_from_game(game)

        # Update partnerships
        self._update_partnerships_from_game(game)

        return game

    def delete_game(self, game_id: str) -> None:
        """Delete a game."""
        games = self.get_games()
        games = [g for g in games if g.id != game_id]

        data = [g.to_dict() for g in games]
        self._save_json_file(self.games_file, data)

    # Partnership methods
    def get_partnerships(self) -> list[Partnership]:
        """Get all partnerships."""
        data = self._load_json_file(self.partnerships_file)
        return [Partnership.from_dict(item) for item in data]

    def get_partnership(self, player_a_id: str, player_b_id: str) -> Partnership | None:
        """Get partnership between two players."""
        partnerships = self.get_partnerships()
        for p in partnerships:
            if (p.player_a_id == player_a_id and p.player_b_id == player_b_id) or (
                p.player_a_id == player_b_id and p.player_b_id == player_a_id
            ):
                return p
        return None

    def _update_partnerships_from_game(self, game: Game) -> None:
        """Update partnership statistics from a game result, always using unordered pairs."""

        partnerships = self.get_partnerships()
        # Build a dict for fast lookup by unordered pair
        partnership_dict = {}
        for p in partnerships:
            key = tuple(sorted([p.player_a_id, p.player_b_id]))
            partnership_dict[key] = p

        # Update partnerships for team A (all unique pairs)
        if len(game.team_a_player_ids) >= 2:
            for p1, p2 in combinations(sorted(game.team_a_player_ids), 2):
                key = tuple(sorted([p1, p2]))
                partnership = partnership_dict.get(key)
                if not partnership:
                    partnership = Partnership(player_a_id=key[0], player_b_id=key[1])
                    partnership_dict[key] = partnership
                partnership.times_together += 1
                if game.team_a_wins:
                    partnership.wins_together += 1

        # Update partnerships for team B (all unique pairs)
        if len(game.team_b_player_ids) >= 2:
            for p1, p2 in combinations(sorted(game.team_b_player_ids), 2):
                key = tuple(sorted([p1, p2]))
                partnership = partnership_dict.get(key)
                if not partnership:
                    partnership = Partnership(player_a_id=key[0], player_b_id=key[1])
                    partnership_dict[key] = partnership
                partnership.times_together += 1
                if game.team_b_wins:
                    partnership.wins_together += 1

        # Save only one entry per unordered pair
        data = [p.to_dict() for p in partnership_dict.values()]
        self._save_json_file(self.partnerships_file, data)

    def _update_player_stats_from_game(self, game: Game) -> None:
        """Update player statistics from a game result."""
        self.get_players()

        # Update stats for all players in the game
        all_player_ids = game.team_a_player_ids + game.team_b_player_ids

        for player_id in all_player_ids:
            player = self.get_player_by_id(player_id)
            if player:
                player.total_games += 1

                # Check if this player won
                if (player_id in game.team_a_player_ids and game.team_a_wins) or (
                    player_id in game.team_b_player_ids and game.team_b_wins
                ):
                    player.total_wins += 1

                self.update_player(player)

    def get_recent_games(self, days: int = 30) -> list[Game]:
        """Get recent games."""
        games = self.get_games()
        recent_date = datetime.now().date()

        recent_games = []
        for game in games:
            game_date = game.created_at.date()
            days_diff = (recent_date - game_date).days
            if days_diff <= days:
                recent_games.append(game)

        return sorted(recent_games, key=lambda x: x.created_at, reverse=True)
