"""AI Key Account Copilot — Streamlit entry point."""

from __future__ import annotations

import streamlit as st

from components.briefing import render_briefing
from components.landing import render_landing
from components.loading import render_loading
from components.styles import apply_global_styles


st.set_page_config(
    page_title="AI Key Account Copilot",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def initialise_session() -> None:
    """Create the small amount of UI-only state needed by the demo."""
    st.session_state.setdefault("screen", "landing")
    st.session_state.setdefault("company_name", "")
    st.session_state.setdefault("meeting_date", None)


def main() -> None:
    initialise_session()
    apply_global_styles()

    screen = st.session_state.screen
    if screen == "loading":
        render_loading()
    elif screen == "briefing":
        render_briefing()
    else:
        render_landing()


if __name__ == "__main__":
    main()

