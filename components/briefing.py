"""Executive briefing presentation assembled from reusable content sections."""

from __future__ import annotations

from datetime import date, datetime
from html import escape

import streamlit as st

from components.styles import render_brand
from services.briefing_data import Opportunity, get_briefing


def _section_heading(number: str, title: str, subtitle: str = "") -> None:
    """Render a consistent executive section heading."""
    st.markdown(f'<div class="section-kicker">{number} · {title}</div><h2>{title}</h2>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<p class="muted">{subtitle}</p>', unsafe_allow_html=True)


def _render_opportunity(item: Opportunity) -> None:
    """Render one opportunity as a decision-ready commercial card."""
    priority_class = {
        "Høj": "priority-high",
        "Mellem": "priority-medium",
        "Lav": "priority-low",
    }[item.priority]
    st.markdown(
        f'''<div class="opportunity {'high-opportunity' if item.priority == 'Høj' else ''}">
          <div class="opportunity-heading"><span class="opportunity-icon">◌</span>{item.title}</div>
          <div class="opportunity-grid">
            <div class="opportunity-field"><span class="small-label">Kommerciel trigger</span>{item.trigger}</div>
            <div class="opportunity-field"><span class="small-label">Hvorfor Schneider skal handle nu</span>{item.why_now}</div>
            <div class="opportunity-field"><span class="small-label">Anbefalet Schneider Electric-portefølje</span>{item.portfolio}</div>
            <div class="opportunity-field"><span class="small-label">Forventet kundeudbytte</span>{item.customer_outcome}</div>
            <div class="opportunity-field"><span class="small-label">Kommerciel prioritet og vurderingssikkerhed</span><span class="tag {priority_class}">{item.priority}</span> <span class="tag">{item.confidence}% sikkerhed</span></div>
          </div>
        </div>''',
        unsafe_allow_html=True,
    )


def _render_kpis() -> None:
    """Render the concise Copilot-style readiness metrics."""
    kpis = (
        ("✓", "Mødeparathed", "94%", "Klar til en fokuseret kommerciel dialog"),
        ("✦", "Vurderingssikkerhed", "91%", "Stærkt grundlag af kunde- og markedssignaler"),
        ("◌", "Salgsmuligheder", "3", "Prioriterede muligheder at undersøge"),
        ("◷", "Læsetid", "4 min.", "Kort briefing til mødelokalet"),
    )
    for column, (icon, label, value, detail) in zip(st.columns(4), kpis):
        with column:
            st.markdown(
                f'<div class="hero-kpi"><span class="hero-kpi-icon">{icon}</span><div class="hero-kpi-label">{label}</div><div class="hero-kpi-value">{value}</div><div class="hero-kpi-detail">{detail}</div></div>',
                unsafe_allow_html=True,
            )


def _render_strategy() -> None:
    """Render the visual centerpiece: practical AI meeting coaching."""
    strategy = (
        ("Åbningsstrategi", "Indled med kundens vækstplan og spørg, hvor kommende investeringer kan få størst effekt på stabil drift, energi og leveringssikkerhed."),
        ("Relationsopbygning", "Giv driftsansvarlige, bæredygtighed og teknik et fælles sprog: forretningsrisiko, beslutningshastighed og målbar værdi."),
        ("Kommerciel positionering", "Positionér Schneider Electric som den partner, der samler bygning, strøm og energi i en plan, der kan skaleres på tværs af faciliteter."),
        ("Executive budskab", "En tidlig, fælles standard reducerer projektrisiko og gør det lettere at dokumentere værdien af hver investering."),
        ("Håndtering af indvendinger", "Hvis kunden ønsker at starte småt, foreslå en afgrænset facilitet med klare målepunkter frem for en bred teknologidiskussion."),
        ("Anbefalet opfølgning", "Aftal en teknisk afdækningsworkshop med de centrale beslutningstagere og et konkret input til den næste investeringsbeslutning."),
    )
    st.markdown('<div class="strategy-centrepiece">', unsafe_allow_html=True)
    st.markdown('<div class="eyebrow">Kommerciel anbefaling</div><div class="strategy-title">Anbefalet mødestrategi</div>', unsafe_allow_html=True)
    st.markdown('<div class="strategy-grid">', unsafe_allow_html=True)
    for title, detail in strategy:
        st.markdown(f'<div class="strategy-row"><div class="strategy-icon">✓</div><div><b>{title}</b><br><span class="muted">{detail}</span></div></div>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)


def _render_executive_assessment() -> None:
    """Render den kommercielle vurdering, som sætter retningen for kundeplanen."""
    assessment = (
        ("Kommercielt potentiale", "Højt", "Tre relevante spor med tydelig forretningsværdi"),
        ("Strategisk match", "Meget stærkt", "Schneider Electric kan samle energi, bygning og strøm"),
        ("Investeringshorisont", "6–18 måneder", "Bedst mulighed før projektrammerne låses"),
        ("Primære forretningsdrivere", "Kapacitet · energi · robusthed", "Drivere med direkte effekt på driftsresultater"),
        ("Anbefalet kommerciel tilgang", "Strategisk afdækning", "Skab mandat til en fælles workshop på én facilitet"),
    )
    st.markdown('<div class="assessment-panel">', unsafe_allow_html=True)
    st.markdown('<div class="eyebrow">Kommerciel vurdering</div><div class="assessment-title">En kunde, der er værd at forfølge — hvis Schneider Electric kommer ind tidligt.</div>', unsafe_allow_html=True)
    st.markdown('<div class="assessment-grid">', unsafe_allow_html=True)
    for label, value, detail in assessment:
        st.markdown(f'<div class="assessment-item"><div class="small-label">{label}</div><div class="assessment-value">{value}</div><div class="assessment-detail">{detail}</div></div>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)


def render_briefing() -> None:
    """Render a skimmable, executive-first briefing using placeholder information."""
    briefing = get_briefing(st.session_state.company_name)
    render_brand()
    if st.button("← Forbered nyt møde", type="secondary"):
        st.session_state.screen = "landing"
        st.rerun()

    meeting_date = st.session_state.meeting_date
    month_names = ("jan.", "feb.", "mar.", "apr.", "maj", "jun.", "jul.", "aug.", "sep.", "okt.", "nov.", "dec.")
    date_label = (
        f"{meeting_date.day}. {month_names[meeting_date.month - 1]} {meeting_date.year}"
        if isinstance(meeting_date, date)
        else "Mødedato er ikke angivet"
    )
    generated_now = datetime.now()
    generated_at = f"{generated_now.day}. {month_names[generated_now.month - 1]} {generated_now.year} · {generated_now:%H:%M}"
    st.markdown('<div class="briefing-top">', unsafe_allow_html=True)
    st.markdown('<div class="eyebrow">Ledelsesbriefing · Udarbejdet af AI Key Account Copilot</div>', unsafe_allow_html=True)
    st.title(str(briefing["company"]))
    st.markdown(f'<p class="muted">Kundemøde · {date_label}<br>Genereret {generated_at}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-kicker">Kommercielt perspektiv</div>', unsafe_allow_html=True)
    st.markdown(f'<h2>{briefing["headline"]}</h2>', unsafe_allow_html=True)
    st.markdown(f'<p class="muted">{escape(str(briefing["summary"]))}</p>', unsafe_allow_html=True)
    _render_kpis()

    st.markdown('<div style="height:3.3rem"></div>', unsafe_allow_html=True)
    _render_executive_assessment()

    st.markdown('<div style="height:3.3rem"></div>', unsafe_allow_html=True)
    _section_heading("01", "Ledelsesresumé")
    st.info("**Kommerciel anbefaling:** Brug mødet til at opnå adgang til den næste investeringsbeslutning. Skab en fælles agenda om kapacitet, energi og driftsrobusthed — og aftal et konkret, afgrænset næste skridt med de rette beslutningstagere.")

    _section_heading("02", "Kundeoverblik")
    for column, (label, value) in zip(st.columns(3), briefing["metrics"]):
        with column:
            st.markdown(f'<div class="card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div></div>', unsafe_allow_html=True)

    st.markdown('<div style="height:2.8rem"></div>', unsafe_allow_html=True)
    _section_heading("03", "Kommercielle signaler", "Brug signalerne til at åbne den relevante salgsdialog.")
    for column, (title, body) in zip(st.columns(3), briefing["developments"]):
        with column:
            st.markdown(f'<div class="card"><span class="tag">Signal</span><h3>{title}</h3><p class="muted">{body}</p></div>', unsafe_allow_html=True)

    st.markdown('<div style="height:2.8rem"></div>', unsafe_allow_html=True)
    _section_heading("04", "Hvor kan Schneider Electric skabe værdi?", "Kommercielle spor, der bør omsættes til næste skridt.")
    for opportunity in briefing["opportunities"]:
        _render_opportunity(opportunity)

    st.markdown('<div style="height:2.8rem"></div>', unsafe_allow_html=True)
    _section_heading("05", "Interessentoverblik", "Forbered den rigtige samtale med hver central interessent.")
    for role, priority, objective, conversation, value in briefing["stakeholders"]:
        st.markdown(
            f'''<div class="stakeholder-card"><div class="stakeholder-heading"><span class="strategy-icon">◉</span>{role}</div>
            <div class="stakeholder-grid">
              <div><span class="small-label">Forretningsprioritet</span>{priority}</div>
              <div><span class="small-label">Salgsmål</span>{objective}</div>
              <div><span class="small-label">Foreslået samtale</span>{conversation}</div>
              <div><span class="small-label">Potentiel Schneider-værdi</span>{value}</div>
            </div></div>''',
            unsafe_allow_html=True,
        )

    st.markdown('<div style="height:2.8rem"></div>', unsafe_allow_html=True)
    _section_heading("06", "Spørgsmål der åbner muligheder", "Spørgsmålene skal afdække projekter, beslutningsdrivere og adgang til næste skridt.")
    for index, question in enumerate(briefing["questions"], start=1):
        st.markdown(f'<div class="strategy-row"><div class="strategy-icon">{index}</div><div>{question}</div></div>', unsafe_allow_html=True)

    st.markdown('<div style="height:3.2rem"></div>', unsafe_allow_html=True)
    _render_strategy()

    st.markdown('<div style="height:3.2rem"></div>', unsafe_allow_html=True)
    st.markdown('''<div class="cta-card">
      <div class="eyebrow" style="color:#9ce6aa">Anbefalet næste handling</div>
      <h2>Skab adgang til den næste investeringsbeslutning</h2>
      <p class="muted">Book en teknisk afdækningsworkshop med driftsorganisationen på en prioriteret facilitet. Det er det hurtigste spor til at kvalificere et konkret projekt og etablere Schneider Electric som strategisk partner.</p>
      <div class="strategy-grid" style="margin-top:1.4rem">
        <div class="cta-metric"><div class="cta-metric-label">Forventet kundeværdi</div><div class="cta-metric-value">Fælles prioritering af driftsrisiko og energiindsats</div></div>
        <div class="cta-metric"><div class="cta-metric-label">Forventet Schneider-værdi</div><div class="cta-metric-value">Adgang til projektspor og beslutningstagere</div></div>
        <div class="cta-metric"><div class="cta-metric-label">Vurderingssikkerhed</div><div class="cta-metric-value">91%</div></div>
        <div class="cta-metric"><div class="cta-metric-label">Succeskriterium</div><div class="cta-metric-value">Aftalt workshop, udvalgt facilitet og navngivne ejere</div></div>
      </div>
    </div>''', unsafe_allow_html=True)
