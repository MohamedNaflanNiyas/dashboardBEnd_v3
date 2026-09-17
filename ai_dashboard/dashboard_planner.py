from .visualization_rules import (
    choose_single_visualization,
    choose_group_visualization,
)
from .semantic_engine import detect_semantic_group

def create_component(
    purpose,
    visualization,
    parameters,
):
    if not parameters:
        return None

    if len(parameters) == 1:

        parameter = parameters[0]

        return {
            "purpose": purpose,
            "visualization": visualization,
            "parameter": {
                "id": parameter["id"],
                "global_code": parameter["global_code"],
                "parameter_name": parameter.get(
                    "parameter_name",
                    parameter["global_code"],
                ),
            },
        }

    return {
        "purpose": purpose,
        "visualization": visualization,
        "parameters": [
            {
                "id": parameter["id"],
                "global_code": parameter["global_code"],
                "parameter_name": parameter.get(
                    "parameter_name",
                    parameter["global_code"],
                ),
            }
            for parameter in parameters
        ],
    }

def group_parameters(parameters):

    groups = {}

    for parameter in parameters:

        group = detect_semantic_group(
            parameter
        )

        if group is None:
            group = (
                parameter.get("category")
                or parameter.get("metric_type")
                or "general"
            )

        group = str(group).lower().strip()

        groups.setdefault(
            group,
            []
        ).append(parameter)

    return groups


def build_dashboard_plan(
    intent,
    selected_parameters,
):

    groups = group_parameters(
        selected_parameters
    )

    components = []

    # --------------------------------------------------
    # Single meaningful parameters
    # --------------------------------------------------

    for parameter in selected_parameters:

        visualization = choose_single_visualization(
            parameter,
            intent,
        )

        component = create_component(
            purpose="current_value",
            visualization=visualization,
            parameters=[parameter],
        )

        if component:
            components.append(component)

    # --------------------------------------------------
    # Related parameter groups
    # --------------------------------------------------

    for group_name, parameters in groups.items():

        if len(parameters) < 2:
            continue

        visualization = choose_group_visualization(
            parameters,
            "comparison",
            intent,
        )

        component = create_component(
            purpose=f"{group_name}_comparison",
            visualization=visualization,
            parameters=parameters,
        )

        if component:
            components.append(component)

    # --------------------------------------------------
    # Trend
    # --------------------------------------------------

    if intent.get("trend"):

        trend_parameters = [
            parameter
            for parameter in selected_parameters
            if parameter.get("metric_type")
        ]

        if trend_parameters:

            parameter = trend_parameters[0]

            components.append(
                create_component(
                    purpose="trend",
                    visualization="line_chart",
                    parameters=[parameter],
                )
            )

    return {
        "dashboard": {
            "title": intent.get(
            "title",
            "General Dashboard"
            ),
            "domain": intent.get(
                "domain",
                "general",
            ),
            "scope": intent.get(
                "scope",
                "unknown",
            ),
            "intent": intent.get(
                "intent",
                "monitor",
            ),
            "components": components,
        }
    }




    # from .dashboard_patterns import (
#     get_pattern_groups,
# )

# from .visualization_rules import (
#     choose_single_metric_visualization,
#     choose_multi_metric_visualization,
#     can_make_trend,
#     can_make_comparison,
#     can_make_distribution,
# )


# MAX_KPIS = 5
# MAX_TRENDS = 4
# MAX_COMPARISONS = 2
# MAX_DISTRIBUTIONS = 1


# def build_parameter_map(parameters):

#     return {
#         parameter["global_code"]: parameter
#         for parameter in parameters
#     }


# def find_available(
#     codes,
#     parameter_map,
# ):

#     result = []

#     for code in codes:

#         parameter = parameter_map.get(code)

#         if parameter:
#             result.append(parameter)

#     return result


# def deduplicate_parameters(parameters):

#     seen = set()
#     result = []

#     for parameter in parameters:

#         code = parameter.get(
#             "global_code"
#         )

#         if not code:
#             continue

#         if code in seen:
#             continue

#         seen.add(code)
#         result.append(parameter)

#     return result


# def choose_summary_parameters(
#     parameters,
#     intent,
# ):

#     if not parameters:
#         return []

#     domain = intent.get(
#         "domain"
#     )

#     scope = intent.get(
#         "scope"
#     )

#     candidates = []

#     for parameter in parameters:

#         if scope != "any":

#             parameter_scope = parameter.get(
#                 "inferred_scope"
#             )

#             if (
#                 parameter_scope not in
#                 [scope, "unknown"]
#             ):
#                 continue

#         candidates.append(parameter)

#     # Prefer plant-level values when the user
#     # explicitly requested the whole plant.
#     if scope == "plant":

#         plant = [
#             p
#             for p in candidates
#             if p.get("inferred_scope") == "plant"
#         ]

#         if plant:
#             candidates = plant

#     # Prefer meaningful summary metrics.
#     priority = {

#         "emission": 100,
#         "production": 90,
#         "intensity": 85,
#         "rate": 80,
#         "consumption": 75,
#         "energy": 70,
#         "concentration": 65,
#         "numeric": 10,
#     }

#     candidates.sort(
#         key=lambda p: priority.get(
#             p.get("inferred_metric_type"),
#             0
#         ),
#         reverse=True
#     )

#     return candidates[:MAX_KPIS]


# def build_group_components(
#     intent,
#     parameters,
# ):

#     domain = intent.get(
#         "domain"
#     )

#     parameter_map = build_parameter_map(
#         parameters
#     )

#     groups = get_pattern_groups(
#         domain
#     )

#     components = []

#     # -------------------------
#     # WATER
#     # -------------------------

#     if domain == "water":

#         reuse = find_available(
#             groups.get(
#                 "water_reuse",
#                 []
#             ),
#             parameter_map
#         )

#         consumption = find_available(
#             groups.get(
#                 "water_consumption",
#                 []
#             ),
#             parameter_map
#         )

#         balance = find_available(
#             groups.get(
#                 "water_balance",
#                 []
#             ),
#             parameter_map
#         )

#         if reuse:

#             components.append({
#                 "purpose": "water_reuse",
#                 "visualization": "progress",
#                 "parameters": [
#                     p["global_code"]
#                     for p in reuse
#                     if p.get(
#                         "inferred_metric_type"
#                     ) == "rate"
#                 ][:1],
#                 "time_range": "current",
#             })

#         if (
#             len(consumption) >= 1
#             and intent.get(
#                 "trend",
#                 True
#             )
#         ):

#             components.append({
#                 "purpose": "water_consumption_trend",
#                 "visualization": "line_chart",
#                 "parameters": [
#                     p["global_code"]
#                     for p in consumption
#                 ][:2],
#                 "time_range": intent.get(
#                     "time_range",
#                     "7d"
#                 ),
#             })

#         if len(balance) >= 2:

#             components.append({
#                 "purpose": "water_balance_trend",
#                 "visualization": "line_chart",
#                 "parameters": [
#                     p["global_code"]
#                     for p in balance
#                     if p.get("uom")
#                 ][:2],
#                 "time_range": intent.get(
#                     "time_range",
#                     "7d"
#                 ),
#             })

#     # -------------------------
#     # EMISSIONS
#     # -------------------------

#     if domain == "emissions":

#         co2_sources = find_available(
#             groups.get(
#                 "co2_sources",
#                 []
#             ),
#             parameter_map
#         )

#         fuel_mix = find_available(
#             groups.get(
#                 "fuel_mix",
#                 []
#             ),
#             parameter_map
#         )

#         air = find_available(
#             groups.get(
#                 "air_emissions",
#                 []
#             ),
#             parameter_map
#         )

#         compliance = find_available(
#             groups.get(
#                 "air_compliance",
#                 []
#             ),
#             parameter_map
#         )

#         if len(co2_sources) >= 2:

#             components.append({
#                 "purpose": "co2_source_comparison",
#                 "visualization": "bar_chart",
#                 "parameters": [
#                     p["global_code"]
#                     for p in co2_sources
#                 ],
#             })

#         if len(fuel_mix) >= 2:

#             components.append({
#                 "purpose": "fuel_energy_mix",
#                 "visualization": "pie_chart",
#                 "parameters": [
#                     p["global_code"]
#                     for p in fuel_mix
#                 ],
#             })

#         if air:

#             components.append({
#                 "purpose": "air_emissions",
#                 "visualization": "bar_chart",
#                 "parameters": [
#                     p["global_code"]
#                     for p in air
#                 ],
#             })

#         if compliance:

#             components.append({
#                 "purpose": "air_compliance",
#                 "visualization": "progress",
#                 "parameters": [
#                     p["global_code"]
#                     for p in compliance
#                 ],
#             })

#     return components


# def build_generic_components(
#     intent,
#     parameters,
# ):

#     components = []

#     trend_candidates = [
#         p
#         for p in parameters
#         if p.get(
#             "inferred_metric_type"
#         ) not in [
#             "duration",
#         ]
#     ]

#     if (
#         intent.get("trend")
#         and trend_candidates
#     ):

#         selected = trend_candidates[:MAX_TRENDS]

#         components.append({
#             "purpose": "metric_trends",
#             "visualization": choose_multi_metric_visualization(
#                 selected,
#                 intent
#             ),
#             "parameters": [
#                 p["global_code"]
#                 for p in selected
#             ],
#             "time_range": intent.get(
#                 "time_range",
#                 "7d"
#             ),
#         })

#     if (
#         intent.get("comparison")
#         and len(parameters) >= 2
#     ):

#         selected = parameters[:MAX_COMPARISONS]

#         components.append({
#             "purpose": "metric_comparison",
#             "visualization": "bar_chart",
#             "parameters": [
#                 p["global_code"]
#                 for p in selected
#             ],
#         })

#     if (
#         intent.get("distribution")
#         and len(parameters) >= 2
#     ):

#         selected = parameters[:6]

#         components.append({
#             "purpose": "metric_distribution",
#             "visualization": (
#                 "pie_chart"
#                 if len(selected) <= 6
#                 else "bar_chart"
#             ),
#             "parameters": [
#                 p["global_code"]
#                 for p in selected
#             ],
#         })

#     return components


# def build_dashboard_plan(
#     intent,
#     parameters,
# ):

#     parameters = deduplicate_parameters(
#         parameters
#     )

#     plan = {
#         "dashboard": {
#             "domain": intent.get(
#                 "domain",
#                 "general"
#             ),

#             "scope": intent.get(
#                 "scope",
#                 "any"
#             ),

#             "intent": intent.get(
#                 "intent",
#                 "monitor"
#             ),

#             "summary": [],

#             "components": [],
#         }
#     }

#     # --------------------------------
#     # 1. SUMMARY KPIs
#     # --------------------------------

#     summary_parameters = (
#         choose_summary_parameters(
#             parameters,
#             intent
#         )
#     )

#     for parameter in summary_parameters:

#         visualization = (
#             choose_single_metric_visualization(
#                 parameter,
#                 {
#                     **intent,
#                     "trend": False,
#                 }
#             )
#         )

#         plan["dashboard"]["summary"].append({

#             "purpose": "current_value",

#             "visualization": visualization,

#             "parameter": parameter[
#                 "global_code"
#             ],
#         })

#     # --------------------------------
#     # 2. DOMAIN-SPECIFIC COMPONENTS
#     # --------------------------------

#     domain_components = (
#         build_group_components(
#             intent,
#             parameters
#         )
#     )

#     plan["dashboard"]["components"].extend(
#         domain_components
#     )

#     # --------------------------------
#     # 3. GENERIC COMPONENTS
#     # --------------------------------

#     generic_components = (
#         build_generic_components(
#             intent,
#             parameters
#         )
#     )

#     plan["dashboard"]["components"].extend(
#         generic_components
#     )

#     # --------------------------------
#     # 4. CLEAN PLAN
#     # --------------------------------

#     plan = clean_dashboard_plan(
#         plan
#     )

#     return plan


# def clean_dashboard_plan(plan):

#     components = (
#         plan["dashboard"]["components"]
#     )

#     cleaned = []

#     seen = set()

#     for component in components:

#         parameters = component.get(
#             "parameters",
#             []
#         )

#         parameters = list(
#             dict.fromkeys(parameters)
#         )

#         if not parameters:
#             continue

#         component["parameters"] = parameters

#         key = (
#             component.get("purpose"),
#             component.get("visualization"),
#             tuple(parameters),
#         )

#         if key in seen:
#             continue

#         seen.add(key)

#         cleaned.append(component)

#     plan["dashboard"]["components"] = cleaned

#     return plan