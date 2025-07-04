"""Data models for the roundnet application."""

import uuid
from dataclasses import dataclass, field
from datetime import date as Date
from datetime import datetime
from typing import Any


@dataclass
class Player:
    """Player model."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    total_wins: int = 0
    total_games: int = 0
    created_at: datetime = field(default_factory=datetime.now)

    @property
    def win_rate(self) -> float:
        """Calculate win rate."""
        return self.total_wins / self.total_games if self.total_games > 0 else 0.0

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'total_wins': self.total_wins,
            'total_games': self.total_games,
            'win_rate': self.win_rate,
            'created_at': self.created_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Player':
        """Create from dictionary."""
        data = data.copy()
        # Remove calculated fields that aren't constructor parameters
        if 'win_rate' in data:
            del data['win_rate']
        if isinstance(data['created_at'], str):
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        return cls(**data)


@dataclass
class Game:
    """Game model for tracking individual game results."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    team_a_player_ids: list[str] = field(default_factory=list)
    team_b_player_ids: list[str] = field(default_factory=list)
    team_a_wins: bool = False
    team_b_wins: bool = False
    is_tie: bool = False
    duration_minutes: int = 30
    notes: str = ""
    algorithm_used: str = "random"  # Track which algorithm was used for team generation
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'id': self.id,
            'team_a_player_ids': self.team_a_player_ids,
            'team_b_player_ids': self.team_b_player_ids,
            'team_a_wins': self.team_a_wins,
            'team_b_wins': self.team_b_wins,
            'is_tie': self.is_tie,
            'duration_minutes': self.duration_minutes,
            'notes': self.notes,
            'algorithm_used': self.algorithm_used,
            'created_at': self.created_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Game':
        """Create from dictionary."""
        data = data.copy()
        # Handle legacy data that might have playing_day_id
        if 'playing_day_id' in data:
            del data['playing_day_id']
        if isinstance(data['created_at'], str):
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        return cls(**data)


@dataclass
class Partnership:
    """Track how often players have played together."""
    player_a_id: str
    player_b_id: str
    times_together: int = 0
    wins_together: int = 0

    @property
    def win_rate_together(self) -> float:
        """Calculate win rate when playing together."""
        return self.wins_together / self.times_together if self.times_together > 0 else 0.0

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'player_a_id': self.player_a_id,
            'player_b_id': self.player_b_id,
            'times_together': self.times_together,
            'wins_together': self.wins_together
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Partnership':
        """Create from dictionary."""
        return cls(**data)
