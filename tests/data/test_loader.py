"""Tests for data loading functionality."""

from unittest.mock import MagicMock, patch

import pandas as pd
import requests

from roundnet.data.loader import (
    fetch_api_data,
    load_player_data,
    load_sample_data,
    save_data_to_csv,
    validate_data,
)


def test_load_sample_data():
    """Test loading sample game data."""
    df = load_sample_data()

    # Check that we get a DataFrame
    assert isinstance(df, pd.DataFrame)

    # Check that it has the expected columns
    expected_columns = [
        "game_id", "date", "team_a", "team_b", "score_a", "score_b",
        "duration_minutes", "location", "game_type"
    ]
    for col in expected_columns:
        assert col in df.columns

    # Check that we have some data
    assert len(df) > 0

    # Check data types
    assert df["game_id"].dtype in ["int64", "int32"]
    assert pd.api.types.is_datetime64_any_dtype(df["date"])


def test_load_player_data():
    """Test loading sample player data."""
    df = load_player_data()

    # Check that we get a DataFrame
    assert isinstance(df, pd.DataFrame)

    # Check that it has the expected columns
    expected_columns = [
        "player_id", "name", "team", "games_played", "wins", "losses",
        "points_scored", "points_conceded"
    ]
    for col in expected_columns:
        assert col in df.columns

    # Check that we have some data
    assert len(df) > 0

    # Check that player names are strings
    assert all(isinstance(name, str) for name in df["name"])


def test_validate_data_success():
    """Test data validation with valid data."""
    df = pd.DataFrame({
        "name": ["Alice", "Bob"],
        "score": [10, 15],
        "team": ["A", "B"]
    })

    required_columns = ["name", "score"]
    assert validate_data(df, required_columns) is True


def test_validate_data_failure():
    """Test data validation with missing columns."""
    df = pd.DataFrame({
        "name": ["Alice", "Bob"],
        "score": [10, 15]
    })

    required_columns = ["name", "score", "missing_column"]

    # Mock streamlit's error function
    with patch('streamlit.error') as mock_error:
        result = validate_data(df, required_columns)
        assert result is False
        mock_error.assert_called_once()


@patch('pandas.DataFrame.to_csv')
@patch('pathlib.Path.mkdir')
def test_save_data_to_csv_success(mock_mkdir, mock_to_csv):
    """Test successful CSV saving."""
    df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})

    result = save_data_to_csv(df, "test.csv")

    assert result is True
    mock_mkdir.assert_called_once()
    mock_to_csv.assert_called_once()


@patch('pandas.DataFrame.to_csv', side_effect=Exception("File error"))
def test_save_data_to_csv_failure(mock_to_csv):
    """Test CSV saving failure."""
    df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})

    with patch('streamlit.error') as mock_error:
        result = save_data_to_csv(df, "test.csv")
        assert result is False
        mock_error.assert_called_once()


@patch('requests.get')
def test_fetch_api_data_success(mock_get):
    """Test successful API data fetching."""
    # Mock successful response
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": "test"}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = fetch_api_data("test-endpoint")

    assert result == {"data": "test"}
    mock_get.assert_called_once()


@patch('requests.get', side_effect=requests.RequestException("Network error"))
def test_fetch_api_data_failure(mock_get):
    """Test API data fetching failure."""
    with patch('streamlit.error') as mock_error:
        result = fetch_api_data("test-endpoint")
        assert result == {}
        mock_error.assert_called_once()


def test_sample_data_consistency():
    """Test that sample data is consistent across calls."""
    df1 = load_sample_data()
    df2 = load_sample_data()

    # Should have same shape and columns
    assert df1.shape == df2.shape
    assert list(df1.columns) == list(df2.columns)
