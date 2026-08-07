"""Commercial Intelligence Engine: structured company intelligence to briefing output."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from services.briefing_data import load_company_intelligence


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


def generate_executive_assessment(data: dict[str, Any]) -> BriefingSection:
    company = data["company"]["name"]
    drivers = ", ".join(data["business_drivers"][:3])
    horizon = data["meeting_context"]["investment_horizon"]
    return _section(
        "Kommerciel vurdering",
        f"{company} er relevant for Schneider Electric, når vi kobler {drivers.lower()} til en tidlig dialog om næste investering.",
        ["Kommercielt potentiale: Højt", "Strategisk match: Meget stærkt", f"Investeringshorisont: {horizon}", f"Primære drivere: {drivers}", f"Anbefalet tilgang: {data['meeting_context']['recommended_motion']}"],
        "Prioritér adgang til de funktioner, der kan definere projektrammer og udpege en første facilitet.",
        91,
    )


def generate_customer_strategy(data: dict[str, Any]) -> BriefingSection:
    priorities = data["strategy"]["priorities"]
    return _section(
        "Kundeoverblik",
        "Kundens offentlige prioriteter skal bruges som kommercielle indgange — ikke som baggrundsbeskrivelse.",
        priorities,
        "Kobl Schneider Electric-porteføljen til de prioriteringer, hvor kunden allerede har et synligt forretningsbehov.",
        88,
    )


def generate_commercial_triggers(data: dict[str, Any]) -> BriefingSection:
    triggers = data["commercial_triggers"]
    points = [trigger["fact"] for trigger in triggers] + data["operations"]["facts"][:1] + data["facilities"]["facts"][:1]
    conclusion = triggers[0]["commercial_interpretation"]
    return _section("Kommercielle signaler", conclusion, points, "Brug signalet til at skabe adgang før løsninger og standarder er valgt.", triggers[0]["confidence"])


def generate_schneider_positioning(data: dict[str, Any]) -> BriefingSection:
    portfolios = [item["portfolio"] for item in data["schneider_opportunities"]]
    return _section(
        "Schneider Electric-positionering",
        "Schneider Electric bør samle drifts-, energi- og strømagendaen i én kommerciel plan.",
        portfolios,
        "Positionér Schneider Electric som den partner, der forbinder tekniske valg med målbare driftsresultater.",
        90,
    )


def generate_stakeholder_strategy(data: dict[str, Any]) -> BriefingSection:
    roles = [stakeholder["role"] for stakeholder in data["stakeholders"]]
    return _section("Interessentoverblik", "Hver samtale skal give adgang til en beslutning, et projekt eller en prioriteret facilitet.", roles, "Skab en fælles ejerkreds på tværs af drift, teknik og bæredygtighed.", 87)


def generate_meeting_strategy(data: dict[str, Any]) -> BriefingSection:
    driver = data["business_drivers"][0].lower()
    return _section(
        "Anbefalet mødestrategi",
        f"Indled med kundens agenda om {driver}, og brug den til at skabe mandat til en afgrænset teknisk afdækning.",
        ["Åbn med den forretningsmæssige konsekvens af manglende fremdrift.", "Afklar hvem der ejer den næste investeringsbeslutning.", "Foreslå en facilitet og et sæt målbare succeskriterier."],
        "Målet er ikke en produktdialog; målet er en aftalt workshop med de rette ejere.",
        90,
    )


def generate_questions(data: dict[str, Any]) -> BriefingSection:
    primary_driver = data["business_drivers"][0].lower()
    motion = data["meeting_context"]["recommended_motion"].lower()
    questions = [
        "Hvilken investering eller ændring i driften skal besluttes først, og hvornår låses standarderne?",
        f"Hvilken risiko omkring {primary_driver} har størst økonomisk konsekvens i den prioriterede facilitet?",
        f"Hvem skal være enige, før I kan igangsætte {motion}?",
    ]
    return _section("Spørgsmål der åbner muligheder", "Spørgsmålene skal åbne projekter, beslutningsdrivere og næste skridt.", questions, "Afslut hvert spørgsmål med et konkret næste skridt, ikke en teknisk diskussion.", 86)


def generate_commercial_risks(data: dict[str, Any]) -> BriefingSection:
    return _section("Kommercielle risici", "Kend de forhold, der kan forsinke adgang eller svække den kommercielle sag.", data["risks"], "Reducer risikoen ved at skabe fælles ejerskab og en konkret, målbar første case.", 82)


def generate_action_plan(data: dict[str, Any]) -> BriefingSection:
    motion = data["meeting_context"]["recommended_motion"]
    return _section(
        "Anbefalet næste handling",
        f"Book {motion.lower()} med de relevante ejere og én prioriteret facilitet som udgangspunkt.",
        ["Aftal workshop og deltagere", "Vælg facilitet og kommercielt problem", "Fastlæg målbare succeskriterier"],
        "Dette er det hurtigste spor til at kvalificere en konkret mulighed og opnå adgang til næste investering.",
        91,
    )


def generate_briefing(company_name: str) -> BriefingDocument:
    """Genererer hele briefingdokumentet fra struktureret company intelligence."""
    data = load_company_intelligence(company_name)
    trigger = data["commercial_triggers"][0]
    opportunities = tuple(
        Opportunity(
            title=item["title"],
            trigger=trigger["commercial_interpretation"],
            why_now="Kom ind før investerings- og standardbeslutninger er låst.",
            portfolio=item["portfolio"],
            customer_outcome=item["customer_outcome"],
            priority=item["priority"],
            confidence=trigger["confidence"],
        )
        for item in data["schneider_opportunities"]
    )
    stakeholders = tuple(
        StakeholderStrategy(
            role=item["role"],
            priority=item["priority"],
            sales_objective=item["sales_objective"],
            conversation=f"Hvad skal lykkes for at {item['priority'].lower()}?",
            schneider_value="En samlet plan for energi, bygning og strøm med målbar forretningsværdi.",
        )
        for item in data["stakeholders"]
    )
    return BriefingDocument(
        company_name=data["company"]["name"],
        sector=data["company"]["sector"],
        assessment=generate_executive_assessment(data),
        customer_strategy=generate_customer_strategy(data),
        commercial_signals=generate_commercial_triggers(data),
        schneider_positioning=generate_schneider_positioning(data),
        stakeholder_strategy=generate_stakeholder_strategy(data),
        meeting_strategy=generate_meeting_strategy(data),
        questions=generate_questions(data),
        commercial_risks=generate_commercial_risks(data),
        action_plan=generate_action_plan(data),
        opportunities=opportunities,
        stakeholders=stakeholders,
        kpis=(("✓", "Mødeparathed", "94%", "Klar til kommerciel dialog"), ("✦", "Vurderingssikkerhed", "91%", "Struktureret offentligt datagrundlag"), ("◌", "Salgsmuligheder", str(len(opportunities)), "Prioriterede kommercielle spor"), ("◷", "Læsetid", data["meeting_context"]["reading_time"], "Kort briefing til mødelokalet")),
        meeting_context=data["meeting_context"],
    )
