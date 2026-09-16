def choose_visualization(
    intent,
    parameters,
):
    """
    Decide the most appropriate visualization
    based on the user's intent and retrieved
    parameter metadata.
    """

    comparison = intent.get(
        "comparison",
        False
    )

    trend = intent.get(
        "trend",
        False
    )

    distribution = intent.get(
        "distribution",
        False
    )

    intent_type = intent.get(
        "intent",
        "monitor"
    )

    # ---------------------------------------------------------
    # Trend
    # ---------------------------------------------------------

    if trend:

        return {
            "type": "line_chart",
            "reason": (
                "The user requested a trend "
                "or historical view."
            )
        }

    # ---------------------------------------------------------
    # Distribution / composition
    # ---------------------------------------------------------

    if distribution:

        if len(parameters) <= 3:

            return {
                "type": "pie_chart",
                "reason": (
                    "The request describes a "
                    "composition, mix or distribution."
                )
            }

        return {
            "type": "bar_chart",
            "reason": (
                "The request describes a distribution "
                "with several categories."
            )
        }

    # ---------------------------------------------------------
    # Comparison
    # ---------------------------------------------------------

    if comparison:

        return {
            "type": "bar_chart",
            "reason": (
                "The user wants to compare "
                "multiple metrics."
            )
        }

    # ---------------------------------------------------------
    # Compliance
    # ---------------------------------------------------------

    if intent_type == "compliance":

        return {
            "type": "progress",
            "reason": (
                "Compliance rates are naturally "
                "represented as percentages."
            )
        }

    # ---------------------------------------------------------
    # Multiple parameters
    # ---------------------------------------------------------

    if len(parameters) > 1:

        return {
            "type": "bar_chart",
            "reason": (
                "Multiple related parameters were "
                "retrieved."
            )
        }

    # ---------------------------------------------------------
    # Single KPI
    # ---------------------------------------------------------

    return {
        "type": "kpi",
        "reason": (
            "A single monitoring metric is best "
            "represented as a KPI."
        )
    }


def build_visualization_plan(
    intent,
    parameters,
):
    """
    Create a dashboard-level visualization plan.
    """

    visualization = choose_visualization(
        intent,
        parameters
    )

    return {
        "primary_visualization": visualization,
        "available_component_types": [
            "kpi",
            "line_chart",
            "bar_chart",
            "pie_chart",
            "area_chart",
            "gauge",
            "progress",
            "status",
            "table",
        ],
        "rules": {
            "trend": "line_chart",
            "comparison": "bar_chart",
            "distribution": "pie_chart",
            "single_current_value": "kpi",
            "percentage_rate": "progress",
            "min_max_range": "gauge",
            "compliance_status": "status",
            "detailed_records": "table",
        }
    }