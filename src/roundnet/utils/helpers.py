"""Helper utility functions."""

import pandas as pd
import streamlit as st
from typing import Any, Dict, List, Optional, Union
from datetime import datetime, date
import json
import hashlib


def format_percentage(value: float, decimal_places: int = 1) -> str:
    """Format a decimal as a percentage string."""
    return f"{value * 100:.{decimal_places}f}%"


def format_duration(minutes: int) -> str:
    """Format duration in minutes to a readable string."""
    hours = minutes // 60
    mins = minutes % 60

    if hours > 0:
        return f"{hours}h {mins}m"
    return f"{mins}m"


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safely divide two numbers, returning default if denominator is zero."""
    if denominator == 0:
        return default
    return numerator / denominator


def generate_hash(data: Any) -> str:
    """Generate a hash for data caching purposes."""
    json_str = json.dumps(data, sort_keys=True, default=str)
    return hashlib.md5(json_str.encode()).hexdigest()


def validate_date_range(start_date: date, end_date: date) -> bool:
    """Validate that start_date is before or equal to end_date."""
    return start_date <= end_date


def create_download_link(df: pd.DataFrame, filename: str, link_text: str = "Download CSV") -> str:
    """Create a download link for a DataFrame."""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{link_text}</a>'
    return href


def display_dataframe_with_styling(df: pd.DataFrame, title: Optional[str] = None) -> None:
    """Display a DataFrame with nice styling."""
    if title:
        st.subheader(title)

    # Apply some basic styling
    styled_df = df.style.format({
        col: "{:.1%}" for col in df.columns if "rate" in col.lower()
    }).format({
        col: "{:.1f}" for col in df.columns if "avg" in col.lower()
    })

    st.dataframe(styled_df, use_container_width=True)


def show_metrics_grid(metrics: Dict[str, Union[int, float, str]], cols: int = 4) -> None:
    """Display metrics in a grid layout."""
    metric_items = list(metrics.items())

    # Create columns
    columns = st.columns(cols)

    for i, (label, value) in enumerate(metric_items):
        col_idx = i % cols
        with columns[col_idx]:
            # Format the value based on type
            if isinstance(value, float):
                if "rate" in label.lower() or "%" in label:
                    formatted_value = format_percentage(value)
                else:
                    formatted_value = f"{value:.2f}"
            else:
                formatted_value = str(value)

            st.metric(label.replace("_", " ").title(), formatted_value)


def filter_dataframe_by_multiselect(
    df: pd.DataFrame,
    column: str,
    selected_values: List[str],
    all_option: str = "All"
) -> pd.DataFrame:
    """Filter DataFrame based on multiselect values."""
    if all_option in selected_values or not selected_values:
        return df
    return df[df[column].isin(selected_values)]


def calculate_trend_indicator(current: float, previous: float) -> str:
    """Calculate trend indicator (up, down, or stable)."""
    if current > previous:
        return "📈"
    elif current < previous:
        return "📉"
    else:
        return "➡️"


def create_color_scale(values: List[float], colorscale: str = "RdYlGn") -> List[str]:
    """Create a color scale for a list of values."""
    import plotly.colors as pc

    # Normalize values to 0-1 range
    min_val = min(values)
    max_val = max(values)

    if max_val == min_val:
        return ["#808080"] * len(values)  # Gray for all equal values

    normalized = [(v - min_val) / (max_val - min_val) for v in values]

    # Get colors from plotly colorscale
    colors = []
    for norm_val in normalized:
        color = pc.sample_colorscale(colorscale, norm_val)[0]
        colors.append(color)

    return colors


def log_user_action(action: str, details: Optional[Dict[str, Any]] = None) -> None:
    """Log user actions for analytics (in a real app, this would go to a logging service)."""
    timestamp = datetime.now().isoformat()
    log_entry = {
        "timestamp": timestamp,
        "action": action,
        "details": details or {},
        "session_id": st.session_state.get("session_id", "unknown")
    }

    # In a real application, you would send this to a logging service
    # For now, we'll just store it in session state for debugging
    if "user_actions" not in st.session_state:
        st.session_state.user_actions = []

    st.session_state.user_actions.append(log_entry)


def export_data_as_json(data: Dict[str, Any], filename: str) -> bytes:
    """Export data as JSON bytes for download."""
    json_str = json.dumps(data, indent=2, default=str)
    return json_str.encode()


import base64  # Add this import at the top
