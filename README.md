# Roundnet Player Management System

A modern Streamlit application for managing roundnet players, organizing playing days, and generating balanced teams. Built with best practices including type hints, testing, and automated code quality checks.

## Features

### 🎯 Core Functionality
- **Player Management**: Create players with skill levels (1-10 scale)
- **Playing Days**: Organize sessions where players gather to play
- **Team Generation**: Multiple algorithms to create balanced teams
- **Game Recording**: Track wins, losses, and ties (no scores needed)
- **Statistics**: Player performance and partnership tracking

### 🔀 Team Generation Algorithms

1. **Random Assignment**: Completely random team pairing
2. **Skill Balanced**: Pairs high-skill with low-skill players
3. **Win Rate Balanced**: Pairs players based on historical win rates
4. **Partnership Balanced**: Minimizes frequent partnerships

### 💾 Data Storage
- File-based JSON storage for persistence
- No database required - perfect for single-user scenarios
- Data stored in `data/` directory

### 🛠️ Development Features
- Modern Python development setup with uv
- Code quality enforcement with ruff and black
- Pre-commit hooks for automated checks
- Comprehensive testing setup
- Type checking with mypy

## Development Setup

### Prerequisites

- Python 3.13 or higher
- [uv](https://github.com/astral-sh/uv) for dependency management

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd roundnet
```

2. Install dependencies using uv:
```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv sync --extra dev
```

3. Install pre-commit hooks:
```bash
uv run pre-commit install
```

### Running the Application

Start the Streamlit app:
```bash
uv run streamlit run src/roundnet/main.py
```

The application will be available at `http://localhost:8501`.

## Usage

### Quick Start

1. **Create sample data** (optional):
   - Click "Create Sample Data" on the dashboard
   - This adds players and playing days to explore the app

2. **Add your own data**:
   - Go to "Add Data" → "Add Player" to create players
   - Set skill levels to help with team balancing
   - Create playing days for your sessions

3. **Organize a session**:
   - Go to "Manage Data" → "Assign Players"
   - Select a playing day and assign players
   - Generate teams using your preferred algorithm
   - Record game results as you play

### Team Generation

1. Assign players to a playing day
2. Choose a team generation algorithm:
   - **Random**: For casual, unpredictable matchups
   - **Skill Balanced**: When you want competitive games
   - **Win Rate Balanced**: Based on historical performance
   - **Partnership Balanced**: To mix up frequent partnerships
3. Generate teams and start playing!
4. Record game results to build statistics

### Data Management

- **Players**: Add, edit skill levels, view statistics
- **Playing Days**: Create sessions, assign players, generate teams
- **Games**: Record results, view history
- **Statistics**: Track player performance and partnerships

### Development Commands

```bash
# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src --cov-report=html

# Format code
uv run black src tests
uv run ruff check --fix src tests

# Type checking
uv run mypy src

# Run pre-commit hooks manually
uv run pre-commit run --all-files
```

## Project Structure

```
src/roundnet/
├── main.py                 # Main Streamlit application
├── components/
│   ├── forms.py             # Forms for players, playing days, games
│   ├── charts.py           # Chart components
│   └── sidebar.py          # Navigation sidebar
├── data/
│   ├── models.py           # Data models (Player, PlayingDay, Game)
│   ├── file_manager.py     # File-based data persistence
│   ├── team_generator.py   # Team generation algorithms
│   ├── manager.py          # Data management layer
│   ├── loader.py           # Data loading utilities
│   ├── processor.py        # Data processing utilities
│   └── loader.py           # Sample data creation
├── config/
│   └── settings.py         # App configuration
└── utils/
    └── helpers.py          # Helper functions
tests/
├── conftest.py
├── test_main.py
├── test_utils.py
└── data/
    ├── test_loader.py
    └── test_processor.py
```

## Data Models

### Player
- Name, skill level (1-10)
- Total games played and wins
- Calculated win rate

### Playing Day
- Date, location, description
- Assigned players
- Generated teams
- Algorithm used

### Game
- Playing day reference
- Team player IDs (2 players per team)
- Result (team A wins, team B wins, or tie)
- Duration and notes

### Partnership
- Tracks how often players play together
- Win rate when partnered
- Used for partnership balancing algorithm

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run the tests and linting (`uv run pytest && uv run ruff check`)
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Key Changes from Previous Version

This refactor removes the concept of static teams in favor of:
- **Dynamic team generation** for each playing day
- **Player-centric approach** with skill levels
- **Partnership tracking** to see who plays together
- **Algorithm-based team balancing** for fair games
- **File-based persistence** instead of session storage

The new system is more flexible and realistic for casual roundnet groups where
teams change frequently.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
