"""Domain model for structured commercial intelligence.

CommercialInsight is the reusable, presentation-agnostic building block of
the application. It captures one link in the reasoning chain from an
observed fact about a company to a recommended commercial motion:

    fact -> business_implication -> commercial_implication
         -> schneider_positioning -> expected_customer_value

Everything downstream — the executive briefing, and eventually other
presentation layers — is built by selecting and arranging CommercialInsight
objects. Nothing outside this module and services/insight_engine.py should
invent business reasoning from raw company data.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Sequence


class InsightCategory(str, Enum):
    """The commercial domains a CommercialInsight can belong to.

    Not every company profile will produce insights in every category —
    categories describe what the model supports, not what every run uses.
    """

    STRATEGY = "Strategy"
    INVESTMENT = "Investment"
    OPERATIONS = "Operations"
    ENERGY = "Energy"
    SUSTAINABILITY = "Sustainability"
    MANUFACTURING = "Manufacturing"
    DIGITALISATION = "Digitalisation"
    FACILITIES = "Facilities"
    STAKEHOLDER = "Stakeholder"
    RISK = "Risk"
    OPPORTUNITY = "Opportunity"
    COMPLIANCE = "Compliance"
    MEETING = "Meeting"


class Priority(str, Enum):
    """Commercial priority of an insight, independent of any presentation label."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

    @property
    def rank(self) -> int:
        """Sortable weight, highest priority first."""
        return {"LOW": 0, "MEDIUM": 1, "HIGH": 2, "CRITICAL": 3}[self.value]


class SourceType(str, Enum):
    """Where a piece of evidence originates.

    Includes both the sources available today (public company research used
    to build demo profiles) and integrations the architecture is designed to
    accept later (see services/insight_engine.py module docstring) without
    changing CommercialInsight itself.
    """

    ANNUAL_REPORT = "Annual Report"
    SUSTAINABILITY_REPORT = "Sustainability Report"
    PRESS_RELEASE = "Press Release"
    COMPANY_WEBSITE = "Company Website"
    NEWS = "News"
    DEMO_DATA = "Demo Data"
    CRM = "CRM"
    SHAREPOINT = "SharePoint"
    MICROSOFT_GRAPH = "Microsoft Graph"
    AZURE_OPENAI = "Azure OpenAI"


# Relative evidentiary strength per source type. Used only by
# calculate_confidence() below — a deterministic input, not a claim about
# real-world reliability.
_SOURCE_STRENGTH: dict[SourceType, float] = {
    SourceType.ANNUAL_REPORT: 1.0,
    SourceType.SUSTAINABILITY_REPORT: 0.95,
    SourceType.CRM: 0.9,
    SourceType.PRESS_RELEASE: 0.85,
    SourceType.SHAREPOINT: 0.85,
    SourceType.MICROSOFT_GRAPH: 0.85,
    SourceType.COMPANY_WEBSITE: 0.8,
    SourceType.NEWS: 0.75,
    SourceType.AZURE_OPENAI: 0.6,
    SourceType.DEMO_DATA: 0.6,
}


@dataclass(frozen=True)
class Source:
    """A single reference backing a CommercialInsight.

    ``reference`` is a free-text locator (a URL, document name, or short
    note) and is optional so that lightweight sources can still be recorded.
    """

    source_type: SourceType
    reference: str = ""


@dataclass(frozen=True)
class CommercialInsight:
    """One structured unit of commercial intelligence about a company.

    This is the central object the whole application is built around. A
    report is only one possible presentation of a collection of these.
    """

    id: str
    category: InsightCategory
    title: str
    fact: str
    business_implication: str
    commercial_implication: str
    schneider_positioning: str
    expected_customer_value: tuple[str, ...]
    recommended_motion: str
    priority: Priority
    confidence: int
    evidence: tuple[str, ...] = field(default_factory=tuple)
    sources: tuple[Source, ...] = field(default_factory=tuple)
    tags: tuple[str, ...] = field(default_factory=tuple)


def calculate_confidence(evidence: Sequence[str], sources: Sequence[Source]) -> int:
    """Deterministic confidence score in the range [35, 97].

    No hardcoded per-insight confidence values anywhere in the codebase —
    every CommercialInsight computes its own score from three legible,
    reproducible factors:

      1. amount of supporting evidence (distinct corroborating facts),
      2. how many separate sources back the insight, and
      3. the average evidentiary strength of those sources.

    This is a deterministic scoring model, not an AI-generated estimate, as
    required by the sprint spec — it can be replaced or extended later
    (e.g. once real source strength data arrives from Microsoft Graph, CRM,
    or news APIs) without changing its callers.
    """

    distinct_evidence = {item.strip().lower() for item in evidence if item.strip()}
    evidence_score = min(len(distinct_evidence) * 9, 30)

    if sources:
        avg_strength = sum(_SOURCE_STRENGTH.get(s.source_type, 0.6) for s in sources) / len(sources)
        source_count_score = min(len(sources) * 4, 12)
    else:
        avg_strength = 0.6
        source_count_score = 0
    strength_score = round(avg_strength * 20)

    base = 35
    score = base + evidence_score + strength_score + source_count_score
    return max(35, min(97, round(score)))


def top_insights(insights: Sequence[CommercialInsight], limit: int) -> list[CommercialInsight]:
    """Highest-priority insights first, ties broken by confidence."""
    return sorted(insights, key=lambda item: (item.priority.rank, item.confidence), reverse=True)[:limit]


def by_category(insights: Sequence[CommercialInsight], category: InsightCategory) -> list[CommercialInsight]:
    """All insights in a given category, in their original order."""
    return [item for item in insights if item.category == category]
