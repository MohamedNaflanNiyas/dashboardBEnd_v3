CONCEPT_ALIASES = {
    "emissions": [
        "emission",
        "emissions",
        "co2",
        "carbon",
        "greenhouse gas",
        "ghg",
        "nox",
        "nitrogen oxide",
        "so2",
        "sulfur dioxide",
        "pm",
        "particulate",
        "pollution",
    ],

    "water": [
        "water",
        "fresh water",
        "water consumption",
        "water abstraction",
        "water reuse",
        "water reused",
        "water discharge",
    ],

    "energy": [
        "energy",
        "electricity",
        "power",
        "fuel",
        "coal",
        "gas",
        "oil",
        "alternative fuel",
        "thermal energy",
    ],

    "production": [
        "production",
        "clinker",
        "cement",
        "output",
        "feed",
    ],

    "compliance": [
        "compliance",
        "limit",
        "exceedance",
        "violation",
        "regulatory",
    ],

    "intensity": [
        "intensity",
        "specific consumption",
        "specific emission",
        "per ton",
        "per tonne",
    ],

    "trend": [
        "trend",
        "history",
        "historical",
        "over time",
        "daily",
        "weekly",
        "monthly",
    ],

    "comparison": [
        "compare",
        "comparison",
        "versus",
        "vs",
        "against",
        "breakdown",
    ],

    "distribution": [
        "distribution",
        "mix",
        "share",
        "percentage",
        "composition",
    ],

    "reuse": [
        "reuse",
        "reused",
        "recycling",
        "recycled",
    ],
}


def detect_concepts(text):
    text = (text or "").lower()

    detected = []

    for concept, terms in CONCEPT_ALIASES.items():

        for term in terms:

            if term in text:

                detected.append(concept)
                break

    return detected