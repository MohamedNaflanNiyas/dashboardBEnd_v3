def normalize(value):
    if value is None:
        return ""

    return str(value).lower().strip()


def is_percentage(parameter):

    uom = normalize(parameter.get("uom"))

    name = normalize(
        parameter.get("parameter_name")
    )

    return (
        "%"
        in uom
        or "rate"
        in name
        or "percentage"
        in name
        or "percent"
        in name
    )


def is_intensity(parameter):

    metric_type = normalize(
        parameter.get("metric_type")
    )

    name = normalize(
        parameter.get("parameter_name")
    )

    return (
        metric_type == "intensity"
        or "intensity" in name
        or "specific" in name
    )


def is_compliance(parameter):

    name = normalize(
        parameter.get("parameter_name")
    )

    category = normalize(
        parameter.get("category")
    )

    metric_type = normalize(
        parameter.get("metric_type")
    )

    text = " ".join([
        name,
        category,
        metric_type,
    ])

    return (
        "compliance" in text
        or "exceedance" in text
    )


def choose_single_visualization(
    parameter,
    intent
):

    if is_compliance(parameter):
        return "progress"

    if is_percentage(parameter):
        return "progress"

    if is_intensity(parameter):
        return "gauge"

    return "kpi"


def choose_group_visualization(
    parameters,
    group_type,
    intent
):

    if group_type == "trend":
        return "line_chart"

    if group_type == "comparison":
        return "bar_chart"

    if group_type == "distribution":
        return "pie_chart"

    if group_type == "compliance":
        return "progress"

    if len(parameters) > 1:
        return "bar_chart"

    return choose_single_visualization(
        parameters[0],
        intent
    )