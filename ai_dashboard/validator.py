ALLOWED_TYPES = {
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

# This function validates the structure and content of a dashboard configuration
#  against a set of parameters. It checks for required fields, component types, 
# parameter references, and ensures that no runtime data or forbidden fields are present 
# in the components. If any validation fails, it returns False along with an error message; 
# otherwise, it returns True indicating the dashboard is valid.
def validate_dashboard(dashboard, parameters):

    # Root validation
    if not isinstance(dashboard, dict):
        return False, "Dashboard must be an object."

    if "dashboard" not in dashboard:
        return False, "Missing dashboard root."

    root = dashboard["dashboard"]

    if not isinstance(root, dict):
        return False, "dashboard must be an object."

    required_root = [
        "title",
        "subtitle",
        "components"
    ]

    for field in required_root:

        if field not in root:
            return False, (
                f"Missing dashboard field: {field}"
            )

    components = root["components"]

    if not isinstance(components, list):
        return False, "components must be a list."

# Authoritative parameter maps
    parameter_map = {
        parameter["id"]: parameter
        for parameter in parameters
    }

    parameter_codes = {
        parameter["global_code"]
        for parameter in parameters
    }

    valid_parameter_ids = {
        parameter["id"]
        for parameter in parameters
    }

# Component validation

    component_ids = set()

    for component in components:

        # Component ID
        if "id" not in component:
            return False, "Component missing id."

        component_id = component["id"]

        if component_id in component_ids:
            return False, (
                f"Duplicate component id: {component_id}"
            )

        component_ids.add(component_id)

        # Component type
        if "type" not in component:
            return False, (
                f"{component_id} missing type."
            )

        component_type = component["type"]

        if component_type not in ALLOWED_TYPES:
            return False, (
                f"Unsupported type: {component_type}"
            )

        # Component title
        if "title" not in component:
            return False, (
                f"{component_id} missing title."
            )

        # SINGLE PARAMETER
        if "parameter" in component:

            parameter = component["parameter"]

            if not isinstance(parameter, dict):
                return False, (
                    f"{component_id} parameter "
                    f"must be an object."
                )

            if "id" not in parameter:
                return False, (
                    f"{component_id} missing parameter.id"
                )

            if "global_code" not in parameter:
                return False, (
                    f"{component_id} missing "
                    f"parameter.global_code"
                )

            parameter_id = parameter["id"]
            global_code = parameter["global_code"]

            # ID must exist
            if parameter_id not in parameter_map:
                return False, (
                    f"Unknown parameter id: "
                    f"{parameter_id}. "
                    f"Available parameter IDs: "
                    f"{sorted(valid_parameter_ids)}"
                )

            # Global code must exist
            if global_code not in parameter_codes:
                return False, (
                    f"Unknown global_code: "
                    f"{global_code}"
                )

            # ID and global code must match
            actual = parameter_map[parameter_id]

            if actual["global_code"] != global_code:

                return False, (
                    f"Parameter mismatch: "
                    f"ID {parameter_id}. "
                    f"Provided global_code "
                    f"'{global_code}', but database "
                    f"has '{actual['global_code']}'."
                )

        # DATA SOURCE
        if "dataSource" in component:

            data_source = component["dataSource"]

            if not isinstance(data_source, dict):
                return False, (
                    f"{component_id} dataSource "
                    f"must be an object."
                )

            data_source_type = data_source.get(
                "type"
            )

            # MULTIPLE PARAMETERS
            if data_source_type == "parameters":

                parameters_list = data_source.get(
                    "parameters"
                )

                if not isinstance(
                    parameters_list,
                    list
                ):
                    return False, (
                        f"{component_id} dataSource.parameters "
                        f"must be a list."
                    )

                if len(parameters_list) == 0:
                    return False, (
                        f"{component_id} dataSource.parameters "
                        f"cannot be empty."
                    )

                for parameter in parameters_list:

                    if not isinstance(
                        parameter,
                        dict
                    ):
                        return False, (
                            f"{component_id} contains "
                            f"an invalid parameter."
                        )

                    if "id" not in parameter:
                        return False, (
                            f"{component_id} dataSource "
                            f"parameter missing id."
                        )

                    if "global_code" not in parameter:
                        return False, (
                            f"{component_id} dataSource "
                            f"parameter missing "
                            f"global_code."
                        )

                    parameter_id = parameter["id"]
                    global_code = parameter["global_code"]

                    # Validate ID
                    if parameter_id not in parameter_map:

                        return False, (
                            f"Unknown parameter id: "
                            f"{parameter_id}"
                        )

                    # Validate global code
                    if global_code not in parameter_codes:

                        return False, (
                            f"Unknown global_code: "
                            f"{global_code}"
                        )

                    # Validate ID/code relationship

                    actual = parameter_map[
                        parameter_id
                    ]

                    if (
                        actual["global_code"]
                        != global_code
                    ):

                        return False, (
                            f"Parameter mismatch: "
                            f"ID {parameter_id}. "
                            f"Provided global_code "
                            f"'{global_code}', but "
                            f"database has "
                            f"'{actual['global_code']}'."
                        )
                    
            # SINGLE PARAMETER DATA SOURCE
            elif data_source_type == "parameter":

                if "parameter" not in component:
                    return False, (
                        f"{component_id} uses a parameter "
                        f"dataSource but has no parameter."
                    )

                expected_id = (
                    component["parameter"]["id"]
                )

                actual_id = data_source.get(
                    "parameterId"
                )

                if actual_id != expected_id:

                    return False, (
                        f"{component_id} "
                        f"dataSource.parameterId "
                        f"does not match "
                        f"parameter.id."
                    )

        # Runtime data protection
        if "data" in component:

            return False, (
                f"{component_id} contains "
                f"runtime data."
            )

        # Layout protection
        forbidden = {
            "x",
            "y",
            "width",
            "height",
            "layout",
            "position",
        }

        for field in forbidden:

            if field in component:

                return False, (
                    f"{component_id} contains "
                    f"forbidden field: {field}"
                )

    return True, "Dashboard is valid."

# ALLOWED_TYPES = {
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


# def validate_dashboard(
#     dashboard,
#     parameters
# ):

#     if not isinstance(dashboard, dict):
#         return False, "Dashboard must be an object."

#     if "dashboard" not in dashboard:
#         return False, "Missing dashboard root."

#     root = dashboard["dashboard"]

#     if not isinstance(root, dict):
#         return False, "dashboard must be an object."

#     required_root = [
#         "title",
#         "subtitle",
#         "components"
#     ]

#     for field in required_root:
#         if field not in root:
#             return False, (
#                 f"Missing dashboard field: {field}"
#             )

#     components = root["components"]

#     if not isinstance(components, list):
#         return False, "components must be a list."

#     parameter_map = {
#         parameter["id"]: parameter
#         for parameter in parameters
#     }

#     parameter_codes = {
#         parameter["global_code"]
#         for parameter in parameters
#     }

#     valid_parameter_ids = {
#     parameter["id"]
#     for parameter in parameters
#     }

#     component_ids = set()



#     for component in components:

#         if "id" not in component:
#             return False, "Component missing id."

#         if component["id"] in component_ids:
#             return False, (
#                 f"Duplicate component id: "
#                 f"{component['id']}"
#             )

#         component_ids.add(component["id"])

#         if "type" not in component:
#             return False, (
#                 f"{component['id']} missing type."
#             )

#         component_type = component["type"]

#         if component_type not in ALLOWED_TYPES:
#             return False, (
#                 f"Unsupported type: "
#                 f"{component_type}"
#             )

#         if "title" not in component:
#             return False, (
#                 f"{component['id']} missing title."
#             )

#         if "parameter" in component:

#             parameter = component["parameter"]

#             if "id" not in parameter:
#                 return False, (
#                     f"{component['id']} missing "
#                     "parameter.id"
#                 )

#             if "global_code" not in parameter:
#                 return False, (
#                     f"{component['id']} missing "
#                     "parameter.global_code"
#                 )

#             parameter_id = parameter["id"]
#             global_code = parameter["global_code"]

#             if parameter_id not in parameter_map:
#                 return False, (
#                     f"Unknown parameter id: "
#                     f"{parameter_id}"
#                 )

#             if global_code not in parameter_codes:
#                 return False, (
#                     f"Unknown global_code: "
#                     f"{global_code}"
#                 )

#             actual = parameter_map[
#                 parameter_id
#             ]

#             if actual["global_code"] != global_code:
#                 return False, (
#                     f"Parameter mismatch: "
#                     f"{parameter_id}",
#                     f"Available parameter IDs: {sorted(valid_parameter_ids)}"
#                 )

#         if "data" in component:
#             return False, (
#                 f"{component['id']} contains "
#                 "runtime data."
#             )

#         forbidden = {
#             "x",
#             "y",
#             "width",
#             "height",
#             "layout",
#             "position"
#         }

#         for field in forbidden:
#             if field in component:
#                 return False, (
#                     f"{component['id']} contains "
#                     f"forbidden field: {field}"
#                 )

#     return True, "Dashboard is valid."