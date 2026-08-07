"""Præsentation af den briefing, som Commercial Intelligence Engine genererer."""

from __future__ import annotations

from datetime import date, datetime
from html import escape

import streamlit as st

from components.styles import render_brand
from services.briefing_engine import BriefingDocument, BriefingSection, Opportunity, generate_briefing


def _section_heading(number: str, title: str, subtitle: str = "") -> None:
    st.markdown(f'<div class="section-kicker">{number} · {title}</div><h2>{title}</h2>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<p class="muted">{subtitle}</p>', unsafe_allow_html=True)


def _render_opportunity(item: Opportunity) -> None:
    priority_class = {"Høj": "priority-high", "Mellem": "priority-medium", "Lav": "priority-low"}[item.priority]
    st.markdown(
        f'''<div class="opportunity {'high-opportunity' if item.priority == 'Høj' else ''}">
          <div class="opportunity-heading"><span class="opportunity-icon">◌</span>{item.title}</div>
          <div class="opportunity-grid">
            <div class="opportunity-field"><span class="small-label">Kommerciel trigger</span>{item.trigger}</div>
            <div class="opportunity-field"><span class="small-label">Hvorfor Schneider skal handle nu</span>{item.why_now}</div>
            <div class="opportunity-field"><span class="small-label">Anbefalet Schneider Electric-portefølje</span>{item.portfolio}</div>
            <div class="opportunity-field"><span class="small-label">Forventet kundeudbytte</span>{item.customer_outcome}</div>
            <div class="opportunity-field"><span class="small-label">Kommerciel prioritet og vurderingssikkerhed</span><span class="tag {priority_class}">{item.priority}</span> <span class="tag">{item.confidence}% sikkerhed</span></div>
          </div></div>''',
        unsafe_allow_html=True,
    )


def _render_kpis(document: BriefingDocument) -> None:
    for column, (icon, label, value, detail) in zip(st.columns(4), document.kpis):
        with column:
            st.markdown(f'<div class="hero-kpi"><span class="hero-kpi-icon">{icon}</span><div class="hero-kpi-label">{label}</div><div class="hero-kpi-value">{value}</div><div class="hero-kpi-detail">{detail}</div></div>', unsafe_allow_html=True)


def _render_executive_assessment(section: BriefingSection) -> None:
    st.markdown('<div class="assessment-panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="eyebrow">{section.title}</div><div class="assessment-title">{section.summary}</div>', unsafe_allow_html=True)
    st.markdown('<div class="assessment-grid">', unsafe_allow_html=True)
    for point in section.key_points:
        label, value = point.split(": ", maxsplit=1)
        st.markdown(f'<div class="assessment-item"><div class="small-label">{label}</div><div class="assessment-value">{value}</div><div class="assessment-detail">{section.commercial_conclusion}</div></div>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)


def _render_strategy(section: BriefingSection) -> None:
    st.markdown('<div class="strategy-centrepiece">', unsafe_allow_html=True)
    st.markdown(f'<div class="eyebrow">Kommerciel anbefaling</div><div class="strategy-title">{section.title}</div>', unsafe_allow_html=True)
    st.markdown('<div class="strategy-grid">', unsafe_allow_html=True)
    for index, point in enumerate(section.key_points, start=1):
        st.markdown(f'<div class="strategy-row"><div class="strategy-icon">{index}</div><div>{point}</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="strategy-row"><div class="strategy-icon">✓</div><div><b>Kommerciel konklusion</b><br><span class="muted">{section.commercial_conclusion}</span></div></div>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)


def render_briefing() -> None:
    """Render den data-drevne executive briefing uden direkte dataadgang fra UI-laget."""
    document = generate_briefing(st.session_state.company_name)
    render_brand()
    if st.button("← Forbered nyt møde", type="secondary"):
        st.session_state.screen = "landing"
        st.rerun()

    meeting_date = st.session_state.meeting_date
    month_names = ("jan.", "feb.", "mar.", "apr.", "maj", "jun.", "jul.", "aug.", "sep.", "okt.", "nov.", "dec.")
    date_label = f"{meeting_date.day}. {month_names[meeting_date.month - 1]} {meeting_date.year}" if isinstance(meeting_date, date) else "Mødedato er ikke angivet"
    now = datetime.now()
    st.markdown('<div class="briefing-top">', unsafe_allow_html=True)
    st.markdown('<div class="eyebrow">Ledelsesbriefing · Udarbejdet af AI Key Account Copilot</div>', unsafe_allow_html=True)
    st.title(document.company_name)
    st.markdown(f'<p class="muted">Kundemøde · {date_label}<br>Genereret {now.day}. {month_names[now.month - 1]} {now.year} · {now:%H:%M}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-kicker">Kommercielt perspektiv</div>', unsafe_allow_html=True)
    st.markdown(f'<h2>{document.assessment.summary}</h2>', unsafe_allow_html=True)
    st.markdown(f'<p class="muted">{escape(document.assessment.commercial_conclusion)}</p>', unsafe_allow_html=True)
    _render_kpis(document)

    st.markdown('<div style="height:3.3rem"></div>', unsafe_allow_html=True)
    _render_executive_assessment(document.assessment)

    st.markdown('<div style="height:3.3rem"></div>', unsafe_allow_html=True)
    _section_heading("01", "Ledelsesresumé")
    st.info(f"**Kommerciel anbefaling:** {document.customer_strategy.commercial_conclusion}")

    _section_heading("02", document.customer_strategy.title)
    for column, point in zip(st.columns(3), document.customer_strategy.key_points):
        with column:
            st.markdown(f'<div class="card"><div class="metric-label">Strategisk prioritet</div><div class="metric-value">{point}</div></div>', unsafe_allow_html=True)

    st.markdown('<div style="height:2.8rem"></div>', unsafe_allow_html=True)
    _section_heading("03", document.commercial_signals.title, document.commercial_signals.summary)
    for column, point in zip(st.columns(3), document.commercial_signals.key_points):
        with column:
            st.markdown(f'<div class="card"><span class="tag">Signal</span><p class="muted">{point}</p></div>', unsafe_allow_html=True)

    st.markdown('<div style="height:2.8rem"></div>', unsafe_allow_html=True)
    _section_heading("04", "Hvor kan Schneider Electric skabe værdi?", document.schneider_positioning.commercial_conclusion)
    for opportunity in document.opportunities:
        _render_opportunity(opportunity)

    st.markdown('<div style="height:2.8rem"></div>', unsafe_allow_html=True)
    _section_heading("05", document.stakeholder_strategy.title, document.stakeholder_strategy.summary)
    for stakeholder in document.stakeholders:
        st.markdown(f'''<div class="stakeholder-card"><div class="stakeholder-heading"><span class="strategy-icon">◉</span>{stakeholder.role}</div><div class="stakeholder-grid"><div><span class="small-label">Forretningsprioritet</span>{stakeholder.priority}</div><div><span class="small-label">Salgsmål</span>{stakeholder.sales_objective}</div><div><span class="small-label">Foreslået samtale</span>{stakeholder.conversation}</div><div><span class="small-label">Potentiel Schneider-værdi</span>{stakeholder.schneider_value}</div></div></div>''', unsafe_allow_html=True)

    st.markdown('<div style="height:2.8rem"></div>', unsafe_allow_html=True)
    _section_heading("06", document.questions.title, document.questions.summary)
    for index, question in enumerate(document.questions.key_points, start=1):
        st.markdown(f'<div class="strategy-row"><div class="strategy-icon">{index}</div><div>{question}</div></div>', unsafe_allow_html=True)

    st.markdown('<div style="height:3.2rem"></div>', unsafe_allow_html=True)
    _render_strategy(document.meeting_strategy)

    st.markdown('<div style="height:3.2rem"></div>', unsafe_allow_html=True)
    action_points = "".join(
        f'<div class="cta-metric"><div class="cta-metric-label">Næste skridt</div><div class="cta-metric-value">{point}</div></div>'
        for point in document.action_plan.key_points
    )
    st.markdown(
        f'''<div class="cta-card"><div class="eyebrow" style="color:#9ce6aa">{document.action_plan.title}</div><h2>{document.action_plan.summary}</h2><p class="muted">{document.action_plan.commercial_conclusion}</p><div class="strategy-grid" style="margin-top:1.4rem">{action_points}</div></div>''',
        unsafe_allow_html=True,
    )
