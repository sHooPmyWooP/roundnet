"""Tests for utility helper functions."""

import pytest
import pandas as pd
from datetime import date
from unittest.mock import patch

from roundnet.utils.helpers import (
    format_percentage,
    format_duration,
    safe_divide,
    validate_date_range,
    calculate_trend_indicator,
    filter_dataframe_by_multiselect
)


def test_format_percentage():
    """Test percentage formatting."""
    assert format_percentage(0.75) == "75.0%"
    assert format_percentage(0.755, 2) == "75.50%"
    assert format_percentage(1.0) == "100.0%"
    assert format_percentage(0.0) == "0.0%"


def test_format_duration():
    """Test duration formatting."""
    assert format_duration(30) == "30m"
    assert format_duration(60) == "1h 0m"
    assert format_duration(90) == "1h 30m"
    assert format_duration(125) == "2h 5m"


def test_safe_divide():
    """Test safe division function."""
    assert safe_divide(10, 2) == 5.0
    assert safe_divide(10, 0) == 0.0
    assert safe_divide(10, 0, default=1.0) == 1.0
    assert safe_divide(7, 3) == pytest.approx(2.333, rel=1e-3)


def test_validate_date_range():
    """Test date range validation."""
    start = date(2024, 1, 1)
    end = date(2024, 12, 31)

    assert validate_date_range(start, end) is True
    assert validate_date_range(end, start) is False
    assert validate_date_range(start, start) is True


def test_calculate_trend_indicator():
    """Test trend indicator calculation."""
    assert calculate_trend_indicator(10, 5) == "📈"  # Up
    assert calculate_trend_indicator(5, 10) == "📉"  # Down
    assert calculate_trend_indicator(5, 5) == "➡️"   # Stable


def test_filter_dataframe_by_multiselect():
    """Test DataFrame filtering by multiselect values."""
    df = pd.DataFrame({
        "team": ["A", "B", "C", "A", "B"],
        "score": [10, 15, 20, 12, 18]
    })

    # Test filtering with specific teams
    filtered = filter_dataframe_by_multiselect(df, "team", ["A", "B"])
    assert len(filtered) == 4
    assert all(team in ["A", "B"] for team in filtered["team"])

    # Test with "All" option
    filtered_all = filter_dataframe_by_multiselect(df, "team", ["All", "A"])
    assert len(filtered_all) == len(df)

    # Test with empty selection
    filtered_empty = filter_dataframe_by_multiselect(df, "team", [])
    assert len(filtered_empty) == len(df)


def test_create_color_scale():
    """Test color scale creation."""
    from roundnet.utils.helpers import create_color_scale

    values = [1, 2, 3, 4, 5]
    colors = create_color_scale(values)

    assert len(colors) == len(values)
    assert all(isinstance(color, str) for color in colors)
    assert all(color.startswith("#") for color in colors)


def test_create_color_scale_equal_values():
    """Test color scale with equal values."""
    from roundnet.utils.helpers import create_color_scale

    values = [5, 5, 5, 5]
    colors = create_color_scale(values)

    assert len(colors) == len(values)
    assert all(color == "#808080" for color in colors)  # All gray


@patch('streamlit.session_state', {})
def test_log_user_action():
    """Test user action logging."""
    from roundnet.utils.helpers import log_user_action
    import streamlit as st

    log_user_action("test_action", {"detail": "test"})

    assert "user_actions" in st.session_state
    assert len(st.session_state.user_actions) == 1

    action = st.session_state.user_actions[0]
    assert action["action"] == "test_action"
    assert action["details"]["detail"] == "test"
    assert "timestamp" in action


def test_export_data_as_json():
    """Test JSON data export."""
    from roundnet.utils.helpers import export_data_as_json

    data = {"key": "value", "number": 42}
    json_bytes = export_data_as_json(data, "test.json")

    assert isinstance(json_bytes, bytes)

    # Decode and check content
    json_str = json_bytes.decode()
    assert "key" in json_str
    assert "value" in json_str
    assert "42" in json_str
