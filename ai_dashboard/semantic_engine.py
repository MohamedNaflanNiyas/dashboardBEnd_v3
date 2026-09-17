from .knowledge.concepts import CONCEPT_ALIASES


def normalize(value):
    if value is None:
        return ""

    return str(value).lower().strip()


def parameter_text(parameter):

    values = [
        parameter.get("parameter_name", ""),
        parameter.get("parameter_description", ""),
        parameter.get("domain", ""),
        parameter.get("category", ""),
        parameter.get("process", ""),
        parameter.get("asset", ""),
        parameter.get("metric_type", ""),
    ]

    values.extend(
        parameter.get("keywords", [])
    )

    return normalize(" ".join(
        str(value)
        for value in values
        if value
    ))


def concept_matches(parameter, concept):

    aliases = CONCEPT_ALIASES.get(
        concept,
        [concept]
    )

    text = parameter_text(parameter)

    for alias in aliases:

        if normalize(alias) in text:
            return True

    return False


def domain_matches(parameter, domain):

    parameter_domain = normalize(
        parameter.get("domain")
    )

    if not parameter_domain:
        return True

    return (
        parameter_domain == normalize(domain)
    )


def score_parameter(parameter, intent):

    score = 0

    domain = intent.get("domain", "")

    if domain_matches(parameter, domain):
        score += 5

    for concept in intent.get("concepts", []):

        if concept_matches(parameter, concept):
            score += 3

    metric_type = normalize(
        parameter.get("metric_type")
    )

    if intent.get("trend") and metric_type:
        score += 1

    return score


def select_relevant_parameters(
    intent,
    candidates,
    minimum_score=3
):

    selected = []

    for parameter in candidates:

        score = score_parameter(
            parameter,
            intent
        )

        if score >= minimum_score:

            item = dict(parameter)

            item["semantic_score"] = score

            selected.append(item)

    selected.sort(
        key=lambda item: item["semantic_score"],
        reverse=True
    )

    return selected


def detect_semantic_group(parameter):

    text = parameter_text(parameter)

    category = normalize(
        parameter.get("category")
    )

    metric_type = normalize(
        parameter.get("metric_type")
    )

    combined = " ".join([
        text,
        category,
        metric_type,
    ])

    if any(
        word in combined
        for word in [
            "nox",
            "nitrogen oxide",
            "so2",
            "sulfur dioxide",
            "pm emission",
            "particulate",
        ]
    ):
        return "air_emissions"

    if "co2" in combined:
        return "co2_emissions"

    if "ghg" in combined:
        return "ghg_emissions"

    if "water" in combined:
        return "water"

    if "energy" in combined:
        return "energy"

    return None