import re

from core.models import ParameterMetaData


def normalize_text(value):
    if value is None:
        return ""

    return str(value).lower().strip()


def parameter_search_text(parameter):
    values = [
        parameter.parameter_name,
        parameter.parameter_description,
        parameter.global_code,
        parameter.domain,
        parameter.category,
        parameter.process,
        parameter.asset,
        parameter.metric_type,
    ]

    keywords = parameter.keywords or []

    values.extend(keywords)

    return normalize_text(" ".join(
        str(value)
        for value in values
        if value
    ))


def tokenize(text):
    return set(
        re.findall(
            r"[a-zA-Z0-9_]+",
            normalize_text(text)
        )
    )


def retrieve_parameters(query, top_k):

    parameters = (
        ParameterMetaData.objects
        .filter(is_active=True)
        .order_by("id")
    )

    query_tokens = tokenize(query)

    results = []

    for parameter in parameters:

        search_text = parameter_search_text(parameter)
        parameter_tokens = tokenize(search_text)

        overlap = query_tokens.intersection(parameter_tokens)

        score = len(overlap)

        if score > 0:
            results.append(
                {
                    "score": score,
                    "parameter": serialize_parameter(parameter),
                }
            )

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return [
        item["parameter"]
        for item in results[:top_k]
    ]


def serialize_parameter(parameter):

    return {
        "id": parameter.id,
        "global_code": parameter.global_code,
        "parameter_name": parameter.parameter_name,
        "parameter_description": (
            parameter.parameter_description or ""
        ),
        "uom": parameter.uom or "",
        "minvalue": parameter.minvalue,
        "maxvalue": parameter.maxvalue,
        "domain": parameter.domain or "",
        "category": parameter.category or "",
        "process": parameter.process or "",
        "asset": parameter.asset or "",
        "metric_type": parameter.metric_type or "",
        "keywords": parameter.keywords or [],
    }



# import re

# from core.models import ParameterMetaData

# STOP_WORDS = {
#     "the",
#     "a",
#     "an",
#     "our",
#     "my",
#     "for",
#     "of",
#     "show",
#     "showing",
#     "display",
#     "displaying",
#     "give",
#     "create",
#     "make",
#     "dashboard",
#     "dashboard",
#     "please",
#     "me",
#     "current",
#     "today",
#     "now",
# }


# SYNONYMS = {
#     "recycled": "reuse",
#     "recycling": "reuse",
#     "recycle": "reuse",
#     "reused": "reuse",

#     "carbon": "co2",
#     "carbon dioxide": "co2",

#     "greenhouse": "ghg",
#     "greenhouse gas": "ghg",

#     "electric": "electricity",
#     "power": "electricity",

#     "freshwater": "fresh water",

#     "nitrogen oxide": "nox",
#     "nitrogen oxides": "nox",

#     "sulfur dioxide": "so2",
#     "sulphur dioxide": "so2",

#     "particulate": "pm",
#     "particulates": "pm",
#     "dust": "pm",

#     "thermal": "heat",
#     "thermal energy": "heat",

#     "alternative fuel": "afr",
# }

# DOMAIN_HINTS = {
#     "water": {
#         "water",
#         "reuse",
#         "recycled",
#         "recycling",
#         "freshwater",
#         "fresh water",
#         "abstraction",
#         "withdrawal",
#         "discharge",
#         "wastewater",
#     },

#     "energy": {
#         "energy",
#         "electricity",
#         "power",
#         "fuel",
#         "coal",
#         "gas",
#         "oil",
#         "thermal",
#         "heat",
#     },

#     "emissions": {
#         "emission",
#         "emissions",
#         "co2",
#         "carbon",
#         "ghg",
#         "greenhouse",
#     },

#     "air_emissions": {
#         "nox",
#         "no2",
#         "so2",
#         "pm",
#         "particulate",
#         "dust",
#         "air emission",
#     },

#     "production": {
#         "production",
#         "clinker",
#         "cement",
#         "output",
#         "feed",
#     },

#     "quality": {
#         "quality",
#         "blaine",
#         "fineness",
#     },
# }

# def detect_domains(query):

#     tokens = tokenize(query)

#     detected = set()

#     normalized_query = normalize_text(
#         query
#     )

#     for domain, hints in DOMAIN_HINTS.items():

#         for hint in hints:

#             normalized_hint = normalize_text(
#                 hint
#             )

#             if (
#                 normalized_hint in normalized_query
#                 or normalized_hint in tokens
#             ):
#                 detected.add(domain)

#     return detected

# def normalize_text(text):
#     """
#     Normalize user query or metadata text.
#     """

#     if not text:
#         return ""

#     text = text.lower()

#     for source, target in SYNONYMS.items():
#         text = text.replace(source, target)

#     text = re.sub(
#         r"[^a-z0-9_%.\- ]+",
#         " ",
#         text
#     )

#     text = re.sub(
#         r"\s+",
#         " ",
#         text
#     ).strip()

#     return text


# def tokenize(text):
#     text = normalize_text(text)

#     tokens = text.split()

#     return {
#         token
#         for token in tokens
#         if token not in STOP_WORDS
#         and len(token) > 1
#     }


# def build_parameter_text(parameter):
#     """
#     Combine all semantic information into one searchable text.
#     """

#     keywords = parameter.keywords or []

#     return " ".join([
#         parameter.global_code or "",
#         parameter.parameter_name or "",
#         parameter.parameter_description or "",
#         parameter.domain or "",
#         parameter.category or "",
#         parameter.process or "",
#         parameter.asset or "",
#         parameter.metric_type or "",
#         " ".join(keywords),
#     ])


# def score_parameter(query, parameter):
#     """
#     Calculate a deterministic relevance score.

#     Higher score = stronger semantic/keyword match.
#     """

#     query_normalized = normalize_text(query)
#     query_tokens = tokenize(query)

#     if not query_tokens:
#         return 0

#     parameter_name = normalize_text(
#         parameter.parameter_name or ""
#     )

#     description = normalize_text(
#         parameter.parameter_description or ""
#     )

#     global_code = normalize_text(
#         parameter.global_code or ""
#     )

#     domain = normalize_text(
#         parameter.domain or ""
#     )

#     category = normalize_text(
#         parameter.category or ""
#     )

#     process = normalize_text(
#         parameter.process or ""
#     )

#     asset = normalize_text(
#         parameter.asset or ""
#     )

#     metric_type = normalize_text(
#         parameter.metric_type or ""
#     )

#     keywords = [
#         normalize_text(keyword)
#         for keyword in (parameter.keywords or [])
#     ]

#     score = 0

#     # Detect domain
#     detected_domains = detect_domains(query)

#     if (
#         parameter.domain
#         and parameter.domain in detected_domains
#     ):
#         score += 35
    
#     # Exact parameter name match
#     if parameter_name and parameter_name in query_normalized:
#         score += 100

#     # Exact keyword phrase match
#     for keyword in keywords:

#         if not keyword:
#             continue

#         keyword_tokens = tokenize(keyword)

#         if keyword in query_normalized:
#             score += 50

#         elif (
#             keyword_tokens
#             and keyword_tokens.issubset(query_tokens)
#         ):
#             score += 35

#     # Token matching
#     parameter_tokens = set()

#     for text in [
#         parameter_name,
#         description,
#         global_code,
#         domain,
#         category,
#         process,
#         asset,
#         metric_type,
#     ]:
#         parameter_tokens.update(
#             tokenize(text)
#         )

#     for keyword in keywords:
#         parameter_tokens.update(
#             tokenize(keyword)
#         )

#     matching_tokens = (
#         query_tokens.intersection(parameter_tokens)
#     )

#     score += len(matching_tokens) * 10

#     # Domain match
#     if domain and domain in query_tokens:
#         score += 15

#     # Category match
#     if category and category in query_tokens:
#         score += 15

#     # Process match
#     if process and process in query_tokens:
#         score += 10

#     # Metric type match
#     if metric_type and metric_type in query_tokens:
#         score += 10

#     return score


# def retrieve_parameters(
#     query,
#     top_k=8,
#     minimum_score=5,
# ):
#     """
#     Retrieve the most relevant active parameters.
#     """

#     parameters = list(
#         ParameterMetaData.objects
#         .filter(is_active=True)
#         .order_by("id")
#     )

#     scored = []

#     for parameter in parameters:

#         score = score_parameter(
#             query,
#             parameter
#         )

#         if score >= minimum_score:

#             scored.append(
#                 {
#                     "parameter": parameter,
#                     "score": score,
#                 }
#             )

#     scored.sort(
#         key=lambda item: (
#             -item["score"],
#             item["parameter"].id
#         )
#     )

#     return scored[:top_k]


# def serialize_retrieved_parameters(results):
#     """
#     Convert Django objects into data that can safely
#     be passed to Qwen.
#     """

#     output = []

#     for item in results:

#         parameter = item["parameter"]

#         output.append(
#             {
#                 "id": parameter.id,
#                 "global_code": parameter.global_code,
#                 "parameter_name": parameter.parameter_name,
#                 "parameter_description": (
#                     parameter.parameter_description or ""
#                 ),
#                 "uom": parameter.uom or "",
#                 "minvalue": parameter.minvalue,
#                 "maxvalue": parameter.maxvalue,

#                 "domain": parameter.domain or "",
#                 "category": parameter.category or "",
#                 "process": parameter.process or "",
#                 "asset": parameter.asset or "",
#                 "metric_type": parameter.metric_type or "",
#                 "keywords": parameter.keywords or [],

#                 "retrieval_score": item["score"],
#             }
#         )

#     return output