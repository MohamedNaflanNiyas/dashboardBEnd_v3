def compatible_units(parameters):
    units = {
        (p.get("uom") or "").strip().lower()
        for p in parameters
    }

    units.discard("")

    return len(units) <= 1


def choose_single_metric_visualization(
    parameter,
    intent,
):

    metric_type = parameter.get(
        "inferred_metric_type"
    )

    if intent.get("trend"):
        return "line_chart"

    if metric_type == "rate":
        return "progress"

    if metric_type == "compliance":
        return "progress"

    if metric_type == "intensity":
        return "gauge"

    if metric_type == "concentration":
        return "gauge"

    return "kpi"


def choose_multi_metric_visualization(
    parameters,
    intent,
):

    if intent.get("trend"):

        if compatible_units(parameters):
            return "line_chart"

        return "line_chart"

    if intent.get("distribution"):

        if len(parameters) <= 6:
            return "pie_chart"

        return "bar_chart"

    if intent.get("comparison"):

        return "bar_chart"

    if compatible_units(parameters):

        return "line_chart"

    return "bar_chart"


def can_make_trend(parameters):

    return len(parameters) >= 1


def can_make_comparison(parameters):

    if len(parameters) < 2:
        return False

    metric_types = {
        p.get("inferred_metric_type")
        for p in parameters
    }

    # Don't compare fundamentally different
    # measurements unless explicitly requested.
    if len(metric_types) > 1:
        return False

    return True


def can_make_distribution(parameters):

    if not parameters:
        return False

    return len(parameters) <= 6