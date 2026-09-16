DOMAIN_KEYWORDS = {
    "emissions": [
        "emission",
        "emissions",
        "co2",
        "carbon",
        "ghg",
        "nox",
        "so2",
        "pm",
        "air emission",
        "pollution",
    ],

    "water": [
        "water",
        "fresh water",
        "water reuse",
        "water consumption",
        "water abstraction",
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
    ],

    "production": [
        "production",
        "clinker",
        "cement",
        "output",
        "feed",
    ],

    "quality": [
        "quality",
        "blaine",
        "xrf",
        "xrd",
    ],

    "compliance": [
        "compliance",
        "regulatory",
        "limit",
        "exceedance",
    ],
}

def detect_domain(text):
    """
    Detect the most likely domain from natural language.

    This is intentionally deterministic.
    """

    text = (text or "").lower()

    scores = {}

    for domain, terms in DOMAIN_KEYWORDS.items():

        score = 0

        for term in terms:

            if term in text:
                # Exact multi word concepts get more weight.
                if " " in term:
                    score += 3
                else:
                    score += 1

        scores[domain] = score

    best_domain = max(
        scores,
        key=scores.get
    )

    if scores[best_domain] == 0:
        return ""

    return best_domain