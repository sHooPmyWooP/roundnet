import pytest

from roundnet.data.models import Partnership, Player
from roundnet.data.team_generator import TeamGenerator


@pytest.fixture
def sample_players():
    return [
        Player(id="p1", name="Alice", total_wins=5, total_games=10),
        Player(id="p2", name="Bob", total_wins=6, total_games=12),
        Player(id="p3", name="Carol", total_wins=7, total_games=14),
        Player(id="p4", name="Dave", total_wins=8, total_games=16),
        Player(id="p5", name="Eve", total_wins=9, total_games=18),
        Player(id="p6", name="Frank", total_wins=10, total_games=20),
    ]


@pytest.fixture
def sample_partnerships():
    return [
        Partnership(
            player_a_id="p1", player_b_id="p2", times_together=2, wins_together=1
        ),
        Partnership(
            player_a_id="p3", player_b_id="p4", times_together=3, wins_together=2
        ),
        Partnership(
            player_a_id="p5", player_b_id="p6", times_together=1, wins_together=1
        ),
    ]


def test_build_partnership_dict(sample_players, sample_partnerships):
    tg = TeamGenerator(sample_players, sample_partnerships)
    d = tg._build_partnership_dict(sample_partnerships)
    assert ("p1", "p2") in d
    assert ("p2", "p1") in d
    assert d[("p1", "p2")].times_together == 2


def test_get_partnership_count(sample_players, sample_partnerships):
    tg = TeamGenerator(sample_players, sample_partnerships)
    assert tg.get_partnership_count("p1", "p2") == 2
    assert tg.get_partnership_count("p2", "p1") == 2
    assert tg.get_partnership_count("p1", "p3") == 0


def test_random_teams(sample_players, sample_partnerships):
    tg = TeamGenerator(sample_players, sample_partnerships)
    player_ids = [p.id for p in sample_players]
    teams = tg.random_teams(player_ids, 2)
    assert len(teams) == 2
    assert sum(len(team) for team in teams) == len(player_ids)
    # Should raise for too few teams
    with pytest.raises(ValueError):
        tg.random_teams(player_ids, 0)
    with pytest.raises(ValueError):
        tg.random_teams(["p1"], 2)


def test_partnership_balanced_teams(sample_players, sample_partnerships):
    tg = TeamGenerator(sample_players, sample_partnerships)
    player_ids = [p.id for p in sample_players]
    teams = tg.partnership_balanced_teams(player_ids, 2)
    assert len(teams) == 2
    assert sum(len(team) for team in teams) == len(player_ids)
    # Should raise for too few teams
    with pytest.raises(ValueError):
        tg.partnership_balanced_teams(player_ids, 1)
    with pytest.raises(ValueError):
        tg.partnership_balanced_teams(["p1"], 2)


def test_win_rate_balanced_teams(sample_players, sample_partnerships):
    tg = TeamGenerator(sample_players, sample_partnerships)
    player_ids = [p.id for p in sample_players]
    teams = tg.win_rate_balanced_teams(player_ids, 2)
    assert len(teams) == 2
    assert sum(len(team) for team in teams) == len(player_ids)
    # Should raise for too few teams
    with pytest.raises(ValueError):
        tg.win_rate_balanced_teams(player_ids, 1)
    with pytest.raises(ValueError):
        tg.win_rate_balanced_teams(["p1"], 2)


def test_generate_teams(sample_players, sample_partnerships):
    tg = TeamGenerator(sample_players, sample_partnerships)
    player_ids = [p.id for p in sample_players]
    # 6 players -> 2 teams
    teams = tg.generate_teams(player_ids, algorithm="random")
    assert len(teams) == 2
    teams = tg.generate_teams(player_ids, algorithm="partnership_balanced")
    assert len(teams) == 2
    teams = tg.generate_teams(player_ids, algorithm="win_rate_balanced")
    assert len(teams) == 2
    # Should raise for too few players
    with pytest.raises(ValueError):
        tg.generate_teams(["p1", "p2", "p3"], algorithm="random")
    # Should raise for unknown algorithm
    with pytest.raises(ValueError):
        tg.generate_teams(player_ids, algorithm="unknown")


def test_calculate_team_balance_score(sample_players, sample_partnerships):
    tg = TeamGenerator(sample_players, sample_partnerships)
    teams = [["p1", "p2"], ["p3", "p4"]]
    metrics = tg.calculate_team_balance_score(teams)
    assert "win_rate_variance" in metrics
    assert "partnership_variance" in metrics
    assert "overall_score" in metrics
    # Empty teams
    metrics = tg.calculate_team_balance_score([])
    assert metrics["win_rate_variance"] == 0.0
    assert metrics["partnership_variance"] == 0.0
    assert metrics["overall_score"] == 0.0
