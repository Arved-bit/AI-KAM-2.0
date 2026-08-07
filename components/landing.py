"""Landing experience for starting a new meeting brief."""

from __future__ import annotations

from datetime import date

import streamlit as st

from components.styles import render_brand


def render_landing() -> None:
    """Render the premium, single-action landing experience."""
    render_brand()

    st.markdown('<div class="landing-greeting">Godmorgen.</div>', unsafe_allow_html=True)
    st.markdown('<div class="eyebrow landing-eyebrow">Forberedelse til kundemøde</div>', unsafe_allow_html=True)
    st.title("Vind dit næste kundemøde.")
    st.markdown(
        '<p class="muted landing-hero-copy">AI Key Account Copilot omsætter virksomhedsindsigt til konkrete salgsmuligheder, mødestrategier og anbefalede næste handlinger – så du møder kunden med et klart kommercielt udgangspunkt.</p>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="landing-question">Hvilket kundemøde vil du forberede i dag?</div>', unsafe_allow_html=True)

    selected_company = ""
    with st.container(border=True):
        st.markdown('<div class="landing-workflow-title">Opret din Executive Briefing</div>', unsafe_allow_html=True)
        st.markdown('<div class="landing-workflow-subtitle">Vælg en demokunde, eller søg efter den kunde, du skal møde.</div>', unsafe_allow_html=True)
        st.markdown('<div class="quick-start-label">Demokunder</div>', unsafe_allow_html=True)

        preset_columns = st.columns(3)
        presets = ("Bavarian Nordic", "AGC Biologics", "Lundbeck")
        for column, preset in zip(preset_columns, presets):
            with column:
                if st.button(preset, key=f"preset_{preset}", use_container_width=True, type="secondary"):
                    selected_company = preset

        st.markdown('<div class="landing-field-space"></div>', unsafe_allow_html=True)
        company = st.text_input(
            "Virksomhedsnavn",
            placeholder="Søg efter kunde eller potentiel kunde",
            value=selected_company or st.session_state.company_name,
            label_visibility="collapsed",
        )
        date_column, action_column = st.columns([1, 1.65], vertical_alignment="bottom")
        with date_column:
            meeting_date = st.date_input(
                "Mødedato (valgfrit)",
                value=None,
                min_value=date.today(),
                format="DD/MM/YYYY",
            )
        with action_column:
            prepare = st.button("Generér Executive Briefing", use_container_width=True, type="primary")

    if selected_company:
        st.session_state.company_name = selected_company
        st.session_state.meeting_date = None
        st.session_state.screen = "loading"
        st.rerun()

    if prepare:
        if not company.strip():
            st.error("Angiv en virksomhed for at generere din briefing.")
            return
        st.session_state.company_name = company.strip()
        st.session_state.meeting_date = meeting_date
        st.session_state.screen = "loading"
        st.rerun()

    st.markdown('<div class="landing-value-heading"><div class="eyebrow">Skab bedre kundedialoger</div><h2>Gå ind til mødet med en plan, der skaber fremdrift.</h2></div>', unsafe_allow_html=True)
    value_cards = st.columns(3)
    content = (
        ("01", "Forstå kundens prioriteter", "Start med de forretningsdrivere, der giver Schneider Electric en relevant og troværdig position."),
        ("02", "Identificér nye salgsmuligheder", "Find de konkrete projekter og risici, hvor en tidlig dialog kan skabe adgang til næste investering."),
        ("03", "Gå til mødet med en klar strategi", "Sæt retning for samtalen, skab enighed om næste skridt og øg sandsynligheden for at vinde forretningen."),
    )
    for column, (number, title, description) in zip(value_cards, content):
        with column:
            st.markdown(
                f'<div class="landing-value-card"><div class="landing-card-number">{number}</div><h3>{title}</h3><p class="muted">{description}</p></div>',
                unsafe_allow_html=True,
            )
