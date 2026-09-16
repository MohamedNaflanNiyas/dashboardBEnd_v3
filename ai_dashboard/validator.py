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


FORBIDDEN_FIELDS = {
    "value",
    "values",
    "data",
    "timestamps",
    "timestamp",
    "lastUpdated",
    "latestValue",
    "x",
    "y",
    "width",
    "height",
    "layout",
    "grid",
    "position",
    "row",
    "column",
}


def normalize(text):

    return (
        (text or "")
        .lower()
        .replace("_", " ")
        .replace("-", " ")
    )


def token_set(text):

    return set(
        normalize(text).split()
    )


def semantic_title_matches(
    component,
    parameter,
):

    title = token_set(
        component.get(
            "title",
            ""
        )
    )

    name = token_set(
        parameter.get(
            "parameter_name",
            ""
        )
    )

    description = token_set(
        parameter.get(
            "parameter_description",
            ""
        )
    )

    reference = (
        name | description
    )

    if not title:
        return True

    overlap = (
        title & reference
    )

    # Don't reject very short titles.
    if len(title) <= 2:
        return True

    return len(overlap) >= 1


def validate_parameter(
    parameter,
    parameter_by_code,
    component_id,
):

    if not isinstance(
        parameter,
        dict
    ):
        return (
            False,
            f"{component_id}: parameter must be object."
        )

    code = parameter.get(
        "global_code"
    )

    if not code:
        return (
            False,
            f"{component_id}: missing global_code."
        )

    if code not in parameter_by_code:
        return (
            False,
            f"{component_id}: unknown global_code {code}."
        )

    return True, ""


def validate_dashboard(
    dashboard,
    parameters,
):

    if not isinstance(
        dashboard,
        dict
    ):
        return False, (
            "Dashboard output must be an object."
        )

    dashboard_data = dashboard.get(
        "dashboard"
    )

    if not isinstance(
        dashboard_data,
        dict
    ):
        return False, (
            "Missing dashboard object."
        )

    parameter_by_code = {
        parameter["global_code"]: parameter
        for parameter in parameters
    }

    components = dashboard_data.get(
        "components",
        []
    )

    if not isinstance(
        components,
        list
    ):
        return False, (
            "dashboard.components must be a list."
        )

    for component in components:

        if not isinstance(
            component,
            dict
        ):
            return False, (
                "Every component must be an object."
            )

        component_id = component.get(
            "id",
            "unknown"
        )

        component_type = component.get(
            "type"
        )

        if component_type not in ALLOWED_TYPES:

            return False, (
                f"{component_id}: "
                f"invalid visualization type "
                f"{component_type}."
            )

        # ---------------------------
        # Forbidden fields
        # ---------------------------

        for field in FORBIDDEN_FIELDS:

            if field in component:

                return False, (
                    f"{component_id}: "
                    f"forbidden field '{field}'."
                )

        # ---------------------------
        # Parameter presence
        # ---------------------------

        has_parameter = (
            "parameter" in component
        )

        has_data_source = (
            "dataSource" in component
        )

        if (
            not has_parameter
            and not has_data_source
        ):

            return False, (
                f"{component_id}: "
                "component must contain "
                "parameter or dataSource."
            )

        # ---------------------------
        # Single parameter
        # ---------------------------

        if has_parameter:

            valid, message = (
                validate_parameter(
                    component["parameter"],
                    parameter_by_code,
                    component_id,
                )
            )

            if not valid:
                return False, message

            code = component[
                "parameter"
            ]["global_code"]

            parameter = (
                parameter_by_code[code]
            )

            if not semantic_title_matches(
                component,
                parameter,
            ):

                return False, (
                    f"{component_id}: "
                    f"title does not appear "
                    f"semantically compatible "
                    f"with parameter {code}."
                )

        # ---------------------------
        # Multi parameter
        # ---------------------------

        if has_data_source:

            data_source = component[
                "dataSource"
            ]

            if not isinstance(
                data_source,
                dict
            ):
                return False, (
                    f"{component_id}: "
                    "dataSource must be object."
                )

            if data_source.get(
                "type"
            ) != "parameters":

                return False, (
                    f"{component_id}: "
                    "dataSource.type must "
                    "be 'parameters'."
                )

            parameter_list = (
                data_source.get(
                    "parameters"
                )
            )

            if not isinstance(
                parameter_list,
                list
            ):
                return False, (
                    f"{component_id}: "
                    "dataSource.parameters "
                    "must be list."
                )

            if len(parameter_list) < 2:

                return False, (
                    f"{component_id}: "
                    "dataSource should contain "
                    "at least two parameters."
                )

            seen_codes = set()

            for parameter_ref in parameter_list:

                valid, message = (
                    validate_parameter(
                        parameter_ref,
                        parameter_by_code,
                        component_id,
                    )
                )

                if not valid:
                    return False, message

                code = parameter_ref[
                    "global_code"
                ]

                if code in seen_codes:

                    return False, (
                        f"{component_id}: "
                        f"duplicate parameter {code}."
                    )

                seen_codes.add(code)

        # A component should not contain both
        # forms in this architecture.
        if (
            has_parameter
            and has_data_source
        ):

            return False, (
                f"{component_id}: "
                "use either parameter or "
                "dataSource, not both."
            )

    return True, "Valid dashboard."












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


# # ============================================================
# # Main dashboard validator
# # ============================================================

# def validate_dashboard(dashboard, parameters):
#     """
#     Validate an AI-generated dashboard definition.

#     The database parameter catalog is authoritative.

#     Validation checks:
#         1. Dashboard structure
#         2. Required dashboard fields
#         3. Component IDs
#         4. Allowed component types
#         5. Required component titles
#         6. Every component has a parameter source
#         7. Single parameter references
#         8. Multiple parameter references
#         9. global_code exists in database
#         10. Resolved parameter ID exists
#         11. global_code ↔ ID relationship is correct
#         12. Runtime data is not generated by AI
#         13. Layout information is not generated by AI
#         14. Optional UOM consistency
#     """

#     # ========================================================
#     # 1. Root validation
#     # ========================================================

#     if not isinstance(dashboard, dict):
#         return False, "Dashboard must be an object."

#     if "dashboard" not in dashboard:
#         return False, "Missing dashboard root."

#     root = dashboard["dashboard"]

#     if not isinstance(root, dict):
#         return False, "dashboard must be an object."

#     # ========================================================
#     # 2. Required dashboard fields
#     # ========================================================

#     required_root_fields = [
#         "title",
#         "subtitle",
#         "components",
#     ]

#     for field in required_root_fields:

#         if field not in root:
#             return False, (
#                 f"Missing dashboard field: {field}"
#             )

#     # ========================================================
#     # 3. Validate root fields
#     # ========================================================

#     if not isinstance(root["title"], str):
#         return False, "dashboard.title must be a string."

#     if not root["title"].strip():
#         return False, "dashboard.title cannot be empty."

#     if not isinstance(root["subtitle"], str):
#         return False, "dashboard.subtitle must be a string."

#     components = root["components"]

#     if not isinstance(components, list):
#         return False, "components must be a list."

#     if len(components) == 0:
#         return False, (
#             "Dashboard must contain at least one component."
#         )

#     # ========================================================
#     # 4. Build authoritative parameter maps
#     # ========================================================
#     #
#     # IMPORTANT:
#     #
#     # parameter_by_id:
#     #     database ID → parameter
#     #
#     # parameter_by_code:
#     #     global_code → parameter
#     #
#     # Never use the ID dictionary to look up a global_code.
#     #
#     # ========================================================

#     parameter_by_id = {
#         parameter["id"]: parameter
#         for parameter in parameters
#     }

#     parameter_by_code = {
#         parameter["global_code"]: parameter
#         for parameter in parameters
#     }

#     valid_parameter_ids = set(
#         parameter_by_id.keys()
#     )

#     valid_parameter_codes = set(
#         parameter_by_code.keys()
#     )

#     # ========================================================
#     # 5. Forbidden fields
#     # ========================================================
#     #
#     # AI generates dashboard structure only.
#     #
#     # Runtime values and physical layout belong to the
#     # backend/frontend and must not be generated by Qwen.
#     #
#     # ========================================================

#     forbidden_runtime_fields = {
#         "data",
#         "values",
#         "timestamps",
#         "lastUpdated",
#         "last_updated",
#         "runtimeData",
#         "runtime_data",
#     }

#     forbidden_layout_fields = {
#         "x",
#         "y",
#         "width",
#         "height",
#         "layout",
#         "position",
#         "grid",
#         "gridPosition",
#         "grid_position",
#     }

#     # ========================================================
#     # 6. Component validation
#     # ========================================================

#     component_ids = set()

#     for component in components:

#         # ----------------------------------------------------
#         # Component must be an object
#         # ----------------------------------------------------

#         if not isinstance(component, dict):
#             return False, (
#                 "Every dashboard component must be an object."
#             )

#         # ----------------------------------------------------
#         # Component ID
#         # ----------------------------------------------------

#         component_id = component.get("id")

#         if not component_id:
#             return False, (
#                 "Every component must have an id."
#             )

#         if component_id in component_ids:
#             return False, (
#                 f"Duplicate component id: "
#                 f"{component_id}"
#             )

#         component_ids.add(component_id)

#         # ----------------------------------------------------
#         # Component type
#         # ----------------------------------------------------

#         component_type = component.get("type")

#         if component_type not in ALLOWED_TYPES:
#             return False, (
#                 f"{component_id} has unsupported "
#                 f"component type '{component_type}'."
#             )

#         # ----------------------------------------------------
#         # Component title
#         # ----------------------------------------------------

#         title = component.get("title")

#         if not title:
#             return False, (
#                 f"{component_id} is missing title."
#             )

#         if not isinstance(title, str):
#             return False, (
#                 f"{component_id} title must be a string."
#             )

#         # ====================================================
#         # 7. Reject runtime fields
#         # ====================================================

#         for field in forbidden_runtime_fields:

#             if field in component:
#                 return False, (
#                     f"{component_id} contains forbidden "
#                     f"runtime field '{field}'. "
#                     f"Runtime values must come from the "
#                     f"database/runtime pipeline, not AI."
#                 )

#         # ====================================================
#         # 8. Reject layout fields
#         # ====================================================

#         for field in forbidden_layout_fields:

#             if field in component:
#                 return False, (
#                     f"{component_id} contains forbidden "
#                     f"layout field '{field}'. "
#                     f"Dashboard layout is controlled by React."
#                 )

#         # ====================================================
#         # 9. Parameter source validation
#         # ====================================================

#         has_parameter = "parameter" in component
#         has_data_source = "dataSource" in component

#         # Every component MUST reference a parameter.
#         if not has_parameter and not has_data_source:
#             return False, (
#                 f"{component_id} must contain either "
#                 f"'parameter' or 'dataSource'. "
#                 f"A dashboard component cannot be created "
#                 f"without a parameter source."
#             )

#         # A component cannot contain both forms.
#         if has_parameter and has_data_source:
#             return False, (
#                 f"{component_id} cannot contain both "
#                 f"'parameter' and 'dataSource'."
#             )

#         # ====================================================
#         # 10. Single parameter validation
#         # ====================================================

#         if has_parameter:

#             parameter = component["parameter"]

#             if not isinstance(parameter, dict):
#                 return False, (
#                     f"{component_id} parameter "
#                     f"must be an object."
#                 )

#             # -----------------------------------------------
#             # global_code
#             # -----------------------------------------------

#             global_code = parameter.get(
#                 "global_code"
#             )

#             if not global_code:
#                 return False, (
#                     f"{component_id} parameter is "
#                     f"missing global_code."
#                 )

#             # -----------------------------------------------
#             # global_code must exist in database
#             # -----------------------------------------------

#             if global_code not in valid_parameter_codes:
#                 return False, (
#                     f"{component_id} uses unknown "
#                     f"global_code '{global_code}'."
#                 )

#             # -----------------------------------------------
#             # Resolved database ID
#             # -----------------------------------------------

#             parameter_id = parameter.get("id")

#             if parameter_id is None:
#                 return False, (
#                     f"{component_id} parameter "
#                     f"'{global_code}' has no resolved ID."
#                 )

#             # ID must exist
#             if parameter_id not in valid_parameter_ids:
#                 return False, (
#                     f"{component_id} parameter "
#                     f"'{global_code}' uses unknown "
#                     f"parameter ID {parameter_id}."
#                 )

#             # -----------------------------------------------
#             # Authoritative parameter
#             # -----------------------------------------------

#             actual = parameter_by_code[
#                 global_code
#             ]

#             actual_id = actual["id"]

#             # -----------------------------------------------
#             # Verify ID ↔ global_code relationship
#             # -----------------------------------------------

#             if parameter_id != actual_id:
#                 return False, (
#                     f"Parameter mismatch: "
#                     f"ID {parameter_id}. "
#                     f"AI provided global_code "
#                     f"'{global_code}', but database "
#                     f"has ID {actual_id}."
#                 )

#             # -----------------------------------------------
#             # Optional UOM validation
#             # -----------------------------------------------

#             component_unit = component.get("unit")
#             actual_unit = actual.get("uom")

#             if (
#                 component_unit
#                 and actual_unit
#                 and component_unit != actual_unit
#             ):
#                 return False, (
#                     f"{component_id} unit mismatch. "
#                     f"Parameter '{global_code}' has unit "
#                     f"'{actual_unit}', but component specifies "
#                     f"'{component_unit}'."
#                 )

#         # ====================================================
#         # 11. dataSource validation
#         # ====================================================

#         if has_data_source:

#             data_source = component[
#                 "dataSource"
#             ]

#             if not isinstance(
#                 data_source,
#                 dict
#             ):
#                 return False, (
#                     f"{component_id} dataSource "
#                     f"must be an object."
#                 )

#             data_source_type = data_source.get(
#                 "type"
#             )

#             # =================================================
#             # Multiple parameter data source
#             # =================================================

#             if data_source_type == "parameters":

#                 parameter_list = data_source.get(
#                     "parameters"
#                 )

#                 if not isinstance(
#                     parameter_list,
#                     list
#                 ):
#                     return False, (
#                         f"{component_id} "
#                         f"dataSource.parameters "
#                         f"must be a list."
#                     )

#                 if len(parameter_list) == 0:
#                     return False, (
#                         f"{component_id} "
#                         f"dataSource.parameters "
#                         f"cannot be empty."
#                     )

#                 # ---------------------------------------------
#                 # Validate every parameter
#                 # ---------------------------------------------

#                 for parameter in parameter_list:

#                     if not isinstance(
#                         parameter,
#                         dict
#                     ):
#                         return False, (
#                             f"{component_id} contains "
#                             f"an invalid parameter."
#                         )

#                     # -----------------------------------------
#                     # global_code
#                     # -----------------------------------------

#                     global_code = parameter.get(
#                         "global_code"
#                     )

#                     if not global_code:
#                         return False, (
#                             f"{component_id} contains "
#                             f"a parameter without "
#                             f"global_code."
#                         )

#                     # -----------------------------------------
#                     # global_code must exist
#                     # -----------------------------------------

#                     if global_code not in valid_parameter_codes:
#                         return False, (
#                             f"{component_id} uses "
#                             f"unknown global_code "
#                             f"'{global_code}'."
#                         )

#                     # -----------------------------------------
#                     # Resolved ID
#                     # -----------------------------------------

#                     parameter_id = parameter.get(
#                         "id"
#                     )

#                     if parameter_id is None:
#                         return False, (
#                             f"{component_id} parameter "
#                             f"'{global_code}' has no "
#                             f"resolved ID."
#                         )

#                     # -----------------------------------------
#                     # ID must exist
#                     # -----------------------------------------

#                     if parameter_id not in valid_parameter_ids:
#                         return False, (
#                             f"{component_id} parameter "
#                             f"'{global_code}' uses unknown "
#                             f"parameter ID {parameter_id}."
#                         )

#                     # -----------------------------------------
#                     # Authoritative parameter
#                     # -----------------------------------------

#                     actual = parameter_by_code[
#                         global_code
#                     ]

#                     actual_id = actual["id"]

#                     # -----------------------------------------
#                     # Verify ID ↔ global_code
#                     # -----------------------------------------

#                     if parameter_id != actual_id:
#                         return False, (
#                             f"Parameter mismatch: "
#                             f"ID {parameter_id}. "
#                             f"AI provided global_code "
#                             f"'{global_code}', but database "
#                             f"has ID {actual_id}."
#                         )

#                 # =================================================
#                 # Optional unit consistency for multi-parameter
#                 # charts
#                 # =================================================
#                 #
#                 # We do not require all parameters to have the
#                 # same UOM here because some chart types may
#                 # legitimately compare related metrics.
#                 #
#                 # The frontend/backend should determine how
#                 # mixed-UOM data is displayed.
#                 #
#                 # =================================================

#             # =================================================
#             # Single parameter dataSource
#             # =================================================

#             elif data_source_type == "parameter":

#                 # ------------------------------------------------
#                 # This format should contain a parameter object.
#                 # ------------------------------------------------

#                 if "parameter" not in component:
#                     return False, (
#                         f"{component_id} dataSource type "
#                         f"'parameter' requires a "
#                         f"'parameter' object."
#                     )

#                 component_parameter = component[
#                     "parameter"
#                 ]

#                 if not isinstance(
#                     component_parameter,
#                     dict
#                 ):
#                     return False, (
#                         f"{component_id} parameter "
#                         f"must be an object."
#                     )

#                 global_code = (
#                     component_parameter.get(
#                         "global_code"
#                     )
#                 )

#                 if not global_code:
#                     return False, (
#                         f"{component_id} dataSource "
#                         f"parameter is missing "
#                         f"global_code."
#                     )

#                 if global_code not in valid_parameter_codes:
#                     return False, (
#                         f"{component_id} uses unknown "
#                         f"global_code '{global_code}'."
#                     )

#                 # ------------------------------------------------
#                 # Resolve/check ID
#                 # ------------------------------------------------

#                 parameter_id = (
#                     component_parameter.get("id")
#                 )

#                 if parameter_id is None:
#                     return False, (
#                         f"{component_id} parameter "
#                         f"'{global_code}' has no "
#                         f"resolved ID."
#                     )

#                 if parameter_id not in valid_parameter_ids:
#                     return False, (
#                         f"{component_id} parameter "
#                         f"'{global_code}' uses unknown "
#                         f"parameter ID {parameter_id}."
#                     )

#                 actual = parameter_by_code[
#                     global_code
#                 ]

#                 actual_id = actual["id"]

#                 if parameter_id != actual_id:
#                     return False, (
#                         f"Parameter mismatch: "
#                         f"ID {parameter_id}. "
#                         f"AI provided global_code "
#                         f"'{global_code}', but database "
#                         f"has ID {actual_id}."
#                     )

#                 # ------------------------------------------------
#                 # Optional parameterId
#                 # ------------------------------------------------

#                 parameter_id_from_source = (
#                     data_source.get("parameterId")
#                 )

#                 if parameter_id_from_source is not None:

#                     if (
#                         parameter_id_from_source
#                         != actual_id
#                     ):
#                         return False, (
#                             f"{component_id} dataSource "
#                             f"parameterId mismatch. "
#                             f"Expected {actual_id}, "
#                             f"got {parameter_id_from_source}."
#                         )

#             # =================================================
#             # Unsupported dataSource type
#             # =================================================

#             else:
#                 return False, (
#                     f"{component_id} has unsupported "
#                     f"dataSource type "
#                     f"'{data_source_type}'. "
#                     f"Expected 'parameter' or "
#                     f"'parameters'."
#                 )

#         # ====================================================
#         # 12. Validate component-specific forbidden fields
#         # ====================================================

#         # AI should not generate chart data structures.
#         chart_data_fields = {
#             "x",
#             "y",
#             "series",
#             "labels",
#             "datasets",
#         }

#         for field in chart_data_fields:

#             if field in component:
#                 return False, (
#                     f"{component_id} contains "
#                     f"forbidden chart data field "
#                     f"'{field}'. "
#                     f"Runtime chart data must come "
#                     f"from the backend."
#                 )

#     # ========================================================
#     # 13. Final validation
#     # ========================================================

#     return True, "Dashboard is valid."