"""Briefing composition: arranges CommercialInsight objects into a report.

Architecture (Sprint 8):

    Company Data -> CommercialInsight objects -> Executive Briefing

services/insight_engine.py owns all business reasoning and produces
CommercialInsight objects (see services/models.py). This module does the
opposite job on purpose: it contains NO business reasoning. Every fact,
implication, and recommendation shown in the briefing already exists on a
CommercialInsight before this module ever runs — here we only select,
order, and format that data into the BriefingSection / Opportunity /
StakeholderStrategy / BriefingDocument shapes that components/briefing.py
renders.

That presentation contract (the four dataclasses below) is intentionally
unchanged from the previous architecture so the UI layer needed no changes
for this refactor. The Executive Briefing is one possible presentation of
the underlying CommercialInsight set — a future dashboard, export, or CRM
sync could read the same insights and look completely different.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

from services.briefing_data import load_company_intelligence
from services.insight_engine import generate_all_insights
from services.models import CommercialInsight, Priority, top_insights


@dataclass(frozen=True)
class BriefingSection:
    """Ensartet outputkontrakt for alle genererede briefingsektioner."""

    title: str
    summary: str
    key_points: tuple[str, ...]
    commercial_conclusion: str
    confidence: int


@dataclass(frozen=True)
class Opportunity:
    title: str
    trigger: str
    why_now: str
    portfolio: str
    customer_outcome: str
    priority: str
    confidence: int


@dataclass(frozen=True)
class StakeholderStrategy:
    role: str
    priority: str
    sales_objective: str
    conversation: str
    schneider_value: str


@dataclass(frozen=True)
class BriefingDocument:
    company_name: str
    sector: str
    assessment: BriefingSection
    customer_strategy: BriefingSection
    commercial_signals: BriefingSection
    schneider_positioning: BriefingSection
    stakeholder_strategy: BriefingSection
    meeting_strategy: BriefingSection
    questions: BriefingSection
    commercial_risks: BriefingSection
    action_plan: BriefingSection
    opportunities: tuple[Opportunity, ...]
    stakeholders: tuple[StakeholderStrategy, ...]
    kpis: tuple[tuple[str, str, str, str], ...]
    meeting_context: dict[str, Any]


def _section(title: str, summary: str, key_points: list[str], conclusion: str, confidence: int) -> BriefingSection:
    return BriefingSection(title, summary, tuple(key_points), conclusion, confidence)


def _by_tag(insights: Sequence[CommercialInsight], tag: str) -> list[CommercialInsight]:
    """Insights tagged by an insight_engine generator, in generation order."""
    return [insight for insight in insights if tag in insight.tags]


def _avg_confidence(insights: Sequence[CommercialInsight], default: int = 60) -> int:
    if not insights:
        return default
    return round(sum(insight.confidence for insight in insights) / len(insights))


# The UI's opportunity card (components/briefing.py) only understands three
# Danish priority labels. CommercialInsight supports four priority levels
# internally (see services/models.py); this presentation-only mapping caps
# CRITICAL to the same visual treatment as HIGH so the unmodified UI keeps
# working. This is formatting, not reasoning — the underlying priority is
# preserved on the CommercialInsight itself.
_PRIORITY_LABEL_DA: dict[Priority, str] = {
    Priority.LOW: "Lav",
    Priority.MEDIUM: "Mellem",
    Priority.HIGH: "Høj",
    Priority.CRITICAL: "Høj",
}


def _priority_label(priority: Priority) -> str:
    return _PRIORITY_LABEL_DA[priority]


_POTENTIAL_LABEL_DA: dict[Priority, str] = {
    Priority.LOW: "Lavt",
    Priority.MEDIUM: "Moderat",
    Priority.HIGH: "Højt",
    Priority.CRITICAL: "Kritisk",
}


def _match_label(insights: Sequence[CommercialInsight]) -> str:
    if not insights:
        return "Ikke vurderet"
    high_share = sum(1 for insight in insights if insight.priority.rank >= Priority.HIGH.rank) / len(insights)
    if high_share >= 0.6:
        return "Meget stærkt"
    if high_share >= 0.35:
        return "Stærkt"
    return "Moderat"


def generate_executive_assessment(insights: list[CommercialInsight], data: dict[str, Any]) -> BriefingSection:
    company = data["company"]["name"]
    drivers = ", ".join(data["business_drivers"][:3])
    horizon = data["meeting_context"]["investment_horizon"]
    motion = data["meeting_context"]["recommended_motion"]
    leading = top_insights(insights, 5)
    lead = leading[0] if leading else None
    conclusion = lead.schneider_positioning if lead else "Prioritér adgang til de funktioner, der kan definere projektrammer."
    return _section(
        "Kommerciel vurdering",
        f"{company} er relevant for Schneider Electric, når vi kobler {drivers.lower()} til en tidlig dialog om næste investering.",
        [
            f"Kommercielt potentiale: {_POTENTIAL_LABEL_DA[lead.priority] if lead else 'Ikke vurderet'}",
            f"Strategisk match: {_match_label(insights)}",
            f"Investeringshorisont: {horizon}",
            f"Primære drivere: {drivers}",
            f"Anbefalet tilgang: {motion}",
        ],
        conclusion,
        _avg_confidence(leading),
    )


def generate_customer_strategy(insights: list[CommercialInsight], data: dict[str, Any]) -> BriefingSection:
    strategy_insights = _by_tag(insights, "strategy-priority")
    points = [insight.title for insight in strategy_insights] or list(data["strategy"]["priorities"])
    return _section(
        "Kundeoverblik",
        "Kundens offentlige prioriteter skal bruges som kommercielle indgange — ikke som baggrundsbeskrivelse.",
        points,
        "Kobl Schneider Electric-porteføljen til de prioriteringer, hvor kunden allerede har et synligt forretningsbehov.",
        _avg_confidence(strategy_insights),
    )


def generate_commercial_signals(insights: list[CommercialInsight], data: dict[str, Any]) -> BriefingSection:
    """Composition of Opportunity insights into the 'signals' section (see module docstring).

    Note this is deliberately distinct from insight_engine.generate_commercial_triggers,
    which performs the actual reasoning and now returns CommercialInsight objects — this
    function only arranges a subset of that output for display.
    """
    trigger_insights = _by_tag(insights, "commercial-trigger")
    operations_insights = _by_tag(insights, "operations")
    facilities_insights = _by_tag(insights, "facilities")
    points = [insight.fact for insight in trigger_insights[:1]]
    points += [insight.fact for insight in operations_insights[:1]]
    points += [insight.fact for insight in facilities_insights[:1]]
    conclusion = trigger_insights[0].business_implication if trigger_insights else ""
    return _section(
        "Kommercielle signaler",
        conclusion,
        points,
        "Brug signalet til at skabe adgang før løsninger og standarder er valgt.",
        trigger_insights[0].confidence if trigger_insights else _avg_confidence(insights),
    )


def generate_schneider_positioning(insights: list[CommercialInsight], data: dict[str, Any]) -> BriefingSection:
    opportunity_insights = _by_tag(insights, "schneider-opportunity")
    portfolios = [insight.schneider_positioning for insight in opportunity_insights]
    return _section(
        "Schneider Electric-positionering",
        "Schneider Electric bør samle drifts-, energi- og strømagendaen i én kommerciel plan.",
        portfolios,
        "Positionér Schneider Electric som den partner, der forbinder tekniske valg med målbare driftsresultater.",
        _avg_confidence(opportunity_insights),
    )


def generate_stakeholder_strategy(insights: list[CommercialInsight], data: dict[str, Any]) -> BriefingSection:
    stakeholder_insights = _by_tag(insights, "stakeholder")
    roles = [insight.title for insight in stakeholder_insights]
    return _section(
        "Interessentoverblik",
        "Hver samtale skal give adgang til en beslutning, et projekt eller en prioriteret facilitet.",
        roles,
        "Skab en fælles ejerkreds på tværs af drift, teknik og bæredygtighed.",
        _avg_confidence(stakeholder_insights),
    )


def generate_meeting_strategy(insights: list[CommercialInsight], data: dict[str, Any]) -> BriefingSection:
    """Meeting strategy is a composition of Stakeholder insights."""
    stakeholder_insights = _by_tag(insights, "stakeholder")
    meeting_insights = _by_tag(insights, "meeting")
    driver = data["business_drivers"][0].lower()
    key_points = ["Åbn med den forretningsmæssige konsekvens af manglende fremdrift."]
    key_points += [f"{insight.title}: {insight.commercial_implication}" for insight in stakeholder_insights[:2]]
    key_points.append("Foreslå en facilitet og et sæt målbare succeskriterier.")
    conclusion = (
        meeting_insights[0].commercial_implication
        if meeting_insights
        else "Målet er ikke en produktdialog; målet er en aftalt workshop med de rette ejere."
    )
    return _section(
        "Anbefalet mødestrategi",
        f"Indled med kundens agenda om {driver}, og brug den til at skabe mandat til en afgrænset teknisk afdækning.",
        key_points,
        conclusion,
        _avg_confidence(stakeholder_insights or meeting_insights),
    )


def generate_questions(insights: list[CommercialInsight], data: dict[str, Any]) -> BriefingSection:
    primary_driver = data["business_drivers"][0].lower()
    meeting_insights = _by_tag(insights, "meeting")
    motion = (meeting_insights[0].recommended_motion if meeting_insights else data["meeting_context"]["recommended_motion"]).lower()
    questions = [
        "Hvilken investering eller ændring i driften skal besluttes først, og hvornår låses standarderne?",
        f"Hvilken risiko omkring {primary_driver} har størst økonomisk konsekvens i den prioriterede facilitet?",
        f"Hvem skal være enige, før I kan igangsætte {motion}?",
    ]
    return _section(
        "Spørgsmål der åbner muligheder",
        "Spørgsmålene skal åbne projekter, beslutningsdrivere og næste skridt.",
        questions,
        "Afslut hvert spørgsmål med et konkret næste skridt, ikke en teknisk diskussion.",
        _avg_confidence(meeting_insights),
    )


def generate_commercial_risks(insights: list[CommercialInsight], data: dict[str, Any]) -> BriefingSection:
    risk_insights = _by_tag(insights, "risk")
    points = [insight.fact for insight in risk_insights]
    conclusion = (
        risk_insights[0].commercial_implication
        if risk_insights
        else "Reducer risikoen ved at skabe fælles ejerskab og en konkret, målbar første case."
    )
    return _section(
        "Kommercielle risici",
        "Kend de forhold, der kan forsinke adgang eller svække den kommercielle sag.",
        points,
        conclusion,
        _avg_confidence(risk_insights),
    )


def generate_action_plan(insights: list[CommercialInsight], data: dict[str, Any]) -> BriefingSection:
    """Action plan is a composition of Recommended Motion insights."""
    meeting_insights = _by_tag(insights, "meeting")
    motion = meeting_insights[0].recommended_motion if meeting_insights else data["meeting_context"]["recommended_motion"]
    return _section(
        "Anbefalet næste handling",
        f"Book {motion.lower()} med de relevante ejere og én prioriteret facilitet som udgangspunkt.",
        ["Aftal workshop og deltagere", "Vælg facilitet og kommercielt problem", "Fastlæg målbare succeskriterier"],
        "Dette er det hurtigste spor til at kvalificere en konkret mulighed og opnå adgang til næste investering.",
        _avg_confidence(meeting_insights or insights),
    )


def _build_opportunities(insights: list[CommercialInsight]) -> tuple[Opportunity, ...]:
    opportunity_insights = _by_tag(insights, "schneider-opportunity")
    return tuple(
        Opportunity(
            title=insight.title,
            trigger=insight.business_implication,
            why_now="Kom ind før investerings- og standardbeslutninger er låst.",
            portfolio=insight.schneider_positioning,
            customer_outcome=", ".join(insight.expected_customer_value),
            priority=_priority_label(insight.priority),
            confidence=insight.confidence,
        )
        for insight in opportunity_insights
    )


def _build_stakeholders(insights: list[CommercialInsight]) -> tuple[StakeholderStrategy, ...]:
    stakeholder_insights = _by_tag(insights, "stakeholder")
    return tuple(
        StakeholderStrategy(
            role=insight.title,
            priority=insight.business_implication,
            sales_objective=insight.commercial_implication,
            conversation=f"Hvad skal lykkes for at {insight.business_implication.lower()}?",
            schneider_value="En samlet plan for energi, bygning og strøm med målbar forretningsværdi.",
        )
        for insight in stakeholder_insights
    )


def generate_briefing(company_name: str) -> BriefingDocument:
    """Loads company intelligence, derives CommercialInsight objects, and composes the briefing."""
    data = load_company_intelligence(company_name)
    insights = generate_all_insights(data)

    opportunities = _build_opportunities(insights)
    stakeholders = _build_stakeholders(insights)
    overall_confidence = _avg_confidence(insights)

    return BriefingDocument(
        company_name=data["company"]["name"],
        sector=data["company"]["sector"],
        assessment=generate_executive_assessment(insights, data),
        customer_strategy=generate_customer_strategy(insights, data),
        commercial_signals=generate_commercial_signals(insights, data),
        schneider_positioning=generate_schneider_positioning(insights, data),
        stakeholder_strategy=generate_stakeholder_strategy(insights, data),
        meeting_strategy=generate_meeting_strategy(insights, data),
        questions=generate_questions(insights, data),
        commercial_risks=generate_commercial_risks(insights, data),
        action_plan=generate_action_plan(insights, data),
        opportunities=opportunities,
        stakeholders=stakeholders,
        kpis=(
            ("✓", "Mødeparathed", f"{overall_confidence}%", "Klar til kommerciel dialog"),
            ("✦", "Vurderingssikkerhed", f"{_avg_confidence(top_insights(insights, 5))}%", "Struktureret offentligt datagrundlag"),
            ("◌", "Salgsmuligheder", str(len(opportunities)), "Prioriterede kommercielle spor"),
            ("◷", "Læsetid", data["meeting_context"]["reading_time"], "Kort briefing til mødelokalet"),
        ),
        meeting_context=data["meeting_context"],
    )
