# Roundnet System Refactoring Summary

## Overview

The roundnet application has been completely refactored from a team-based system to a player-centric system with dynamic team generation. This change better reflects how casual roundnet groups actually play.

## Key Changes

### 🏗️ Architecture Changes

| **Before**                         | **After**                               |
| ---------------------------------- | --------------------------------------- |
| Static teams with assigned players | Dynamic team generation per playing day |
| Session-based memory storage       | File-based JSON persistence             |
| Score tracking (21-15, etc.)       | Win/Loss/Tie tracking only              |
| Team-centric statistics            | Player-centric statistics               |

### 📊 Data Model Changes

#### Old System:
```
Teams (static) → Players → Games (with scores)
```

#### New System:
```
Players → Playing Days → Generated Teams → Games (W/L/T)
```

### 🎯 Core Features

#### Removed:
- ❌ Static team management
- ❌ Score tracking (21-15, etc.)
- ❌ Team-based charts and analytics
- ❌ Session-only storage

#### Added:
- ✅ Player skill levels (1-10 scale)
- ✅ Playing day organization
- ✅ 4 team generation algorithms
- ✅ Partnership tracking
- ✅ Persistent file storage
- ✅ Win/Loss/Tie game results

### 🔀 Team Generation Algorithms

1. **Random Assignment**: Completely random pairing
2. **Skill Balanced**: High-skill paired with low-skill players
3. **Win Rate Balanced**: Based on historical performance
4. **Partnership Balanced**: Minimizes frequent partnerships

### 💾 Data Persistence

- **Files**: JSON files in `data/` directory
- **Models**: Proper dataclasses with type hints
- **Storage**: Players, Playing Days, Games, Partnerships
- **Backup**: Easy to backup entire system (just copy `data/` folder)

## File Structure Changes

### New Files Added:
```
src/roundnet/data/
├── models.py           # Data models (Player, PlayingDay, Game, Partnership)
├── file_manager.py     # File-based persistence layer
├── team_generator.py   # Team generation algorithms
└── new_loader.py       # Sample data for new system

src/roundnet/components/
└── new_forms.py        # Forms for new system

demo.py                 # Demonstration script
NEW_README.md          # Updated documentation
```

### Modified Files:
```
src/roundnet/
├── main.py            # Updated to use new system
├── data/manager.py    # Wrapper for file manager + legacy compatibility
├── components/sidebar.py  # Updated navigation
└── config/settings.py     # Updated app title and description
```

## Usage Changes

### Old Workflow:
1. Create teams
2. Assign players to teams
3. Record games between teams
4. View team statistics

### New Workflow:
1. Create players (with skill levels)
2. Create playing days
3. Assign players to playing days
4. Generate teams using algorithms
5. Record game results
6. View player and partnership statistics

## Benefits of the New System

### 🎯 More Realistic
- Reflects how people actually play roundnet (teams change each session)
- No need to pre-define static teams
- Flexible player participation per session

### ⚖️ Better Balance
- Multiple algorithms for fair team generation
- Skill-based balancing
- Partnership tracking to ensure variety

### 💾 Better Data Management
- Persistent storage (survives browser refreshes)
- Easy backup and restore
- No dependency on session state

### 📊 Richer Analytics
- Individual player performance tracking
- Partnership statistics
- Playing day summaries
- Algorithm effectiveness analysis

## Migration Guide

If you have data in the old system:

1. **Export player names**: Note down all players from the old system
2. **Add skill levels**: Estimate skill levels (1-10) for each player
3. **Create playing days**: Create sessions for when you played
4. **Recreate game history**: Record major games as wins/losses/ties

The new system starts fresh but is much more powerful and realistic for ongoing use.

## Technical Implementation

### Data Models (Dataclasses):
- `Player`: Name, skill level, game statistics
- `PlayingDay`: Date, location, assigned players, generated teams
- `Game`: Playing day reference, team players, result
- `Partnership`: Player pair statistics

### Team Generation:
- Pluggable algorithm system
- Balance metrics calculation
- Variance analysis for team fairness

### File Storage:
- JSON serialization with datetime handling
- Atomic writes for data safety
- Lazy loading for performance

## Running the New System

1. **Start the app**:
   ```bash
   uv run streamlit run src/roundnet/main.py
   ```

2. **Try the demo**:
   ```bash
   python demo.py
   ```

3. **Explore features**:
   - Create sample data from the dashboard
   - Add your own players and playing days
   - Try different team generation algorithms
   - Record games and view statistics
