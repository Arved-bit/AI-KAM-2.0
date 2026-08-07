"""Commercial Insight Engine: company intelligence -> CommercialInsight objects.

This is the only layer in the application that performs business reasoning.
Every function here takes the structured company intelligence dictionary
(currently loaded from demo_data/*.json via services.briefing_data, later
from Azure OpenAI, Microsoft Graph, CRM, SharePoint, news APIs, or annual
reports directly) and returns one or more CommercialInsight objects.

services/briefing_engine.py never reasons about a fact — it only selects and
arranges the CommercialInsight objects produced here. Reordering that
boundary is the point of this sprint: previously the briefing engine
generated finished sentences directly from raw data; now every conclusion is
first captured as an explicit, inspectable reasoning chain:

    fact -> business_implication -> commercial_implication
         -> schneider_positioning -> expected_customer_value

Nothing here depends on Streamlit, and nothing here produces display text —
that stays the presentation layer's job.
"""

from __future__ import annotations

from typing import Any

from services.models import (
    CommercialInsight,
    InsightCategory,
    Priority,
    Source,
    SourceType,
    calculate_confidence,
)


# ---------------------------------------------------------------------------
# Small, shared helpers. None of these hold business reasoning themselves —
# they only support the generators below (slugging, source typing, label
# parsing, light keyword categorisation).
# ---------------------------------------------------------------------------

_DEFAULT_CUSTOMER_VALUE: tuple[str, ...] = ("Lavere driftsrisiko", "Højere effektivitet", "Bedre skalerbarhed")

_DANISH_PRIORITY_TO_ENUM: dict[str, Priority] = {
    "lav": Priority.LOW,
    "mellem": Priority.MEDIUM,
    "høj": Priority.HIGH,
    "kritisk": Priority.CRITICAL,
}

# Keyword hints used only to refine which InsightCategory a fact belongs to.
# A fact keeps its section's default category when nothing matches.
_CATEGORY_KEYWORDS: tuple[tuple[InsightCategory, tuple[str, ...]], ...] = (
    (InsightCategory.ENERGY, ("energi", "mwh", "kwh", "strøm")),
    (InsightCategory.SUSTAINABILITY, ("bæredygtig", "klima", "net-zero", "cirkularitet", "co2")),
    (InsightCategory.MANUFACTURING, ("produktion", "fremstilling", "bioreaktor", "campus", "kapacitet", "fabrik")),
    (InsightCategory.DIGITALISATION, ("digital", "data", "software")),
    (InsightCategory.COMPLIANCE, ("iso ", "gmp", "regulat", "ecovadis", "compliance")),
)


def _slug(value: str) -> str:
    return "-".join(value.strip().casefold().split()) or "insight"


def _refine_category(text: str, default: InsightCategory) -> InsightCategory:
    lowered = text.casefold()
    for category, keywords in _CATEGORY_KEYWORDS:
        if any(keyword in lowered for keyword in keywords):
            return category
    return default


def _source_from_url(url: str) -> Source:
    if not url:
        return Source(SourceType.DEMO_DATA, "demo_data")
    lowered = url.casefold()
    if "sustainab" in lowered or "esg" in lowered:
        return Source(SourceType.SUSTAINABILITY_REPORT, url)
    if lowered.endswith(".pdf") or "annual" in lowered:
        return Source(SourceType.ANNUAL_REPORT, url)
    if "news" in lowered or "press" in lowered:
        return Source(SourceType.PRESS_RELEASE, url)
    return Source(SourceType.COMPANY_WEBSITE, url)


def _priority_from_danish_label(label: str) -> Priority:
    return _DANISH_PRIORITY_TO_ENUM.get(label.strip().casefold(), Priority.MEDIUM)


def _rank_priority(index: int) -> Priority:
    """First item in a naturally-ordered list outranks the rest.

    Demo intelligence lists (facts, risks, stakeholders, ...) are already
    ordered by relevance in the source data, so position is a legitimate,
    deterministic priority signal in the absence of richer scoring inputs.
    """
    return Priority.HIGH if index == 0 else Priority.MEDIUM


# ---------------------------------------------------------------------------
# Category generators. Each one owns the reasoning for its slice of the
# company intelligence and returns fully-formed CommercialInsight objects.
# ---------------------------------------------------------------------------


def generate_strategy_insights(data: dict[str, Any]) -> list[CommercialInsight]:
    company = data["company"]["name"]
    source = _source_from_url(data["strategy"].get("facts_source", ""))
    priorities = data["strategy"]["priorities"]
    insights = []
    for index, priority_fact in enumerate(priorities):
        evidence = [priority_fact, *priorities]
        sources = [source]
        insights.append(
            CommercialInsight(
                id=f"strategy-{_slug(company)}-{index}",
                category=_refine_category(priority_fact, InsightCategory.STRATEGY),
                title=priority_fact,
                fact=priority_fact,
                business_implication=f"{company} har gjort dette til en synlig, offentligt kommunikeret prioritet.",
                commercial_implication="En synlig ledelsesprioritet er et kommercielt indgangspunkt, før konkurrenter positionerer sig.",
                schneider_positioning="Kobl Schneider Electric-porteføljen til den prioritet, hvor kunden allerede har et forretningsbehov.",
                expected_customer_value=_DEFAULT_CUSTOMER_VALUE,
                recommended_motion=data["meeting_context"]["recommended_motion"],
                priority=_rank_priority(index),
                confidence=calculate_confidence(evidence, sources),
                evidence=tuple(evidence),
                sources=tuple(sources),
                tags=("strategy-priority",),
            )
        )
    return insights


def generate_investment_insights(data: dict[str, Any]) -> list[CommercialInsight]:
    return _generate_fact_insights(
        data,
        section="investments",
        category=InsightCategory.INVESTMENT,
        commercial_template="Investeringen skaber et konkret vindue for en tidlig kommerciel dialog, før budgettet er bundet.",
    )


def generate_operations_insights(data: dict[str, Any]) -> list[CommercialInsight]:
    return _generate_fact_insights(
        data,
        section="operations",
        category=InsightCategory.OPERATIONS,
        commercial_template="Driftskompleksiteten øger værdien af integreret data på tværs af energi, bygning og strøm.",
    )


def generate_facilities_insights(data: dict[str, Any]) -> list[CommercialInsight]:
    return _generate_fact_insights(
        data,
        section="facilities",
        category=InsightCategory.FACILITIES,
        commercial_template="Facilitetsniveauet er, hvor en teknisk afdækning konkret kan igangsættes.",
    )


def _generate_fact_insights(
    data: dict[str, Any],
    *,
    section: str,
    category: InsightCategory,
    commercial_template: str,
) -> list[CommercialInsight]:
    company = data["company"]["name"]
    facts = data[section]["facts"]
    interpretations = data[section].get("interpretations", [])
    source = _source_from_url(data["strategy"].get("facts_source", ""))
    insights = []
    for index, fact in enumerate(facts):
        business_implication = interpretations[index] if index < len(interpretations) else interpretations[0] if interpretations else fact
        evidence = [fact, business_implication]
        sources = [source, Source(SourceType.DEMO_DATA, f"demo_data/{section}")]
        insights.append(
            CommercialInsight(
                id=f"{section}-{_slug(company)}-{index}",
                category=_refine_category(fact + " " + business_implication, category),
                title=fact,
                fact=fact,
                business_implication=business_implication,
                commercial_implication=commercial_template,
                schneider_positioning="Positionér Schneider Electric som den partner, der forbinder tekniske valg med målbare driftsresultater.",
                expected_customer_value=_DEFAULT_CUSTOMER_VALUE,
                recommended_motion=data["meeting_context"]["recommended_motion"],
                priority=_rank_priority(index),
                confidence=calculate_confidence(evidence, sources),
                evidence=tuple(evidence),
                sources=tuple(sources),
                tags=(section,),
            )
        )
    return insights


def generate_stakeholder_insights(data: dict[str, Any]) -> list[CommercialInsight]:
    company = data["company"]["name"]
    source = Source(SourceType.DEMO_DATA, "demo_data/stakeholders")
    insights = []
    for index, stakeholder in enumerate(data["stakeholders"]):
        evidence = [stakeholder["role"], stakeholder["priority"], stakeholder["sales_objective"]]
        sources = [source]
        insights.append(
            CommercialInsight(
                id=f"stakeholder-{_slug(company)}-{index}",
                category=InsightCategory.STAKEHOLDER,
                title=stakeholder["role"],
                fact=f"{stakeholder['role']} prioriterer {stakeholder['priority'].lower()}.",
                business_implication=stakeholder["priority"],
                commercial_implication=stakeholder["sales_objective"],
                schneider_positioning="Tilpas samtalen til denne stakeholders beslutningsansvar og succeskriterier.",
                expected_customer_value=_DEFAULT_CUSTOMER_VALUE,
                recommended_motion=data["meeting_context"]["recommended_motion"],
                priority=_rank_priority(index),
                confidence=calculate_confidence(evidence, sources),
                evidence=tuple(evidence),
                sources=tuple(sources),
                tags=("stakeholder",),
            )
        )
    return insights


def generate_risk_insights(data: dict[str, Any]) -> list[CommercialInsight]:
    company = data["company"]["name"]
    source = Source(SourceType.DEMO_DATA, "demo_data/risks")
    insights = []
    for index, risk in enumerate(data["risks"]):
        evidence = [risk]
        sources = [source]
        insights.append(
            CommercialInsight(
                id=f"risk-{_slug(company)}-{index}",
                category=InsightCategory.RISK,
                title=risk,
                fact=risk,
                business_implication="Risikoen kan forsinke eller svække den kommercielle sag, hvis den ikke adresseres tidligt.",
                commercial_implication="Reducér risikoen ved at skabe fælles ejerskab på tværs af de involverede funktioner.",
                schneider_positioning="Brug en afgrænset, målbar første case til at demonstrere værdi før risikoen materialiserer sig.",
                expected_customer_value=_DEFAULT_CUSTOMER_VALUE,
                recommended_motion=data["meeting_context"]["recommended_motion"],
                priority=_rank_priority(index),
                confidence=calculate_confidence(evidence, sources),
                evidence=tuple(evidence),
                sources=tuple(sources),
                tags=("risk",),
            )
        )
    return insights


def generate_commercial_triggers(data: dict[str, Any]) -> list[CommercialInsight]:
    """Fold observed commercial triggers into concrete Schneider Electric motions.

    This is the sprint's headline example: a generator that used to return
    finished briefing text now returns structured CommercialInsight objects,
    one per matched Schneider Electric opportunity, each carrying its own
    fact -> ... -> expected_customer_value reasoning chain.
    """

    company = data["company"]["name"]
    trigger = data["commercial_triggers"][0]
    source = _source_from_url(data["strategy"].get("facts_source", ""))
    insights = []
    for index, opportunity in enumerate(data["schneider_opportunities"]):
        evidence = [trigger["fact"], trigger["commercial_interpretation"], opportunity["customer_outcome"]]
        sources = [source, Source(SourceType.DEMO_DATA, "demo_data/schneider_opportunities")]
        customer_value = tuple(part.strip() for part in opportunity["customer_outcome"].replace(" og ", ", ").split(", ") if part.strip())
        insights.append(
            CommercialInsight(
                id=f"opportunity-{_slug(company)}-{index}",
                category=InsightCategory.OPPORTUNITY,
                title=opportunity["title"],
                fact=trigger["fact"],
                business_implication=trigger["commercial_interpretation"],
                commercial_implication=f"Skaber en tidlig kommerciel indgang til en dialog om {opportunity['portfolio']}.",
                schneider_positioning=opportunity["portfolio"],
                expected_customer_value=customer_value or _DEFAULT_CUSTOMER_VALUE,
                recommended_motion=data["meeting_context"]["recommended_motion"],
                priority=_priority_from_danish_label(opportunity["priority"]),
                confidence=calculate_confidence(evidence, sources),
                evidence=tuple(evidence),
                sources=tuple(sources),
                tags=("commercial-trigger", "schneider-opportunity"),
            )
        )
    return insights


def generate_meeting_insights(data: dict[str, Any]) -> list[CommercialInsight]:
    company = data["company"]["name"]
    context = data["meeting_context"]
    source = Source(SourceType.DEMO_DATA, "demo_data/meeting_context")
    evidence = [context["recommended_motion"], context["investment_horizon"]]
    sources = [source]
    return [
        CommercialInsight(
            id=f"meeting-{_slug(company)}-0",
            category=InsightCategory.MEETING,
            title=context["recommended_motion"],
            fact=f"Investeringshorisont på {context['investment_horizon']} understøtter {context['recommended_motion'].lower()}.",
            business_implication="Beslutningen har en defineret tidshorisont, hvor kravene endnu ikke er låst.",
            commercial_implication="Tidlig adgang inden for horisonten øger sandsynligheden for at forme kravene og standarderne.",
            schneider_positioning="Brug motion til at sikre adgang til de rette beslutningstagere, før valg er truffet.",
            expected_customer_value=_DEFAULT_CUSTOMER_VALUE,
            recommended_motion=context["recommended_motion"],
            priority=Priority.HIGH,
            confidence=calculate_confidence(evidence, sources),
            evidence=tuple(evidence),
            sources=tuple(sources),
            tags=("meeting",),
        )
    ]


def generate_all_insights(data: dict[str, Any]) -> list[CommercialInsight]:
    """Run every category generator and return the full insight set for a company."""
    return [
        *generate_strategy_insights(data),
        *generate_investment_insights(data),
        *generate_operations_insights(data),
        *generate_facilities_insights(data),
        *generate_stakeholder_insights(data),
        *generate_risk_insights(data),
        *generate_commercial_triggers(data),
        *generate_meeting_insights(data),
    ]
