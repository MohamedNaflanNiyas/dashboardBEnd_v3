# this file contains functions that are used to extract information from dashboard definitions. 
# The functions are used in the dashboard_api app to validate and process dashboard definitions.

def get_dashboard_parameter_ids(definition):

    parameter_ids = set()

    dashboard = definition.get(
        "dashboard",
        {}
    )

    components = dashboard.get(
        "components",
        []
    )

    for component in components:

        parameter = component.get(
            "parameter"
        )

        if parameter:
            parameter_ids.add(
                parameter["id"]
            )

        data_source = component.get(
            "dataSource"
        )

        if not data_source:
            continue

        if data_source.get("type") == "parameters":

            for parameter in data_source.get(
                "parameters",
                []
            ):
                parameter_ids.add(
                    parameter["id"]
                )

    return list(parameter_ids)