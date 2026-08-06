"""Shared visual system for the AI Key Account Copilot demo."""

from __future__ import annotations

import streamlit as st


def apply_global_styles() -> None:
    """Apply the product's white, editorial, Fluent-inspired visual language."""
    st.markdown(
        """
        <style>
          @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
          :root { --ink:#1d252d; --muted:#64707a; --green:#3dcd58; --green-dark:#218838; --green-ink:#176b2b; --line:#e4e8e5; --surface:#f5f7f5; --soft-green:#f1faf3; --navy:#173b2d; }
          .stApp { background: #ffffff; color: var(--ink); font-family: 'DM Sans', sans-serif; }
          #MainMenu, footer, header { visibility: hidden; }
          .block-container { max-width: 1200px; padding: 1.4rem 3rem 4.5rem; }
          h1, h2, h3 { font-family: 'Manrope', sans-serif; letter-spacing: -0.04em; color: var(--ink); }
          h1 { font-size: 3.55rem !important; line-height: 1.08 !important; font-weight: 800 !important; }
          h2 { font-size: 1.85rem !important; margin: .1rem 0 .85rem !important; }
          h3 { font-size: 1.02rem !important; letter-spacing: -.02em; }
          .stButton > button { background: var(--green); color: #112318; border: 0; border-radius: 7px; font: 700 .9rem 'DM Sans', sans-serif; padding: .76rem 1.25rem; min-height: 46px; box-shadow: 0 5px 12px rgba(40,130,59,.10); transition: all .18s ease; }
          .stButton > button:hover { background: #2db74a; transform: translateY(-1px); box-shadow: 0 5px 12px rgba(40,130,59,.16); }
          .stButton > button[kind="secondary"], button[data-testid="baseButton-secondary"] { background:#fff; color:#334039; border:1px solid #d8dfd9; box-shadow:none; }
          .stButton > button[kind="secondary"]:hover, button[data-testid="baseButton-secondary"]:hover { background:var(--soft-green); border-color:#9cd7a9; }
          div[data-baseweb="input"] > div, div[data-baseweb="select"] > div { border-color: #dce3ed; border-radius: 9px; min-height: 48px; }
          div[data-baseweb="input"] > div:focus-within { border-color: var(--green-dark); box-shadow: 0 0 0 3px rgba(61,205,88,.16); }
          .brand { display:flex; align-items:center; gap:10px; color:#1d252d; font:700 .94rem 'Manrope',sans-serif; letter-spacing:-.02em; }
          .brand-mark { display:grid; place-items:center; height:29px; width:29px; border-radius:5px; color:#102b18; background:var(--green); font-size:15px; }
          .eyebrow { color:var(--green-ink); font-weight:700; font-size:.72rem; letter-spacing:.1em; text-transform:uppercase; }
          .muted { color:var(--muted); font-size:1rem; line-height:1.65; }
          .section-kicker { color:var(--green-ink); font-weight:700; font-size:.72rem; letter-spacing:.1em; text-transform:uppercase; margin-bottom:.35rem; }
          .card { background:#fff; border:1px solid var(--line); border-radius:12px; padding:1.5rem; height:100%; box-sizing:border-box; box-shadow:0 5px 16px rgba(27,42,32,.04); transition:transform .18s ease,box-shadow .18s ease; }
          .card:hover { transform:translateY(-2px); box-shadow:0 10px 24px rgba(27,42,32,.075); }
          .metric-label { color:var(--muted); font-size:.78rem; font-weight:600; text-transform:uppercase; letter-spacing:.07em; }
          .metric-value { color:var(--ink); font:800 1.55rem 'Manrope',sans-serif; letter-spacing:-.05em; margin-top:.25rem; }
          .tag { display:inline-block; padding:.26rem .58rem; border-radius:99px; color:var(--green-ink); background:#e7f7ea; font-size:.74rem; font-weight:700; }
          .priority-high { color:#a24510; background:#fff0e8; }
          .priority-medium { color:#796020; background:#fff7d9; }
          .opportunity { border-left:3px solid var(--green); background:#fbfdfb; padding:1.25rem 1.3rem; border-radius:0 10px 10px 0; margin:.9rem 0; }
          .high-opportunity { border-left-width:4px; border-top:1px solid #f4d2bd; border-right:1px solid #f4d2bd; border-bottom:1px solid #f4d2bd; background:#fffdfa; }
          .opportunity-title { font-weight:700; color:var(--ink); margin-bottom:.35rem; }
          .small-label { color:var(--muted); font-size:.76rem; font-weight:700; letter-spacing:.06em; text-transform:uppercase; }
          .strategy-row { display:flex; gap:13px; align-items:flex-start; padding:.9rem 0; border-bottom:1px solid var(--line); }
          .strategy-row:last-child { border-bottom:0; }
          .strategy-icon { flex:0 0 27px; display:grid; place-items:center; width:27px; height:27px; border-radius:6px; background:#e7f7ea; color:var(--green-ink); font-weight:700; }
          .briefing-top { display:flex; justify-content:space-between; align-items:flex-start; padding:1.65rem 0 2.3rem; border-bottom:1px solid var(--line); margin-bottom:2.6rem; }
          .loading-wrap { max-width:650px; margin: 12vh auto 0; }
          .loading-card { padding:3rem 3.2rem; border:1px solid var(--line); border-radius:18px; box-shadow:0 18px 50px rgba(24,48,32,.09); background:#fff; }
          .ai-orb { display:grid; place-items:center; height:42px; width:42px; border-radius:13px; color:#176b2b; background:#e7f7ea; font-size:1.2rem; margin-bottom:1.35rem; }
          .progress-track { overflow:hidden; height:4px; border-radius:99px; background:#edf1ed; margin:1.7rem 0 .65rem; }
          .progress-track span { display:block; height:100%; border-radius:99px; background:var(--green); transition:width .45s ease; }
          .active-task-panel { display:flex; align-items:center; gap:1rem; min-height:78px; margin:.25rem 0 .8rem; padding:1.1rem 1.2rem; border-radius:12px; background:var(--soft-green); border:1px solid #d9efde; }
          .active-task-pulse { display:grid; place-items:center; flex:0 0 34px; width:34px; height:34px; border-radius:50%; background:rgba(61,205,88,.16); }
          .active-task-pulse span { display:block; width:11px; height:11px; border-radius:50%; background:var(--green-dark); animation:aiPulse 1.4s ease-in-out infinite; }
          .active-task-name { margin-top:.15rem; font:700 1.05rem 'Manrope',sans-serif; letter-spacing:-.025em; color:var(--ink); }
          .loading-status { display:flex; justify-content:space-between; color:var(--muted); font-size:.78rem; font-weight:600; }
          .remaining-time { margin-top:1.35rem; color:var(--muted); font-size:.83rem; text-align:center; }
          .loading-task { display:flex; align-items:center; gap:14px; padding:13px 0; border-bottom:1px solid var(--line); color:#25334a; font-size:.95rem; transition:all .35s ease; }
          .loading-dot { width:25px; height:25px; border-radius:50%; background:#eff3f8; color:#8c98a9; display:grid; place-items:center; font-size:.75rem; }
          .loading-done .loading-dot { background:#e4f4e9; color:#16813b; }
          .loading-active { color:var(--green-ink); font-weight:700; }
          .loading-active .loading-dot { background:#e7f7ea; color:var(--green-ink); }
          .quick-start-label { color:var(--muted); font-size:.78rem; font-weight:700; letter-spacing:.05em; margin:0 0 .55rem; }
          .landing-lead { max-width:700px; font-size:1.08rem; }
          .landing-greeting { margin-top:2.35rem; color:var(--muted); font:500 1rem 'DM Sans',sans-serif; }
          .landing-eyebrow { margin-top:1.15rem; }
          .landing-hero-copy { max-width:820px; margin:1rem 0 1.2rem; font-size:1.12rem; line-height:1.7; }
          .landing-question { margin:1.6rem 0 2rem; color:var(--ink); font:650 1.08rem 'Manrope',sans-serif; letter-spacing:-.025em; }
          div[data-testid="stVerticalBlockBorderWrapper"] { border:1px solid #dce5de; border-radius:16px; background:#fff; box-shadow:0 15px 36px rgba(25,54,35,.065); }
          div[data-testid="stVerticalBlockBorderWrapper"] > div { padding:1.75rem 1.85rem 1.85rem; }
          .landing-workflow-title { color:var(--ink); font:750 1.18rem 'Manrope',sans-serif; letter-spacing:-.03em; }
          .landing-workflow-subtitle { margin:.35rem 0 1.5rem; color:var(--muted); font-size:.92rem; }
          .landing-field-space { height:.8rem; }
          div[data-testid="stVerticalBlockBorderWrapper"] .stButton > button[kind="primary"] { min-height:56px; border-radius:9px; font-size:.98rem; }
          div[data-testid="stVerticalBlockBorderWrapper"] .stButton > button[kind="secondary"] { min-height:44px; border-radius:8px; }
          .landing-value-heading { margin:5.8rem 0 1.5rem; max-width:700px; }
          .landing-value-heading h2 { margin-top:.38rem !important; }
          .landing-value-card { min-height:205px; padding:1.65rem; border:1px solid var(--line); border-radius:14px; background:#fff; box-shadow:0 5px 18px rgba(27,42,32,.04); transition:transform .2s ease,box-shadow .2s ease; }
          .landing-value-card:hover { transform:translateY(-3px); box-shadow:0 14px 30px rgba(27,42,32,.075); }
          .landing-card-number { display:grid; place-items:center; width:30px; height:30px; margin-bottom:1.25rem; border-radius:8px; color:var(--green-ink); background:#e7f7ea; font-weight:700; font-size:.76rem; }
          .hero-kpi { background:#fff; border:1px solid var(--line); border-radius:12px; padding:1.15rem 1.2rem; min-height:112px; box-shadow:0 4px 16px rgba(27,42,32,.04); }
          .hero-kpi-icon { display:inline-grid; place-items:center; height:28px; width:28px; margin-bottom:.6rem; border-radius:8px; color:var(--green-ink); background:#e7f7ea; font-size:.85rem; }
          .hero-kpi-label { color:var(--muted); font-size:.73rem; font-weight:700; letter-spacing:.06em; text-transform:uppercase; }
          .hero-kpi-value { color:var(--ink); font:800 1.42rem 'Manrope',sans-serif; letter-spacing:-.05em; margin-top:.15rem; }
          .hero-kpi-detail { color:var(--muted); font-size:.77rem; line-height:1.35; margin-top:.3rem; }
          .assessment-panel { padding:2.1rem 2.25rem; border:1px solid #cfe8d4; border-radius:16px; background:linear-gradient(115deg,#f1faf3,#ffffff 72%); box-shadow:0 12px 30px rgba(35,118,52,.07); }
          .assessment-title { max-width:780px; margin:.25rem 0 1.45rem; font:800 1.55rem/1.25 'Manrope',sans-serif; letter-spacing:-.04em; color:var(--ink); }
          .assessment-grid { display:grid; grid-template-columns:repeat(5,1fr); gap:.75rem; }
          .assessment-item { padding:1rem; border-radius:10px; background:rgba(255,255,255,.82); border:1px solid #e1ece3; }
          .assessment-value { margin:.35rem 0; font:750 1rem/1.25 'Manrope',sans-serif; letter-spacing:-.025em; color:var(--green-ink); }
          .assessment-detail { color:var(--muted); font-size:.76rem; line-height:1.38; }
          .opportunity-grid { display:grid; grid-template-columns:1fr 1fr; gap:.75rem 1.5rem; margin-top:.9rem; }
          .opportunity-field { font-size:.9rem; line-height:1.45; }
          .opportunity-field .small-label { display:block; margin-bottom:.14rem; }
          .opportunity-icon { display:inline-grid; place-items:center; width:31px; height:31px; margin-right:.55rem; vertical-align:middle; border-radius:8px; color:var(--green-ink); background:#e7f7ea; }
          .opportunity-heading { font:750 1.08rem 'Manrope',sans-serif; letter-spacing:-.025em; color:var(--ink); }
          .priority-low { color:#4e6874; background:#edf3f4; }
          .stakeholder-card { margin:.8rem 0; padding:1.35rem; border:1px solid var(--line); border-radius:12px; background:#fff; box-shadow:0 4px 15px rgba(27,42,32,.035); }
          .stakeholder-heading { display:flex; align-items:center; gap:.6rem; margin-bottom:1rem; font:750 1.02rem 'Manrope',sans-serif; letter-spacing:-.02em; }
          .stakeholder-grid { display:grid; grid-template-columns:1fr 1fr; gap:.9rem 1.6rem; font-size:.9rem; line-height:1.45; }
          .stakeholder-grid .small-label { display:block; margin-bottom:.15rem; }
          .strategy-centrepiece { padding:2.15rem 2.25rem; border:1px solid #b9e8c3; border-radius:16px; background:linear-gradient(120deg,#f1fbf3,#ffffff 68%); box-shadow:0 12px 30px rgba(35,118,52,.08); }
          .strategy-title { font:800 1.65rem 'Manrope',sans-serif; letter-spacing:-.045em; color:var(--ink); margin:.25rem 0 1.25rem; }
          .strategy-grid { display:grid; grid-template-columns:1fr 1fr; gap:.25rem 2rem; }
          .cta-card { padding:2.15rem 2.25rem; border-radius:16px; color:#fff; background:#193f2a; box-shadow:0 14px 32px rgba(20,54,35,.16); }
          .cta-card h2 { color:#fff; margin:.35rem 0 .65rem !important; }
          .cta-card .muted { color:#dcebe0; }
          .cta-metric { border-left:1px solid rgba(255,255,255,.22); padding-left:1rem; }
          .cta-metric-label { color:#b9d7c0; font-size:.7rem; font-weight:700; letter-spacing:.08em; text-transform:uppercase; }
          .cta-metric-value { font:700 1rem 'Manrope',sans-serif; margin-top:.25rem; }
          @keyframes aiPulse { 0%,100% { transform:scale(.82); opacity:.6; } 50% { transform:scale(1.15); opacity:1; } }
          @media(max-width:900px) { .assessment-grid { grid-template-columns:repeat(2,1fr); } }
          @media(max-width:700px) { .block-container { padding:1.2rem 1.15rem 3rem; } h1 { font-size:2.45rem !important; } .briefing-top { display:block; } .loading-card,.strategy-centrepiece,.cta-card,.assessment-panel { padding:1.5rem; } .opportunity-grid,.strategy-grid,.stakeholder-grid,.assessment-grid { grid-template-columns:1fr; } .loading-status { gap:.5rem; flex-direction:column; } .landing-greeting { margin-top:2.5rem; } .landing-value-heading { margin-top:3.8rem; } div[data-testid="stVerticalBlockBorderWrapper"] > div { padding:1.3rem; } }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_brand() -> None:
    st.markdown(
        '<div class="brand"><span class="brand-mark">◆</span> AI Key Account Copilot</div>',
        unsafe_allow_html=True,
    )
