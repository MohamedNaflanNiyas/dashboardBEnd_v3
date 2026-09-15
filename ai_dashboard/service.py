from .prompt import build_dashboard_prompt
from .generator import generate_dashboard
from .parser import parse_json_response
from .validator import validate_dashboard

from core.models import Parameter


def get_parameter_catalog():
    """
    Read active parameters from the database.

    This information is provided to Qwen so that
    Qwen knows which parameters are available.
    """

    parameters = (
        Parameter.objects
        .filter(is_active=True)
        .order_by("id")
    )

    return [
        {
            "id": p.id,
            "global_code": p.global_code,
            "parameter_name": p.parameter_name,
            "parameter_description": p.parameter_description or "",
            "uom": p.uom or "",
            "minvalue": p.minvalue,
            "maxvalue": p.maxvalue,
        }
        for p in parameters
    ]


def resolve_parameter_ids(dashboard, parameters):
    """
    Resolve AI-generated global_codes into authoritative
    database parameter IDs.

    Qwen generates only global_code.

    Example:

        {
            "global_code": "L1_FUEL_OIL_MIX"
        }

    Django resolves:

        L1_FUEL_OIL_MIX -> 33
    """

    # Create global_code -> database ID map
    parameter_map = {
        parameter["global_code"]: parameter["id"]
        for parameter in parameters
    }

    components = (
        dashboard
        .get("dashboard", {})
        .get("components", [])
    )

    # Process every dashboard component
    for component in components:

        component_id = component.get("id", "unknown")

        # CASE 1: Single parameter
        if "parameter" in component:

            parameter = component["parameter"]

            if not isinstance(parameter, dict):
                raise ValueError(
                    f"{component_id} parameter must be an object."
                )

            global_code = parameter.get("global_code")

            if not global_code:
                raise ValueError(
                    f"{component_id} is missing "
                    f"parameter.global_code"
                )

            if global_code not in parameter_map:
                raise ValueError(
                    f"Unknown global_code: {global_code}"
                )

            # Resolve DB ID
            parameter["id"] = parameter_map[global_code]

        # CASE 2: Multiple parameters
        if "dataSource" in component:

            data_source = component["dataSource"]

            if not isinstance(data_source, dict):
                raise ValueError(
                    f"{component_id} dataSource must be an object."
                )

            data_source_type = data_source.get("type")

            # Multiple parameters
            if data_source_type == "parameters":

                parameters_list = data_source.get(
                    "parameters"
                )

                if not isinstance(parameters_list, list):
                    raise ValueError(
                        f"{component_id} dataSource.parameters "
                        f"must be a list."
                    )

                for parameter in parameters_list:

                    if not isinstance(parameter, dict):
                        raise ValueError(
                            f"{component_id} contains an invalid "
                            f"parameter."
                        )

                    global_code = parameter.get(
                        "global_code"
                    )

                    if not global_code:
                        raise ValueError(
                            f"{component_id} contains a parameter "
                            f"without global_code."
                        )

                    if global_code not in parameter_map:
                        raise ValueError(
                            f"Unknown global_code: {global_code}"
                        )

                    # Resolve DB ID
                    parameter["id"] = (
                        parameter_map[global_code]
                    )
                    
            # Single parameter dataSource
            elif (
                data_source_type == "parameter"
                and "parameter" in component
            ):

                data_source["parameterId"] = (
                    component["parameter"]["id"]
                )

    return dashboard



# def resolve_parameter_ids(dashboard, parameters):
#     """
#     Convert AI-generated global_code values into
#     authoritative database IDs.

#     Qwen generates:

#         global_code

#     Django generates:

#         id

#     Example:

#         L1_FUEL_OIL_MIX
#                 ↓
#         ID 33
#     """

#     parameter_map = {
#         parameter["global_code"]: parameter["id"]
#         for parameter in parameters
#     }

#     components = (
#         dashboard
#         .get("dashboard", {})
#         .get("components", [])
#     )

#     # Process every dashboard component
#     for component in components:

#         # Resolve component parameter
#         if "parameter" in component:

#             parameter = component["parameter"]

#             global_code = parameter.get("global_code")

#             if not global_code:
#                 raise ValueError(
#                     f"{component['id']} is missing "
#                     f"parameter.global_code"
#                 )

#             if global_code not in parameter_map:
#                 raise ValueError(
#                     f"Unknown global_code: {global_code}"
#                 )

#             parameter_id = parameter_map[global_code]

#             # Backend adds authoritative DB ID
#             parameter["id"] = parameter_id

#         # Resolve chart dataSource
#         if "dataSource" in component:

#             data_source = component["dataSource"]

#             if (
#                 data_source.get("type") == "parameter"
#                 and "parameter" in component
#             ):

#                 data_source["parameterId"] = (
#                     component["parameter"]["id"]
#                 )

#     return dashboard

# This function generates a dashboard structure based on the user's request.
# It retrieves the parameter catalog from the database, builds a prompt for the AI model,
# generates the dashboard, parses the JSON response, resolves global_code values into database IDs,
# and validates the resulting dashboard structure. If the validation fails, it raises a ValueError
# with an appropriate message.
def generate_dashboard_from_request(user_request):

    # STEP 1: Get parameter catalog from DB

    parameters = get_parameter_catalog()

    print("\n========== PARAMETER CATALOG ==========")

    for parameter in parameters:
        print(
            parameter["id"],
            "|",
            parameter["global_code"],
            "|",
            parameter["parameter_name"]
        )

    print("=========================================\n")

    # STEP 2: Build AI prompt
    prompt = build_dashboard_prompt(
        user_request,
        parameters
    )
    # print("\n========== PROMPT ==========")
    # print(prompt)
    # print("=========================================\n")

    # STEP 3: Ask Qwen to generate dashboard
    raw_output = generate_dashboard(prompt)

    print("\n========== RAW QWEN OUTPUT ==========")
    print(raw_output)
    print("=====================================\n")

    # STEP 4: Convert AI response into Python JSON
    dashboard = parse_json_response(raw_output)

    print("\n========== PARSED DASHBOARD ==========")
    print(dashboard)
    print("======================================\n")

    # STEP 5: Resolve global_code values into database IDs
    dashboard = resolve_parameter_ids(
        dashboard,
        parameters
    )

    print("\n========== AFTER ID RESOLUTION ==========")
    print(dashboard)
    print("=========================================\n")

    # STEP 6: Validate dashboard structure
    valid, message = validate_dashboard(
        dashboard,
        parameters
    )

    if not valid:
        raise ValueError(message)

    # STEP 7: Return final dashboard
    return dashboard








# from .prompt import build_dashboard_prompt
# from .generator import generate_dashboard
# from .parser import parse_json_response
# from .validator import validate_dashboard

# from core.models import Parameter


# # when user request comes in, need to get the parameter catalog from the database, 
# # build the prompt, generate the dashboard, parse the JSON response, and validate the dashboard.
# def get_parameter_catalog():

#     parameters = Parameter.objects.filter(
#         is_active=True
#     ).order_by("id")

#     return [
#         {
#             "id": p.id,
#             "global_code": p.global_code,
#             "parameter_name": p.parameter_name,
#             "parameter_description": (
#                 p.parameter_description or ""
#             ),
#             "uom": p.uom or "",
#             "minvalue": p.minvalue,
#             "maxvalue": p.maxvalue,
#         }
#         for p in parameters
#     ]

# # This function generates a dashboard structure based on the user's request. 
# # It retrieves the parameter catalog from the database, builds a prompt for the AI model, 
# # generates the dashboard, parses the JSON response, and validates the resulting dashboard structure. 
# # If the validation fails, it raises a ValueError with an appropriate message.
# def generate_dashboard_from_request(
#     user_request
# ):

#     parameters = get_parameter_catalog()

#     prompt = build_dashboard_prompt(
#         user_request,
#         parameters
#     )

#     raw_output = generate_dashboard(
#         prompt
#     )

#     dashboard = parse_json_response(
#         raw_output
#     )

#     valid, message = validate_dashboard(
#         dashboard,
#         parameters
#     )

#     if not valid:
#         raise ValueError(message)

#     return dashboard

# import json

# def generate_dashboard_from_request(user_request):

#     parameters = get_parameter_catalog()

#     print("\n========== PARAMETER CATALOG ==========")

#     for parameter in parameters:
#         print(
#             parameter["id"],
#             "|",
#             parameter["global_code"],
#             "|",
#             parameter["parameter_name"]
#         )

#     print("========================================\n")

#     prompt = build_dashboard_prompt(
#         user_request,
#         parameters
#     )

#     raw_output = generate_dashboard(
#         prompt
#     )

#     print("\n========== RAW QWEN OUTPUT ==========")
#     print(raw_output)
#     print("=====================================\n")

#     dashboard = parse_json_response(
#         raw_output
#     )

#     print("\n========== PARSED DASHBOARD ==========")
#     print(json.dumps(dashboard, indent=2))
#     print("======================================\n")

#     valid, message = validate_dashboard(
#         dashboard,
#         parameters
#     )

#     if not valid:
#         raise ValueError(message)

#     return dashboard