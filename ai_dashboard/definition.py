ALLOWED_VISUALIZATIONS = {
    "kpi",
    "line_chart",
    "bar_chart",
    "pie_chart",
    "area_chart",
    "gauge",
    "progress",
    "status",
    "table",
}


def build_component(
    component_id,
    component_type,
    title,
    parameter=None,
    parameters=None,
):
    """
    Convert one planner component into the
    final dashboard component schema.
    """

    if component_type not in ALLOWED_VISUALIZATIONS:
        raise ValueError(
            f"Invalid visualization type: {component_type}"
        )

    if not title:
        title = component_id

    component = {
        "id": component_id,
        "type": component_type,
        "title": str(title),
    }

    # Single parameter
    if parameter:

        parameter_id = parameter.get("id")
        global_code = parameter.get("global_code")

        if not parameter_id:
            raise ValueError(
                f"Component {component_id} "
                "has a parameter without database id."
            )

        if not global_code:
            raise ValueError(
                f"Component {component_id} "
                "has a parameter without global_code."
            )

        component["parameter"] = {
            "id": parameter_id,
            "global_code": global_code
        }

    
    # Multiple parameters
    if parameters:

        parameter_list = []

        for parameter in parameters:

            parameter_id = parameter.get("id")
            global_code = parameter.get("global_code")

            if not parameter_id:
                raise ValueError(
                    f"Component {component_id} "
                    "contains a parameter without database id."
                )
            if not global_code:
                raise ValueError(
                    f"Component {component_id} "
                    "contains a parameter without "
                    "global_code."
                )

            parameter_list.append(
                {
                    "id": parameter_id,
                    "global_code": global_code
                }
            )

        component["dataSource"] = {
            "type": "parameters",
            "parameters": parameter_list,
        }

    return component


def build_final_dashboard(plan):

    if not isinstance(plan, dict):
        raise ValueError(
            "Dashboard plan must be a dictionary."
        )

    dashboard_plan = plan.get(
        "dashboard"
    )

    if not isinstance(
        dashboard_plan,
        dict
    ):
        raise ValueError(
            "Dashboard plan is missing "
            "'dashboard' object."
        )

    raw_components = dashboard_plan.get(
        "components",
        []
    )

    if not isinstance(
        raw_components,
        list
    ):
        raise ValueError(
            "Dashboard plan components "
            "must be a list."
        )

    final_components = []

    for index, item in enumerate(
        raw_components
    ):

        if not isinstance(
            item,
            dict
        ):
            raise ValueError(
                f"Planner component {index} "
                "must be an object."
            )

        visualization = item.get(
            "visualization"
        )

        if not visualization:
            raise ValueError(
                f"Planner component {index} "
                "has no visualization."
            )

        parameter = item.get(
            "parameter"
        )

        parameters = item.get(
            "parameters"
        )

        # Single parameter
        if isinstance(
            parameter,
            dict
        ):

            title = (
                parameter.get(
                    "parameter_name"
                )
                or parameter.get(
                    "global_code"
                )
                or f"Component {index + 1}"
            )

            component = build_component(
                component_id=f"component_{index + 1}",
                component_type=visualization,
                title=title,
                parameter=parameter,
            )

        # Multiple parameters
        elif isinstance(
            parameters,
            list
        ) and parameters:

            purpose = item.get(
                "purpose"
            )

            if purpose:
                title = str(
                    purpose
                ).replace(
                    "_",
                    " "
                ).title()
            else:
                title = (
                    f"{visualization} "
                    f"comparison"
                )

            component = build_component(
                component_id=f"component_{index + 1}",
                component_type=visualization,
                title=title,
                parameters=parameters,
            )

        else:

            raise ValueError(
                f"Planner component {index} "
                "has neither a valid parameter "
                "nor parameters list."
            )

        final_components.append(
            component
        )

    return {
        "dashboard": {
            "title": dashboard_plan.get(
            "title",
            "General Dashboard"
            ),
            "domain": dashboard_plan.get(
                "domain",
                "general"
            ),
            "scope": dashboard_plan.get(
                "scope",
                "unknown"
            ),
            "intent": dashboard_plan.get(
                "intent",
                "monitor"
            ),
            "components": final_components,
        }
    }





# ALLOWED_VISUALIZATIONS = {
#     "kpi",
#     "line_chart",
#     "bar_chart",
#     "pie_chart",
#     "area_chart",
#     "gauge",
#     "progress",
#     "status",
#     "table",
# }


# def build_component(
#     component_id,
#     component_type,
#     title,
#     parameter=None,
#     parameters=None,
# ):
#     if component_type not in ALLOWED_VISUALIZATIONS:
#         raise ValueError(
#             f"Invalid visualization type: {component_type}"
#         )

#     component = {
#         "id": component_id,
#         "type": component_type,
#         "title": title,
#     }

#     if parameter:
#         component["parameter"] = {
#             "global_code": parameter["global_code"],
#         }

#     if parameters:
#         component["dataSource"] = {
#             "type": "parameters",
#             "parameters": [
#                 {
#                     "global_code": parameter["global_code"],
#                 }
#                 for parameter in parameters
#             ],
#         }

#     return component


# def build_final_dashboard(plan):
#     dashboard_plan = plan.get(
#         "dashboard",
#         {}
#     )

#     final_components = []

#     for index, item in enumerate(
#         dashboard_plan.get(
#             "components",
#             []
#         )
#     ):

#         visualization = item.get(
#             "visualization"
#         )

#         if not visualization:
#             raise ValueError(
#                 f"Planner component {index} "
#                 "has no visualization."
#             )

#         parameter = item.get(
#             "parameter"
#         )

#         parameters = item.get(
#             "parameters"
#         )

#         # ------------------------------------------
#         # Single parameter
#         # ------------------------------------------

#         if parameter:

#             title = parameter.get(
#                 "parameter_name",
#                 parameter.get(
#                     "global_code",
#                     f"Component {index + 1}"
#                 )
#             )

#             component = build_component(
#                 component_id=f"component_{index + 1}",
#                 component_type=visualization,
#                 title=title,
#                 parameter=parameter,
#             )

#         # ------------------------------------------
#         # Multiple parameters
#         # ------------------------------------------

#         elif parameters:

#             purpose = item.get(
#                 "purpose",
#                 "Comparison"
#             )

#             title = purpose.replace(
#                 "_",
#                 " "
#             ).title()

#             component = build_component(
#                 component_id=f"component_{index + 1}",
#                 component_type=visualization,
#                 title=title,
#                 parameters=parameters,
#             )

#         else:

#             raise ValueError(
#                 f"Planner component {index} "
#                 "has no parameter(s)."
#             )

#         final_components.append(
#             component
#         )

#     return {
#         "dashboard": {
#             "domain": dashboard_plan.get(
#                 "domain",
#                 "general"
#             ),
#             "scope": dashboard_plan.get(
#                 "scope",
#                 "unknown"
#             ),
#             "intent": dashboard_plan.get(
#                 "intent",
#                 "monitor"
#             ),
#             "components": final_components,
#         }
#     }


# # this file contains functions that are used to extract information from dashboard definitions. 
# # The functions are used in the dashboard_api app to validate and process dashboard definitions.

# def get_dashboard_parameter_ids(definition):

#     parameter_ids = set()

#     dashboard = definition.get(
#         "dashboard",
#         {}
#     )

#     components = dashboard.get(
#         "components",
#         []
#     )

#     for component in components:

#         parameter = component.get(
#             "parameter"
#         )

#         if parameter:
#             parameter_ids.add(
#                 parameter["id"]
#             )

#         data_source = component.get(
#             "dataSource"
#         )

#         if not data_source:
#             continue

#         if data_source.get("type") == "parameters":

#             for parameter in data_source.get(
#                 "parameters",
#                 []
#             ):
#                 parameter_ids.add(
#                     parameter["id"]
#                 )

#     return list(parameter_ids)