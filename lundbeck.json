"""Purposeful research-progress animation used before rendering a briefing."""

from __future__ import annotations

import time
from html import escape

import streamlit as st

from components.styles import render_brand


TASKS = (
    "Analyserer virksomheden",
    "Læser årsrapport",
    "Gennemgår bæredygtighedsstrategi",
    "Finder seneste investeringer",
    "Analyserer nyheder",
    "Identificerer interessenter",
    "Matcher Schneider Electric-porteføljen",
    "Udarbejder kommercielle muligheder",
    "Udarbejder mødestrategi",
    "Genererer ledelsesbriefing",
)


def _task_markup(active_index: int) -> str:
    """Produce the single, focused active task for the animation frame."""
    completed = active_index
    task = TASKS[active_index]
    return f'''<div class="active-task-panel">
      <div class="active-task-pulse"><span></span></div>
      <div><div class="small-label">I gang nu</div><div class="active-task-name">{task}</div></div>
    </div>
    <div class="loading-status"><span>✓ {completed} af {len(TASKS)} trin gennemført</span><span>Trin {active_index + 1}</span></div>'''


def render_loading() -> None:
    """Animate the research narrative, then enter the executive briefing."""
    render_brand()
    placeholder = st.empty()
    company = escape(st.session_state.company_name)
    seconds_per_step = 1.45
    for active_index in range(len(TASKS)):
        with placeholder.container():
            progress = int(((active_index + 1) / len(TASKS)) * 100)
            seconds_remaining = round((len(TASKS) - active_index - 1) * seconds_per_step)
            st.markdown('<div class="loading-wrap loading-card">', unsafe_allow_html=True)
            st.markdown('<div class="ai-orb">✦</div>', unsafe_allow_html=True)
            st.markdown('<div class="eyebrow">Forberedelse i gang</div>', unsafe_allow_html=True)
            st.markdown(f'<h2>Forbereder {company}</h2>', unsafe_allow_html=True)
            st.markdown('<p class="muted">Udarbejder et skarpt kommercielt udgangspunkt til dit kundemøde.</p>', unsafe_allow_html=True)
            st.markdown(f'<div class="progress-track"><span style="width:{progress}%"></span></div>', unsafe_allow_html=True)
            st.markdown(_task_markup(active_index), unsafe_allow_html=True)
            remaining_label = "Færdiggør din briefing" if seconds_remaining == 0 else f"Forventet resterende tid · {seconds_remaining} sekunder"
            st.markdown(f'<div class="remaining-time">{remaining_label}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        time.sleep(seconds_per_step)
    st.session_state.screen = "briefing"
    st.rerun()
