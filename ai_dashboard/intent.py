import json
import re

def parse_json_response(response):
    response = response.strip()

    # Remove markdown code fences if the model adds them
    response = re.sub(
        r"^```(?:json)?\s*",
        "",
        response,
        flags=re.IGNORECASE,
    )

    response = re.sub(
        r"\s*```$",
        "",
        response,
    )

    # Convert Python-style booleans/null to JSON
    response = re.sub(
        r"\bTrue\b",
        "true",
        response,
    )

    response = re.sub(
        r"\bFalse\b",
        "false",
        response,
    )

    response = re.sub(
        r"\bNone\b",
        "null",
        response,
    )

    return json.loads(response)


def extract_intent_from_model(user_request, generate_text):
    prompt = f"""
You are an intent understanding engine for an industrial
sustainability dashboard.

Understand the user's request.

Do NOT select database parameters.
Do NOT generate global_codes.
Do NOT generate parameter IDs.

Return JSON only.

Identify:

- domain
- scope
- intent
- concepts
- whether a trend is requested
- whether comparison is requested
- whether distribution is requested
- whether compliance is requested
- whether disclosure is requested
- time range

Allowed domains:
emissions
water
energy
production
quality
compliance
general

Allowed scopes:
plant
line
area
asset
unknown

User request:

{user_request}

Return:

{{
    "title": "Cement Plant Emissions Dashboard",
    "domain": "emissions",
    "scope": "plant",
    "intent": "dashboard",
    "concepts": ["emission", "co2"],
    "trend": False,
    "comparison": False,
    "distribution": False,
    "disclosure": False,
    "compliance": False,
    "time_range": "24h"
}}
"""

    raw = generate_text(prompt)

    print("\n")
    print("=" * 80)
    print("RAW QWEN INTENT RESPONSE")
    print("=" * 80)
    print(raw)
    print("=" * 80)
    print("\n")

    data = parse_json_response(raw)

    return normalize_intent(data)


def normalize_intent(intent):
    return {
        "title": str(intent.get("title","General Dashboard")).strip(),
        "domain": str(intent.get("domain", "general")).lower().strip(),
        "scope": str(intent.get("scope", "unknown")).lower().strip(),
        "intent": str(intent.get("intent", "monitor")).lower().strip(),
        "concepts": [
            str(x).lower().strip()
            for x in intent.get("concepts", [])
            if x
        ],
        "trend": bool(intent.get("trend", False)),
        "comparison": bool(intent.get("comparison", False)),
        "distribution": bool(intent.get("distribution", False)),
        "compliance": bool(intent.get("compliance", False)),
        "disclosure": bool(intent.get("disclosure", False)),
        "time_range": intent.get("time_range", "24h"),
    }



# from .generator import generate_text
# from .parser import parse_json_response


# INTENT_SYSTEM_PROMPT = """
# You are the intent analysis module for SustainOS,
# a cement plant sustainability monitoring platform.

# Your job is NOT to create a dashboard.

# Your job is ONLY to understand the user's request.

# Return ONLY valid JSON.

# The JSON must have exactly this structure:

# {
#     "domain": "",
#     "intent": "",
#     "topic": "",
#     "metrics": [],
#     "comparison": false,
#     "trend": false,
#     "distribution": false,
#     "time_range": "24h"
# }

# Possible domains include:

# - production
# - energy
# - emissions
# - water
# - air_emissions
# - quality
# - sustainability
# - compliance
# - general

# Possible intents include:

# - monitor
# - compare
# - trend
# - distribution
# - compliance
# - summary
# - analyze

# Rules:

# 1. Understand the meaning of the user's words.
# 2. Recognize synonyms.
# 3. "recycled water" means water reuse.
# 4. "carbon" may mean CO2.
# 5. "greenhouse gases" means GHG.
# 6. "nitrogen oxides" means NOx.
# 7. "sulfur dioxide" means SO2.
# 8. "dust" or "particulate matter" means PM.
# 9. "fuel mix" or "energy mix" means a distribution/composition.
# 10. "over time", "trend", "history" means trend=true.
# 11. "compare" means comparison=true.
# 12. "breakdown", "composition", "mix" means distribution=true.
# 13. Never invent parameter codes.
# 14. Do not create dashboard components.
# 15. Do not generate runtime values.
# 16. Use "24h" when the user does not specify a time range.


# ==================================================
# SUSTAINABILITY DISCLOSURE
# ==================================================

# Words such as:

# disclosure
# reporting
# sustainability disclosure
# ESG disclosure
# water disclosure
# emissions disclosure

# usually indicate that the user wants a summary
# of relevant sustainability metrics.

# Do NOT interpret "disclosure" as comparison.

# If the request contains "water" together with
# "consumption", "disclosure", "reuse", "recycling",
# "fresh water", "abstraction", or "discharge":

# domain should be "water".

# Use intent "summary" unless the user explicitly
# requests comparison, trend, analysis, or distribution.

# comparison=true ONLY when the user explicitly
# asks to compare, contrast, versus, vs, difference,
# higher/lower, or comparison.

# Do NOT set comparison=true merely because
# multiple metrics are mentioned.

# Example:

# "Show water consumption and reuse"

# comparison = false

# Example:

# "Compare water consumption and reuse"

# comparison = true

# ==================================================
# MULTIPLE METRICS ≠ COMPARISON
# ==================================================

# Mentioning multiple metrics does NOT automatically
# mean comparison.

# Only use:

# "comparison": true

# when the user explicitly asks for a comparison.

# Examples:

# "Show water consumption and water reuse"

# comparison = false


# "Show water consumption, reuse and discharge"

# comparison = false


# "Compare water consumption and water reuse"

# comparison = true


# "Water consumption versus reuse"

# comparison = true

# Return JSON only.
# """


# def build_intent_prompt(user_request):

#     return f"""
# {INTENT_SYSTEM_PROMPT}

# USER REQUEST:

# {user_request}

# Return only the JSON object.
# """


# def extract_intent(user_request):

#     prompt = build_intent_prompt(
#         user_request
#     )

#     raw_output = generate_text(prompt)

#     intent = parse_json_response(
#         raw_output
#     )

#     return normalize_intent(intent)


# def normalize_intent(intent):

#     if not isinstance(intent, dict):
#         raise ValueError(
#             "Intent must be a JSON object."
#         )

#     return {
#         "domain": (
#             intent.get("domain")
#             or "general"
#         ),

#         "intent": (
#             intent.get("intent")
#             or "monitor"
#         ),

#         "topic": (
#             intent.get("topic")
#             or ""
#         ),

#         "metrics": (
#             intent.get("metrics")
#             if isinstance(
#                 intent.get("metrics"),
#                 list
#             )
#             else []
#         ),

#         "comparison": bool(
#             intent.get("comparison", False)
#         ),

#         "trend": bool(
#             intent.get("trend", False)
#         ),

#         "distribution": bool(
#             intent.get("distribution", False)
#         ),

#         "time_range": (
#             intent.get("time_range")
#             or "24h"
#         ),
#     }