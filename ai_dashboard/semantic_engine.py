import re


def normalize(text):
    return re.sub(
        r"[^a-z0-9%]+",
        " ",
        (text or "").lower()
    ).strip()


def infer_scope(parameter):

    code = (
        parameter.get("global_code")
        or ""
    ).upper()

    name = normalize(
        parameter.get("parameter_name", "")
    )

    description = normalize(
        parameter.get("parameter_description", "")
    )

    combined = (
        f"{code} {name} {description}"
    )

    if (
        code.startswith("PLNT_")
        or code.startswith("PLT_")
        or code.startswith("SCP1_")
        or "plant" in combined
    ):
        return "plant"

    if (
        code.startswith("L1_")
        or "line 1" in combined
    ):
        return "line_1"

    if (
        code.startswith("L2_")
        or "line 2" in combined
    ):
        return "line_2"

    return "unknown"


def infer_metric_type(parameter):

    code = normalize(
        parameter.get("global_code", "")
    )

    name = normalize(
        parameter.get("parameter_name", "")
    )

    description = normalize(
        parameter.get("parameter_description", "")
    )

    metric = normalize(
        parameter.get("metric_type", "")
    )

    text = " ".join([
        code,
        name,
        description,
        metric,
    ])

    if any(
        word in text
        for word in [
            "compliance",
            "exceedance",
        ]
    ):
        return "compliance"

    if any(
        word in text
        for word in [
            "rate",
            "ratio",
            "percentage",
            "percent",
            "mix",
            "share",
        ]
    ):
        return "rate"

    if any(
        word in text
        for word in [
            "intensity",
            "specific",
            "per tonne",
            "per ton",
        ]
    ):
        return "intensity"

    if any(
        word in text
        for word in [
            "emission",
            "emissions",
        ]
    ):
        return "emission"

    if any(
        word in text
        for word in [
            "production",
            "output",
        ]
    ):
        return "production"

    if any(
        word in text
        for word in [
            "flow",
            "feed",
            "consumption",
        ]
    ):
        return "consumption"

    if any(
        word in text
        for word in [
            "concentration",
        ]
    ):
        return "concentration"

    if any(
        word in text
        for word in [
            "power",
            "energy",
        ]
    ):
        return "energy"

    if any(
        word in text
        for word in [
            "duration",
        ]
    ):
        return "duration"

    return "numeric"


def infer_domain(parameter):

    explicit = (
        parameter.get("domain")
        or ""
    ).strip().lower()

    if explicit:
        return explicit

    text = " ".join([
        parameter.get("global_code", ""),
        parameter.get("parameter_name", ""),
        parameter.get("parameter_description", ""),
    ])

    text = normalize(text)

    domain_terms = {

        "water": [
            "water",
            "fresh water",
            "reuse",
            "abstraction",
            "discharge",
        ],

        "emissions": [
            "emission",
            "co2",
            "ghg",
            "nox",
            "so2",
            "particulate",
            "pm",
        ],

        "energy": [
            "energy",
            "power",
            "electricity",
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
        ],
    }

    scores = {}

    for domain, terms in domain_terms.items():

        score = sum(
            1
            for term in terms
            if term in text
        )

        scores[domain] = score

    best = max(
        scores,
        key=scores.get
    )

    if scores[best] == 0:
        return "unknown"

    return best


def enrich_parameter(parameter):

    enriched = dict(parameter)

    enriched["inferred_scope"] = infer_scope(
        parameter
    )

    enriched["inferred_metric_type"] = infer_metric_type(
        parameter
    )

    enriched["inferred_domain"] = infer_domain(
        parameter
    )

    return enriched


def enrich_parameters(parameters):

    return [
        enrich_parameter(parameter)
        for parameter in parameters
    ]