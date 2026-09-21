from .intent import extract_intent_from_model
from .retrieval import retrieve_parameters
from .semantic_engine import select_relevant_parameters
from .dashboard_planner import build_dashboard_plan
from .definition import build_final_dashboard
from .validator import validate_dashboard
from .generator import generate_text


def generate_dashboard_from_request(user_request):

    # STEP 1: Understand user request
    intent = extract_intent_from_model(
        user_request,
        generate_text,
    )
    print("Intent: \n")
    print(intent)

    # STEP 2: Build retrieval query
    retrieval_query = " ".join(
        [
            user_request,
            intent.get("domain", ""),
            " ".join(
                intent.get(
                    "concepts",
                    []
                )
            ),
        ]
    )

    
    # STEP 3:Retrieve candidates
    candidates = retrieve_parameters(
        retrieval_query,
        top_k=10,
    )
    print("\ncandidates:\n")
    print(f"\n {candidates}\n")

    
    # STEP 4: Semantic selection
    selected_parameters = (
        select_relevant_parameters(
            intent,
            candidates,
        )
    )
    print("\nselected parameters: Sementic Search \n")
    print(selected_parameters)


    if not selected_parameters:
        raise ValueError(
            "No relevant parameters found "
            "for the requested dashboard."
        )

    # STEP 5: Build dashboard plan
    dashboard_plan = build_dashboard_plan(
        intent,
        selected_parameters,
    )

    print("\n======Dashboard plan: ============\n")
    print(dashboard_plan)

    #STEP 6: Build final JSON
    dashboard = build_final_dashboard(
        dashboard_plan
    )

    print("\n")
    print("=" * 80)
    print("FINAL DASHBOARD BEFORE VALIDATION")
    print("=" * 80)

    import pprint
    pprint.pprint(
        dashboard,
        sort_dicts=False
    )

    print("=" * 80)
    print("\n")

    # STEP 7: Validate
    validate_dashboard(
        dashboard,
        selected_parameters,
    )

    return dashboard








# from core.models import ParameterMetaData


# from .intent import extract_intent

# from .retrieval import (
#     retrieve_parameters,
#     serialize_retrieved_parameters,
# )

# from .semantic_engine import (
#     enrich_parameters,
# )

# from .dashboard_planner import (
#     build_dashboard_plan,
# )

# from .prompt import (
#     build_dashboard_prompt,
# )

# from .generator import (
#     generate_dashboard,
# )

# from .parser import (
#     parse_json_response,
# )

# from .validator import (
#     validate_dashboard,
# )


# def get_parameter_catalog():

#     parameters = (
#         ParameterMetaData.objects
#         .filter(
#             is_active=True
#         )
#         .order_by("id")
#     )

#     return [

#         {
#             "id": parameter.id,

#             "global_code": parameter.global_code,

#             "parameter_name": (
#                 parameter.parameter_name
#             ),

#             "parameter_description": (
#                 parameter.parameter_description
#                 or ""
#             ),

#             "uom": (
#                 parameter.uom
#                 or ""
#             ),

#             "minvalue": parameter.minvalue,

#             "maxvalue": parameter.maxvalue,

#             "domain": (
#                 parameter.domain
#                 or ""
#             ),

#             "category": (
#                 parameter.category
#                 or ""
#             ),

#             "process": (
#                 parameter.process
#                 or ""
#             ),

#             "asset": (
#                 parameter.asset
#                 or ""
#             ),

#             "metric_type": (
#                 parameter.metric_type
#                 or ""
#             ),

#             "keywords": (
#                 parameter.keywords
#                 or []
#             ),
#         }

#         for parameter in parameters
#     ]


# def resolve_parameter_ids(
#     dashboard,
#     parameters,
# ):

#     parameter_by_code = {
#         parameter["global_code"]: parameter
#         for parameter in parameters
#     }

#     components = (
#         dashboard
#         .get("dashboard", {})
#         .get("components", [])
#     )

#     for component in components:

#         component_id = component.get(
#             "id",
#             "unknown"
#         )

#         if "parameter" in component:

#             parameter = component[
#                 "parameter"
#             ]

#             if not isinstance(
#                 parameter,
#                 dict
#             ):
#                 raise ValueError(
#                     f"{component_id}: "
#                     "parameter must be object."
#                 )

#             code = parameter.get(
#                 "global_code"
#             )

#             if code not in parameter_by_code:

#                 raise ValueError(
#                     f"{component_id}: "
#                     f"Unknown global_code: {code}"
#                 )

#             catalog_parameter = (
#                 parameter_by_code[code]
#             )

#             parameter["id"] = (
#                 catalog_parameter["id"]
#             )

#             # Backend owns unit.
#             component["unit"] = (
#                 catalog_parameter.get(
#                     "uom"
#                 )
#                 or ""
#             )

#         if "dataSource" in component:

#             data_source = component[
#                 "dataSource"
#             ]

#             if not isinstance(
#                 data_source,
#                 dict
#             ):
#                 raise ValueError(
#                     f"{component_id}: "
#                     "dataSource must be object."
#                 )

#             if data_source.get(
#                 "type"
#             ) != "parameters":

#                 raise ValueError(
#                     f"{component_id}: "
#                     "Unsupported dataSource type."
#                 )

#             parameter_list = (
#                 data_source.get(
#                     "parameters",
#                     []
#                 )
#             )

#             for parameter in parameter_list:

#                 code = parameter.get(
#                     "global_code"
#                 )

#                 if code not in parameter_by_code:

#                     raise ValueError(
#                         f"{component_id}: "
#                         f"Unknown global_code: {code}"
#                     )

#                 parameter["id"] = (
#                     parameter_by_code[
#                         code
#                     ]["id"]
#                 )

#     return dashboard


# def generate_dashboard_from_request(
#     user_request
# ):

#     # ==================================================
#     # 1. INTENT
#     # ==================================================

#     intent = extract_intent(
#         user_request
#     )

#     print(
#         "\n========== INTENT =========="
#     )

#     print(intent)

#     # ==================================================
#     # 2. RETRIEVAL QUERY
#     # ==================================================

#     retrieval_query = " ".join([

#         user_request,

#         intent.get(
#             "domain",
#             ""
#         ),

#         intent.get(
#             "topic",
#             ""
#         ),

#         " ".join(
#             intent.get(
#                 "concepts",
#                 []
#             )
#         ),
#     ])

#     # ==================================================
#     # 3. RETRIEVE MORE CANDIDATES
#     # ==================================================

#     retrieved = retrieve_parameters(

#         retrieval_query,

#         top_k=24
#     )

#     parameters = (
#         serialize_retrieved_parameters(
#             retrieved
#         )
#     )

#     print(
#         "\n========== RETRIEVED PARAMETERS =========="
#     )

#     for parameter in parameters:

#         print(

#             parameter.get(
#                 "retrieval_score",
#                 0
#             ),

#             parameter[
#                 "global_code"
#             ],

#             parameter[
#                 "parameter_name"
#             ]
#         )

#     # ==================================================
#     # 4. SEMANTIC ENRICHMENT
#     # ==================================================

#     parameters = enrich_parameters(
#         parameters
#     )

#     print(
#         "\n========== SEMANTIC PARAMETERS =========="
#     )

#     for parameter in parameters:

#         print(

#             parameter[
#                 "global_code"
#             ],

#             parameter[
#                 "inferred_domain"
#             ],

#             parameter[
#                 "inferred_scope"
#             ],

#             parameter[
#                 "inferred_metric_type"
#             ],
#         )

#     # ==================================================
#     # 5. GET COMPLETE CATALOG
#     # ==================================================

#     catalog = get_parameter_catalog()

#     catalog = enrich_parameters(
#         catalog
#     )

#     # ==================================================
#     # 6. BUILD DASHBOARD PLAN
#     # ==================================================

#     dashboard_plan = (
#         build_dashboard_plan(
#             intent,
#             parameters,
#         )
#     )

#     print(
#         "\n========== DASHBOARD PLAN =========="
#     )

#     print(
#         dashboard_plan
#     )

#     # ==================================================
#     # 7. QWEN PROMPT
#     # ==================================================

#     prompt = build_dashboard_prompt(

#         user_request=user_request,

#         intent=intent,

#         parameters=parameters,

#         dashboard_plan=dashboard_plan,
#     )

#     # ==================================================
#     # 8. QWEN
#     # ==================================================

#     raw_output = generate_dashboard(
#         prompt
#     )

#     print(
#         "\n========== RAW QWEN OUTPUT =========="
#     )

#     print(raw_output)

#     # ==================================================
#     # 9. PARSE
#     # ==================================================

#     dashboard = parse_json_response(
#         raw_output
#     )

#     # ==================================================
#     # 10. RESOLVE IDS
#     # ==================================================

#     dashboard = resolve_parameter_ids(

#         dashboard,

#         catalog,
#     )

#     # ==================================================
#     # 11. VALIDATE
#     # ==================================================

#     valid, message = (
#         validate_dashboard(
#             dashboard,
#             catalog,
#         )
#     )

#     if not valid:

#         raise ValueError(
#             message
#         )

#     return dashboard







# # from core.models import ParameterMetaData

# # from .intent import extract_intent
# # from .retrieval import (
# #     retrieve_parameters,
# #     serialize_retrieved_parameters,
# # )
# # from .planner import build_visualization_plan
# # from .prompt import build_dashboard_prompt
# # from .generator import generate_dashboard
# # from .parser import parse_json_response
# # from .validator import validate_dashboard


# # def get_parameter_catalog():
# #     """
# #     Return the full parameter catalog.

# #     This is still useful for validation and ID resolution.
# #     It is NOT necessarily passed to Qwen anymore.
# #     """

# #     parameters = (
# #         ParameterMetaData.objects
# #         .filter(is_active=True)
# #         .order_by("id")
# #     )

# #     return [
# #         {
# #             "id": parameter.id,
# #             "global_code": parameter.global_code,
# #             "parameter_name": parameter.parameter_name,
# #             "parameter_description": (
# #                 parameter.parameter_description or ""
# #             ),
# #             "uom": parameter.uom or "",
# #             "minvalue": parameter.minvalue,
# #             "maxvalue": parameter.maxvalue,
# #             "domain": parameter.domain or "",
# #             "category": parameter.category or "",
# #             "process": parameter.process or "",
# #             "asset": parameter.asset or "",
# #             "metric_type": parameter.metric_type or "",
# #             "keywords": parameter.keywords or [],
# #         }
# #         for parameter in parameters
# #     ]


# # def resolve_parameter_ids(
# #     dashboard,
# #     parameters,
# # ):
# #     """
# #     Convert AI-selected global_codes into
# #     authoritative database IDs.
# #     """

# #     parameter_map = {
# #         parameter["global_code"]: parameter["id"]
# #         for parameter in parameters
# #     }

# #     components = (
# #         dashboard
# #         .get("dashboard", {})
# #         .get("components", [])
# #     )

# #     for component in components:

# #         component_id = component.get(
# #             "id",
# #             "unknown"
# #         )

# #         # =====================================================
# #         # Single parameter
# #         # =====================================================

# #         if "parameter" in component:

# #             parameter = component["parameter"]

# #             if not isinstance(
# #                 parameter,
# #                 dict
# #             ):
# #                 raise ValueError(
# #                     f"{component_id} parameter "
# #                     f"must be an object."
# #                 )

# #             global_code = parameter.get(
# #                 "global_code"
# #             )

# #             if not global_code:

# #                 raise ValueError(
# #                     f"{component_id} is missing "
# #                     f"parameter.global_code"
# #                 )

# #             if global_code not in parameter_map:

# #                 raise ValueError(
# #                     f"Unknown global_code: "
# #                     f"{global_code}"
# #                 )

# #             parameter["id"] = (
# #                 parameter_map[global_code]
# #             )

# #         # =====================================================
# #         # Multiple parameters
# #         # =====================================================

# #         if "dataSource" in component:

# #             data_source = component[
# #                 "dataSource"
# #             ]

# #             if not isinstance(
# #                 data_source,
# #                 dict
# #             ):
# #                 raise ValueError(
# #                     f"{component_id} dataSource "
# #                     f"must be an object."
# #                 )

# #             data_source_type = (
# #                 data_source.get("type")
# #             )

# #             if data_source_type == "parameters":

# #                 parameters_list = (
# #                     data_source.get(
# #                         "parameters"
# #                     )
# #                 )

# #                 if not isinstance(
# #                     parameters_list,
# #                     list
# #                 ):
# #                     raise ValueError(
# #                         f"{component_id} "
# #                         f"dataSource.parameters "
# #                         f"must be a list."
# #                     )

# #                 for parameter in parameters_list:

# #                     if not isinstance(
# #                         parameter,
# #                         dict
# #                     ):
# #                         raise ValueError(
# #                             f"{component_id} contains "
# #                             f"an invalid parameter."
# #                         )

# #                     global_code = (
# #                         parameter.get(
# #                             "global_code"
# #                         )
# #                     )

# #                     if not global_code:

# #                         raise ValueError(
# #                             f"{component_id} contains "
# #                             f"a parameter without "
# #                             f"global_code."
# #                         )

# #                     if global_code not in parameter_map:

# #                         raise ValueError(
# #                             f"Unknown global_code: "
# #                             f"{global_code}"
# #                         )

# #                     parameter["id"] = (
# #                         parameter_map[
# #                             global_code
# #                         ]
# #                     )

# #             # =================================================
# #             # Single parameter dataSource
# #             # =================================================

# #             elif (
# #                 data_source_type == "parameter"
# #                 and "parameter" in component
# #             ):

# #                 component_parameter = (
# #                     component["parameter"]
# #                 )

# #                 global_code = (
# #                     component_parameter.get(
# #                         "global_code"
# #                     )
# #                 )

# #                 if global_code not in parameter_map:

# #                     raise ValueError(
# #                         f"Unknown global_code: "
# #                         f"{global_code}"
# #                     )

# #                 data_source[
# #                     "parameterId"
# #                 ] = parameter_map[
# #                     global_code
# #                 ]

# #     return dashboard


# # def generate_dashboard_from_request(
# #     user_request
# # ):

# #     # =========================================================
# #     # STEP 1
# #     # Understand the user's natural language
# #     # =========================================================

# #     intent = extract_intent(
# #         user_request
# #     )

# #     print(
# #         "\n========== INTENT =========="
# #     )
# #     print(intent)

# #     # =========================================================
# #     # STEP 2
# #     # Retrieve relevant parameters
# #     # =========================================================

# #     retrieval_query = " ".join([
# #         user_request,
# #         intent.get("domain", ""),
# #         intent.get("topic", ""),
# #         " ".join(
# #             intent.get("metrics", [])
# #         ),
# #     ])

# #     retrieved = retrieve_parameters(
# #         retrieval_query,
# #         top_k=8
# #     )

# #     parameters = serialize_retrieved_parameters(
# #         retrieved
# #     )

# #     print(
# #         "\n========== RETRIEVED PARAMETERS =========="
# #     )

# #     for parameter in parameters:

# #         print(
# #             parameter["retrieval_score"],
# #             parameter["global_code"],
# #             parameter["parameter_name"]
# #         )

# #     # =========================================================
# #     # STEP 3
# #     # Visualization planning
# #     # =========================================================

# #     visualization_plan = (
# #         build_visualization_plan(
# #             intent,
# #             parameters
# #         )
# #     )

# #     print(
# #         "\n========== VISUALIZATION PLAN =========="
# #     )

# #     print(
# #         visualization_plan
# #     )

# #     # =========================================================
# #     # STEP 4
# #     # Generate final dashboard JSON
# #     # =========================================================

# #     prompt = build_dashboard_prompt(
# #         user_request=user_request,
# #         intent=intent,
# #         parameters=parameters,
# #         visualization_plan=visualization_plan,
# #     )

# #     raw_output = generate_dashboard(
# #         prompt
# #     )

# #     print(
# #         "\n========== RAW QWEN OUTPUT =========="
# #     )

# #     print(raw_output)

# #     # =========================================================
# #     # STEP 5
# #     # Parse JSON
# #     # =========================================================

# #     dashboard = parse_json_response(
# #         raw_output
# #     )

# #     # =========================================================
# #     # STEP 6
# #     # Get authoritative database catalog
# #     # =========================================================

# #     catalog = get_parameter_catalog()

# #     # =========================================================
# #     # STEP 7
# #     # Resolve global_code → DB ID
# #     # =========================================================

# #     dashboard = resolve_parameter_ids(
# #         dashboard,
# #         catalog
# #     )

# #     # =========================================================
# #     # STEP 8
# #     # Deterministic validation
# #     # =========================================================

# #     valid, message = validate_dashboard(
# #         dashboard,
# #         catalog
# #     )

# #     if not valid:

# #         raise ValueError(
# #             message
# #         )

# #     # =========================================================
# #     # STEP 9
# #     # Return final dashboard definition
# #     # =========================================================

# #     return dashboard


# # from .prompt import build_dashboard_prompt
# # from .generator import generate_dashboard
# # from .parser import parse_json_response
# # from .validator import validate_dashboard

# # from core.models import Parameter


# # def get_parameter_catalog():
# #     """
# #     Read active parameters from the database.

# #     This information is provided to Qwen so that
# #     Qwen knows which parameters are available.
# #     """

# #     parameters = (
# #         Parameter.objects
# #         .filter(is_active=True)
# #         .order_by("id")
# #     )

# #     return [
# #         {
# #             "id": p.id,
# #             "global_code": p.global_code,
# #             "parameter_name": p.parameter_name,
# #             "parameter_description": p.parameter_description or "",
# #             "uom": p.uom or "",
# #             "minvalue": p.minvalue,
# #             "maxvalue": p.maxvalue,
# #         }
# #         for p in parameters
# #     ]


# # def resolve_parameter_ids(dashboard, parameters):
# #     """
# #     Resolve AI-generated global_codes into authoritative
# #     database parameter IDs.

# #     Qwen generates only global_code.

# #     Example:

# #         {
# #             "global_code": "L1_FUEL_OIL_MIX"
# #         }

# #     Django resolves:

# #         L1_FUEL_OIL_MIX -> 33
# #     """

# #     # Create global_code -> database ID map
# #     parameter_map = {
# #         parameter["global_code"]: parameter["id"]
# #         for parameter in parameters
# #     }

# #     components = (
# #         dashboard
# #         .get("dashboard", {})
# #         .get("components", [])
# #     )

# #     # Process every dashboard component
# #     for component in components:

# #         component_id = component.get("id", "unknown")

# #         # CASE 1: Single parameter
# #         if "parameter" in component:

# #             parameter = component["parameter"]

# #             if not isinstance(parameter, dict):
# #                 raise ValueError(
# #                     f"{component_id} parameter must be an object."
# #                 )

# #             global_code = parameter.get("global_code")

# #             if not global_code:
# #                 raise ValueError(
# #                     f"{component_id} is missing "
# #                     f"parameter.global_code"
# #                 )

# #             if global_code not in parameter_map:
# #                 raise ValueError(
# #                     f"Unknown global_code: {global_code}"
# #                 )

# #             # Resolve DB ID
# #             parameter["id"] = parameter_map[global_code]

# #         # CASE 2: Multiple parameters
# #         if "dataSource" in component:

# #             data_source = component["dataSource"]

# #             if not isinstance(data_source, dict):
# #                 raise ValueError(
# #                     f"{component_id} dataSource must be an object."
# #                 )

# #             data_source_type = data_source.get("type")

# #             # Multiple parameters
# #             if data_source_type == "parameters":

# #                 parameters_list = data_source.get(
# #                     "parameters"
# #                 )

# #                 if not isinstance(parameters_list, list):
# #                     raise ValueError(
# #                         f"{component_id} dataSource.parameters "
# #                         f"must be a list."
# #                     )

# #                 for parameter in parameters_list:

# #                     if not isinstance(parameter, dict):
# #                         raise ValueError(
# #                             f"{component_id} contains an invalid "
# #                             f"parameter."
# #                         )

# #                     global_code = parameter.get(
# #                         "global_code"
# #                     )

# #                     if not global_code:
# #                         raise ValueError(
# #                             f"{component_id} contains a parameter "
# #                             f"without global_code."
# #                         )

# #                     if global_code not in parameter_map:
# #                         raise ValueError(
# #                             f"Unknown global_code: {global_code}"
# #                         )

# #                     # Resolve DB ID
# #                     parameter["id"] = (
# #                         parameter_map[global_code]
# #                     )
                    
# #             # Single parameter dataSource
# #             elif (
# #                 data_source_type == "parameter"
# #                 and "parameter" in component
# #             ):

# #                 data_source["parameterId"] = (
# #                     component["parameter"]["id"]
# #                 )

# #     return dashboard



# # # def resolve_parameter_ids(dashboard, parameters):
# # #     """
# # #     Convert AI-generated global_code values into
# # #     authoritative database IDs.

# # #     Qwen generates:

# # #         global_code

# # #     Django generates:

# # #         id

# # #     Example:

# # #         L1_FUEL_OIL_MIX
# # #                 ↓
# # #         ID 33
# # #     """

# # #     parameter_map = {
# # #         parameter["global_code"]: parameter["id"]
# # #         for parameter in parameters
# # #     }

# # #     components = (
# # #         dashboard
# # #         .get("dashboard", {})
# # #         .get("components", [])
# # #     )

# # #     # Process every dashboard component
# # #     for component in components:

# # #         # Resolve component parameter
# # #         if "parameter" in component:

# # #             parameter = component["parameter"]

# # #             global_code = parameter.get("global_code")

# # #             if not global_code:
# # #                 raise ValueError(
# # #                     f"{component['id']} is missing "
# # #                     f"parameter.global_code"
# # #                 )

# # #             if global_code not in parameter_map:
# # #                 raise ValueError(
# # #                     f"Unknown global_code: {global_code}"
# # #                 )

# # #             parameter_id = parameter_map[global_code]

# # #             # Backend adds authoritative DB ID
# # #             parameter["id"] = parameter_id

# # #         # Resolve chart dataSource
# # #         if "dataSource" in component:

# # #             data_source = component["dataSource"]

# # #             if (
# # #                 data_source.get("type") == "parameter"
# # #                 and "parameter" in component
# # #             ):

# # #                 data_source["parameterId"] = (
# # #                     component["parameter"]["id"]
# # #                 )

# # #     return dashboard

# # # This function generates a dashboard structure based on the user's request.
# # # It retrieves the parameter catalog from the database, builds a prompt for the AI model,
# # # generates the dashboard, parses the JSON response, resolves global_code values into database IDs,
# # # and validates the resulting dashboard structure. If the validation fails, it raises a ValueError
# # # with an appropriate message.
# # def generate_dashboard_from_request(user_request):

# #     # STEP 1: Get parameter catalog from DB

# #     parameters = get_parameter_catalog()

# #     print("\n========== PARAMETER CATALOG ==========")

# #     for parameter in parameters:
# #         print(
# #             parameter["id"],
# #             "|",
# #             parameter["global_code"],
# #             "|",
# #             parameter["parameter_name"]
# #         )

# #     print("=========================================\n")

# #     # STEP 2: Build AI prompt
# #     prompt = build_dashboard_prompt(
# #         user_request,
# #         parameters
# #     )
# #     # print("\n========== PROMPT ==========")
# #     # print(prompt)
# #     # print("=========================================\n")

# #     # STEP 3: Ask Qwen to generate dashboard
# #     raw_output = generate_dashboard(prompt)

# #     print("\n========== RAW QWEN OUTPUT ==========")
# #     print(raw_output)
# #     print("=====================================\n")

# #     # STEP 4: Convert AI response into Python JSON
# #     dashboard = parse_json_response(raw_output)

# #     print("\n========== PARSED DASHBOARD ==========")
# #     print(dashboard)
# #     print("======================================\n")

# #     # STEP 5: Resolve global_code values into database IDs
# #     dashboard = resolve_parameter_ids(
# #         dashboard,
# #         parameters
# #     )

# #     print("\n========== AFTER ID RESOLUTION ==========")
# #     print(dashboard)
# #     print("=========================================\n")

# #     # STEP 6: Validate dashboard structure
# #     valid, message = validate_dashboard(
# #         dashboard,
# #         parameters
# #     )

# #     if not valid:
# #         raise ValueError(message)

# #     # STEP 7: Return final dashboard
# #     return dashboard








# # # from .prompt import build_dashboard_prompt
# # # from .generator import generate_dashboard
# # # from .parser import parse_json_response
# # # from .validator import validate_dashboard

# # # from core.models import Parameter


# # # # when user request comes in, need to get the parameter catalog from the database, 
# # # # build the prompt, generate the dashboard, parse the JSON response, and validate the dashboard.
# # # def get_parameter_catalog():

# # #     parameters = Parameter.objects.filter(
# # #         is_active=True
# # #     ).order_by("id")

# # #     return [
# # #         {
# # #             "id": p.id,
# # #             "global_code": p.global_code,
# # #             "parameter_name": p.parameter_name,
# # #             "parameter_description": (
# # #                 p.parameter_description or ""
# # #             ),
# # #             "uom": p.uom or "",
# # #             "minvalue": p.minvalue,
# # #             "maxvalue": p.maxvalue,
# # #         }
# # #         for p in parameters
# # #     ]

# # # # This function generates a dashboard structure based on the user's request. 
# # # # It retrieves the parameter catalog from the database, builds a prompt for the AI model, 
# # # # generates the dashboard, parses the JSON response, and validates the resulting dashboard structure. 
# # # # If the validation fails, it raises a ValueError with an appropriate message.
# # # def generate_dashboard_from_request(
# # #     user_request
# # # ):

# # #     parameters = get_parameter_catalog()

# # #     prompt = build_dashboard_prompt(
# # #         user_request,
# # #         parameters
# # #     )

# # #     raw_output = generate_dashboard(
# # #         prompt
# # #     )

# # #     dashboard = parse_json_response(
# # #         raw_output
# # #     )

# # #     valid, message = validate_dashboard(
# # #         dashboard,
# # #         parameters
# # #     )

# # #     if not valid:
# # #         raise ValueError(message)

# # #     return dashboard

# # # import json

# # # def generate_dashboard_from_request(user_request):

# # #     parameters = get_parameter_catalog()

# # #     print("\n========== PARAMETER CATALOG ==========")

# # #     for parameter in parameters:
# # #         print(
# # #             parameter["id"],
# # #             "|",
# # #             parameter["global_code"],
# # #             "|",
# # #             parameter["parameter_name"]
# # #         )

# # #     print("========================================\n")

# # #     prompt = build_dashboard_prompt(
# # #         user_request,
# # #         parameters
# # #     )

# # #     raw_output = generate_dashboard(
# # #         prompt
# # #     )

# # #     print("\n========== RAW QWEN OUTPUT ==========")
# # #     print(raw_output)
# # #     print("=====================================\n")

# # #     dashboard = parse_json_response(
# # #         raw_output
# # #     )

# # #     print("\n========== PARSED DASHBOARD ==========")
# # #     print(json.dumps(dashboard, indent=2))
# # #     print("======================================\n")

# # #     valid, message = validate_dashboard(
# # #         dashboard,
# # #         parameters
# # #     )

# # #     if not valid:
# # #         raise ValueError(message)

# # #     return dashboard