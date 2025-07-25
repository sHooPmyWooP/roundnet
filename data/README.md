# Data Directory

This directory contains JSON data files for the roundnet application's
player-centric system.

## Structure

The data directory contains three main JSON files that form the core of the
roundnet tracking system:

- `players.json` - Player profiles with skill levels and statistics
- `games.json` - Individual game results with team compositions and outcomes
- `partnerships.json` - Statistics on player partnerships across games

## File Formats

The application uses JSON files for data persistence with the following
benefits:
- Human-readable format for easy inspection and backup
- Structured data with proper typing via dataclasses
- Atomic writes for data safety
- Easy backup (just copy the entire `data/` directory)

## Sample Data

Sample data is automatically generated by the application using the "Create
Sample Data" feature in the dashboard. This populates realistic test data
including players with varying skill levels and game history with partnerships.

## Data Schema

### Players Data (`players.json`)
- `id`: Unique player identifier (UUID)
- `name`: Player name
- `skill_level`: Player skill rating (1-10 scale)
- `total_wins`: Number of games won
- `total_games`: Total games played
- `created_at`: Player registration timestamp

### Games Data (`games.json`)
- `id`: Unique game identifier (UUID)
- `team_a_player_ids`: Player IDs for team A
- `team_b_player_ids`: Player IDs for team B
- `team_a_wins`: Boolean indicating if team A won
- `team_b_wins`: Boolean indicating if team B won
- `is_tie`: Boolean indicating if the game was a tie
- `duration_minutes`: Game duration in minutes
- `notes`: Optional game notes
- `algorithm_used`: Algorithm used for team generation
- `created_at`: Game recording timestamp

### Partnerships Data (`partnerships.json`)
- `player_a_id`: First player's ID (alphabetically ordered)
- `player_b_id`: Second player's ID
- `times_together`: Number of times these players have been teammates
- `wins_together`: Number of games won as teammates

## System Features

### Player-Centric Design
The system tracks individual players rather than static teams, reflecting how
casual roundnet is typically played with changing team compositions each
session.

### Dynamic Team Generation
Four algorithms are available for generating balanced teams:
1. **Random Assignment**: Completely random pairing
2. **Skill Balanced**: Pairs high-skill with low-skill players
3. **Win Rate Balanced**: Based on historical win rates
4. **Partnership Balanced**: Minimizes frequent partnerships

### Win/Loss Tracking
Games are recorded as wins, losses, or ties rather than specific scores,
focusing on overall performance trends rather than detailed scoring.

## Data Management

### Backup and Restore
- **Backup**: Copy the entire `data/` directory
- **Restore**: Replace the `data/` directory with your backup
- **Reset**: Delete JSON files and use "Create Sample Data" to start fresh

### File Safety
- Atomic writes prevent data corruption
- JSON format allows manual inspection and editing if needed
- Dataclass validation ensures data integrity
