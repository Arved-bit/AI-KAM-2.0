"""Typed placeholder briefing data for the MVP demonstration."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Opportunity:
    title: str
    trigger: str
    why_now: str
    portfolio: str
    customer_outcome: str
    priority: str
    confidence: int


def get_briefing(company_name: str) -> dict[str, object]:
    """Returnerer troværdige demodata uden eksterne integrationer."""
    company = company_name or "Kunde"
    return {
        "company": company,
        "headline": "Prioritér en kommerciel dialog om kapacitet, energiværdi og driftsrobusthed.",
        "summary": (
            f"{company} er en attraktiv kunde, når samtalen kobles direkte til udvidelsesplaner, "
            "driftsrisiko og energiforbrug. Schneider Electric bør tage ejerskab på den kommercielle agenda "
            "og skabe en fælles plan for et afgrænset, målbar første skridt."
        ),
        "metrics": [("Branche", "Lægemidler og biotek"), ("Strategisk signal", "Kapacitetsudvidelse"), ("Fokusområde", "Energirobusthed")],
        "developments": [
            ("Udvidelsesagenda", "Brug kapacitetsudvidelse som indgang til en tidlig dialog om standarder, investeringsplan og driftsklarhed."),
            ("Effektivitetspres", "Kobl energiindsigt til ledelsens behov for lavere omkostninger og dokumenterede bæredygtighedsresultater."),
            ("Driftskontinuitet", "Positionér robust strøm og aktivstyring som en forudsætning for at beskytte produktion og leveringssikkerhed."),
        ],
        "opportunities": [
            Opportunity(
                "Gør næste udvidelse til en Schneider Electric-standard",
                "Kommende udvidelser og modernisering skaber et vindue til at påvirke standarder, arkitektur og valg af partner.",
                "Schneider Electric bør engagere sig før projektrammerne er låst, så vores løsning bliver del af investeringsbeslutningen.",
                "EcoStruxure Building Operation med integreret strømstyring.",
                "Hurtigere stabil drift, mindre projektrisiko og en skalerbar platform på tværs af faciliteter.",
                "Høj",
                94,
            ),
            Opportunity(
                "Skab en ledelsesagenda om energi og dekarbonisering",
                "Energiomkostninger og bæredygtighedsmål giver et stærkt grundlag for at tale om målbar forretningsværdi.",
                "Schneider Electric skal skabe en fælles baseline, før kunden vælger isolerede energiinitiativer uden samlet effekt.",
                "EcoStruxure Resource Advisor og Power Monitoring Expert.",
                "Lavere energiomkostninger, bedre ledelsesrapportering og dokumenterede fremskridt mod klimaambitioner.",
                "Høj",
                91,
            ),
            Opportunity(
                "Beskyt produktionen mod kostbare driftsafbrydelser",
                "Øget kompleksitet i kritiske miljøer forstærker risikoen for, at små afvigelser påvirker produktion og kvalitet.",
                "Schneider Electric bør koble strøm- og anlægsrisiko til den forretningsmæssige pris ved nedetid.",
                "EcoStruxure Power og prædiktive vedligeholdelsesservices.",
                "Mere driftskontinuitet, mindre uplanlagt nedetid og beskyttet produktionsoutput.",
                "Mellem",
                86,
            ),
        ],
        "stakeholders": [
            ("Driftsansvarlig", "Sikre oppetid, produktivitet og stabil produktion", "Skabe mandat til en workshop om driftsrisici", "Hvilke hændelser eller flaskehalse påvirker jeres evne til at levere stabilt?", "Tidlig varsling, færre afbrydelser og bedre kontrol over kritiske anlæg."),
            ("Bæredygtighedsansvarlig", "Levere dokumenterbare fremskridt på energi og klima", "Etablere Schneider Electric som partner for en fælles energibaseline", "Hvor mangler I i dag et samlet, troværdigt billede af energiforbrug og fremdrift?", "Pålidelig rapportering og konkrete beslutningsgrundlag for energiindsatser."),
            ("Teknik og driftsorganisation", "Gennemføre projekter uden at forstyrre driften", "Få indblik i kommende projekter og tekniske beslutningskriterier", "Hvilke krav skal være opfyldt, før en ny løsning kan implementeres uden risiko for driften?", "En interoperabel implementeringsvej med lavere risiko og tydeligere ansvar."),
        ],
        "questions": [
            "Hvilke udvidelses- eller moderniseringsprojekter skal godkendes de næste 6–18 måneder, og hvornår vælges de tekniske standarder?",
            "Hvilken driftsrisiko ville få størst økonomisk konsekvens, hvis den ramte en kritisk facilitet i morgen?",
            "Hvilke beslutningskriterier skal en energiinvestering opfylde, før den får ledelsens prioritet?",
            "Hvem skal være enige, før I kan prioritere et pilotprojekt på en udvalgt facilitet?",
        ],
    }
