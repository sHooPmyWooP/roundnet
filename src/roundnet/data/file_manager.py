"""File-based data manager for persistent storage."""

import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime, date

from roundnet.data.models import Player, PlayingDay, Game, Partnership
from roundnet.data.team_generator import TeamGenerator


class FileDataManager:
    """Manager for file-based data persistence."""

    def __init__(self, data_dir: str = "data"):
        """Initialize with data directory."""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.players_file = self.data_dir / "players.json"
        self.playing_days_file = self.data_dir / "playing_days.json"
        self.games_file = self.data_dir / "games.json"
        self.partnerships_file = self.data_dir / "partnerships.json"

    def _load_json_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Load data from JSON file."""
        if not file_path.exists():
            return []
        
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def _save_json_file(self, file_path: Path, data: List[Dict[str, Any]]):
        """Save data to JSON file."""
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except IOError:
            pass  # Silent fail for now, could add logging

    # Player methods
    def get_players(self) -> List[Player]:
        """Get all players."""
        data = self._load_json_file(self.players_file)
        return [Player.from_dict(item) for item in data]

    def add_player(self, name: str, skill_level: int = 5) -> Player:
        """Add a new player."""
        player = Player(name=name, skill_level=skill_level)
        players = self.get_players()
        players.append(player)
        
        data = [p.to_dict() for p in players]
        self._save_json_file(self.players_file, data)
        return player

    def update_player(self, player: Player):
        """Update an existing player."""
        players = self.get_players()
        for i, p in enumerate(players):
            if p.id == player.id:
                players[i] = player
                break
        
        data = [p.to_dict() for p in players]
        self._save_json_file(self.players_file, data)

    def delete_player(self, player_id: str):
        """Delete a player."""
        players = self.get_players()
        players = [p for p in players if p.id != player_id]
        
        data = [p.to_dict() for p in players]
        self._save_json_file(self.players_file, data)

    def get_player_by_id(self, player_id: str) -> Optional[Player]:
        """Get player by ID."""
        players = self.get_players()
        for player in players:
            if player.id == player_id:
                return player
        return None

    # Playing day methods
    def get_playing_days(self) -> List[PlayingDay]:
        """Get all playing days."""
        data = self._load_json_file(self.playing_days_file)
        return [PlayingDay.from_dict(item) for item in data]

    def add_playing_day(self, date: date, location: str = "", description: str = "") -> PlayingDay:
        """Add a new playing day."""
        playing_day = PlayingDay(date=date, location=location, description=description)
        playing_days = self.get_playing_days()
        playing_days.append(playing_day)
        
        data = [pd.to_dict() for pd in playing_days]
        self._save_json_file(self.playing_days_file, data)
        return playing_day

    def update_playing_day(self, playing_day: PlayingDay):
        """Update an existing playing day."""
        playing_days = self.get_playing_days()
        for i, pd in enumerate(playing_days):
            if pd.id == playing_day.id:
                playing_days[i] = playing_day
                break
        
        data = [pd.to_dict() for pd in playing_days]
        self._save_json_file(self.playing_days_file, data)

    def delete_playing_day(self, playing_day_id: str):
        """Delete a playing day."""
        playing_days = self.get_playing_days()
        playing_days = [pd for pd in playing_days if pd.id != playing_day_id]
        
        data = [pd.to_dict() for pd in playing_days]
        self._save_json_file(self.playing_days_file, data)

    def get_playing_day_by_id(self, playing_day_id: str) -> Optional[PlayingDay]:
        """Get playing day by ID."""
        playing_days = self.get_playing_days()
        for playing_day in playing_days:
            if playing_day.id == playing_day_id:
                return playing_day
        return None

    def assign_players_to_playing_day(self, playing_day_id: str, player_ids: List[str]):
        """Assign players to a playing day."""
        playing_day = self.get_playing_day_by_id(playing_day_id)
        if playing_day:
            playing_day.player_ids = player_ids
            self.update_playing_day(playing_day)

    def generate_teams_for_playing_day(self, playing_day_id: str, algorithm: str = "random") -> List[List[str]]:
        """Generate teams for a playing day using the specified algorithm."""
        playing_day = self.get_playing_day_by_id(playing_day_id)
        if not playing_day or len(playing_day.player_ids) < 2:
            return []
        
        players = self.get_players()
        partnerships = self.get_partnerships()
        
        generator = TeamGenerator(players, partnerships)
        teams = generator.generate_teams(playing_day.player_ids, algorithm)
        
        # Update the playing day with generated teams
        playing_day.generated_teams = teams
        playing_day.team_generation_algorithm = algorithm
        self.update_playing_day(playing_day)
        
        return teams

    # Game methods
    def get_games(self) -> List[Game]:
        """Get all games."""
        data = self._load_json_file(self.games_file)
        return [Game.from_dict(item) for item in data]

    def add_game(self, playing_day_id: str, team_a_player_ids: List[str], 
                 team_b_player_ids: List[str], team_a_wins: bool = False,
                 team_b_wins: bool = False, is_tie: bool = False,
                 duration_minutes: int = 30, notes: str = "") -> Game:
        """Add a new game."""
        game = Game(
            playing_day_id=playing_day_id,
            team_a_player_ids=team_a_player_ids,
            team_b_player_ids=team_b_player_ids,
            team_a_wins=team_a_wins,
            team_b_wins=team_b_wins,
            is_tie=is_tie,
            duration_minutes=duration_minutes,
            notes=notes
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

    def delete_game(self, game_id: str):
        """Delete a game."""
        games = self.get_games()
        games = [g for g in games if g.id != game_id]
        
        data = [g.to_dict() for g in games]
        self._save_json_file(self.games_file, data)

    def get_games_for_playing_day(self, playing_day_id: str) -> List[Game]:
        """Get all games for a specific playing day."""
        games = self.get_games()
        return [g for g in games if g.playing_day_id == playing_day_id]

    # Partnership methods
    def get_partnerships(self) -> List[Partnership]:
        """Get all partnerships."""
        data = self._load_json_file(self.partnerships_file)
        return [Partnership.from_dict(item) for item in data]

    def get_partnership(self, player_a_id: str, player_b_id: str) -> Optional[Partnership]:
        """Get partnership between two players."""
        partnerships = self.get_partnerships()
        for p in partnerships:
            if ((p.player_a_id == player_a_id and p.player_b_id == player_b_id) or
                (p.player_a_id == player_b_id and p.player_b_id == player_a_id)):
                return p
        return None

    def _update_partnerships_from_game(self, game: Game):
        """Update partnership statistics from a game result."""
        partnerships = self.get_partnerships()
        
        # Update partnerships for team A
        if len(game.team_a_player_ids) >= 2:
            partnership = self.get_partnership(game.team_a_player_ids[0], game.team_a_player_ids[1])
            if not partnership:
                partnership = Partnership(
                    player_a_id=game.team_a_player_ids[0],
                    player_b_id=game.team_a_player_ids[1]
                )
                partnerships.append(partnership)
            
            partnership.times_together += 1
            if game.team_a_wins:
                partnership.wins_together += 1
        
        # Update partnerships for team B
        if len(game.team_b_player_ids) >= 2:
            partnership = self.get_partnership(game.team_b_player_ids[0], game.team_b_player_ids[1])
            if not partnership:
                partnership = Partnership(
                    player_a_id=game.team_b_player_ids[0],
                    player_b_id=game.team_b_player_ids[1]
                )
                partnerships.append(partnership)
            
            partnership.times_together += 1
            if game.team_b_wins:
                partnership.wins_together += 1
        
        # Save partnerships
        data = [p.to_dict() for p in partnerships]
        self._save_json_file(self.partnerships_file, data)

    def _update_player_stats_from_game(self, game: Game):
        """Update player statistics from a game result."""
        players = self.get_players()
        
        # Update stats for all players in the game
        all_player_ids = game.team_a_player_ids + game.team_b_player_ids
        
        for player_id in all_player_ids:
            player = self.get_player_by_id(player_id)
            if player:
                player.total_games += 1
                
                # Check if this player won
                if ((player_id in game.team_a_player_ids and game.team_a_wins) or
                    (player_id in game.team_b_player_ids and game.team_b_wins)):
                    player.total_wins += 1
                
                self.update_player(player)

    def get_recent_playing_days(self, days: int = 30) -> List[PlayingDay]:
        """Get recent playing days."""
        playing_days = self.get_playing_days()
        recent_date = datetime.now().date()
        
        recent_days = []
        for pd in playing_days:
            days_diff = (recent_date - pd.date).days
            if days_diff <= days:
                recent_days.append(pd)
        
        return sorted(recent_days, key=lambda x: x.date, reverse=True)
