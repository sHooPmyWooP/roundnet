"""Main Streamlit application for roundnet analysis."""

import streamlit as st
from typing import Optional

from roundnet.components.sidebar import render_sidebar
from roundnet.components.charts import create_sample_chart
from roundnet.config.settings import APP_TITLE, APP_DESCRIPTION


def main() -> None:
    """Main function to run the Streamlit app."""
    # Page configuration
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon="🏐",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # App header
    st.title(APP_TITLE)
    st.markdown(APP_DESCRIPTION)

    # Sidebar
    sidebar_data = render_sidebar()

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("Dashboard")

        # Sample chart
        chart = create_sample_chart()
        st.plotly_chart(chart, use_container_width=True)

        # Sample metrics
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        with metric_col1:
            st.metric("Total Games", "42", "2")
        with metric_col2:
            st.metric("Win Rate", "67%", "5%")
        with metric_col3:
            st.metric("Average Score", "15.2", "-0.3")

    with col2:
        st.header("Recent Activity")

        # Sample activity feed
        activities = [
            "Game completed: Team A vs Team B",
            "New player registered: John Doe",
            "Tournament scheduled for next week",
            "Practice session reminder",
        ]

        for activity in activities:
            st.info(activity)

    # Footer
    st.markdown("---")
    st.markdown("Built with ❤️ using Streamlit")


if __name__ == "__main__":
    main()
