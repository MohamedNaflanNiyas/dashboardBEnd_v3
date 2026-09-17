def build_dashboard_prompt(
   user_request,
   intent=None,
   dashboard_plan=None,
):

   return f"""

You are the natural-language understanding engine for SustainOS,
a cement plant sustainability monitoring system.

Your job is ONLY to understand the user's dashboard request.

You must NOT design the dashboard.
You must NOT select database parameters.
You must NOT create dashboard components.
You must NOT create global codes.
You must NOT generate runtime values.
You must NOT generate timestamps.
You must NOT generate layout information.

Analyze the user's request and return ONLY a JSON object.

USER REQUEST:
{user_request}

Return this exact JSON structure:

{{
"title": "string",
"domain": "string",
"scope": "string",
"intent": "string",
"concepts": [],
"trend": false,
"comparison": false,
"distribution": false,
"disclosure": false,
"compliance": false,
"time_range": "24h"
}}

RULES:

1. title
   Generate a short, meaningful dashboard title based on the user's request.

The title should:

* clearly describe the requested subject
* reflect the requested scope when relevant
* normally end with "Dashboard"
* contain no more than 10 words
* not contain global codes
* not contain database IDs
* not contain runtime values

Examples:

User request:
"Give me an emissions dashboard for my entire cement plant"

Title:
"Cement Plant Emissions Dashboard"

User request:
"Show me water consumption and reuse"

Title:
"Water Consumption and Reuse Dashboard"

User request:
"Create a dashboard for line 1 energy performance"

Title:
"Line 1 Energy Performance Dashboard"

2. domain
   Identify the main sustainability domain.

Allowed domains:

emissions
water
energy
production
quality
compliance
general

3. scope
   Identify the requested scope.

Use values such as:

plant
line
kiln
cement_mill
department
asset
unknown

If the user says "entire plant", "whole plant", or "cement plant",
use:

"plant"

4. intent
   Identify what the user wants to do.

Examples:

monitor
dashboard
trend
comparison
distribution
disclosure
compliance

Use the most appropriate single value.

5. concepts
   Return a small list of important concepts explicitly requested
   by the user.

Examples:

Emissions request:
["emission", "co2"]

Water request:
["water", "consumption", "reuse"]

Energy request:
["energy", "fuel"]

Do not add unrelated concepts.

6. trend
   Set true only when the user asks for:

* trend
* history
* historical data
* over time
* daily
* weekly
* monthly
* time series

Otherwise false.

7. comparison
   Set true only when the user asks to:

* compare
* comparison
* versus
* vs
* against

Otherwise false.

8. distribution
   Set true only when the user asks for:

* distribution
* mix
* share
* percentage composition
* breakdown

Otherwise false.

9. disclosure
   Set true only when the user explicitly asks for
   sustainability disclosure, reporting, or disclosure metrics.

Otherwise false.

10. compliance
    Set true only when the user explicitly asks about:

* compliance
* regulatory limits
* violations
* exceedance
* regulatory performance

Otherwise false.

11. time_range
    Identify the requested time period.

Examples:

"today" -> "24h"
"current" -> "24h"
"last 24 hours" -> "24h"
"this week" -> "7d"
"last 7 days" -> "7d"
"this month" -> "30d"
"last month" -> "30d"

If no time period is specified, use:

"24h"

IMPORTANT:

* Return valid JSON only.
* Do not use markdown.
* Do not use ```json.
* Do not include explanations.
* Do not add extra fields.
  """









# def build_dashboard_prompt(
#     user_request,
#     intent,
#     dashboard_plan,
# ):

#     return f"""
# You are a JSON formatting engine for SustainOS.

# The software has already selected the dashboard
# components and parameters.

# Convert the supplied dashboard plan into the
# required final JSON format.

# IMPORTANT RULES:

# 1. Do not add components.
# 2. Do not remove components.
# 3. Do not change parameters.
# 4. Do not invent global codes.
# 5. Use every global_code exactly as supplied.
# 6. Do not generate runtime values.
# 7. Do not generate timestamps.
# 8. Do not generate layout information.
# 9. Return JSON only.
# 10. Do not include markdown.
# 11. Do not include explanations.

# Allowed component types:

# kpi
# line_chart
# bar_chart
# pie_chart
# area_chart
# gauge
# progress
# status
# table

# Every component must contain:

# id
# type
# title

# For one parameter use:

# "parameter": {{
#     "global_code": "EXACT_CODE"
# }}

# For multiple parameters use:

# "dataSource": {{
#     "type": "parameters",
#     "parameters": [
#         {{
#             "global_code": "EXACT_CODE"
#         }}
#     ]
# }}

# FINAL JSON STRUCTURE:

# {{
#     "dashboard": {{
#         "domain": "string",
#         "scope": "string",
#         "intent": "string",
#         "components": []
#     }}
# }}

# DASHBOARD PLAN:

# {dashboard_plan}

# Return ONLY the JSON object.
# """


# import json


# def build_dashboard_prompt(
#     user_request,
#     intent,
#     parameters,
#     dashboard_plan,
# ):

#     compact_parameters = []

#     for parameter in parameters:

#         compact_parameters.append({

#             "global_code": parameter[
#                 "global_code"
#             ],

#             "parameter_name": parameter[
#                 "parameter_name"
#             ],

#             "parameter_description": parameter[
#                 "parameter_description"
#             ],

#             "uom": parameter.get(
#                 "uom",
#                 ""
#             ),

#             "minvalue": parameter.get(
#                 "minvalue"
#             ),

#             "maxvalue": parameter.get(
#                 "maxvalue"
#             ),

#             "inferred_scope": parameter.get(
#                 "inferred_scope"
#             ),

#             "inferred_metric_type": parameter.get(
#                 "inferred_metric_type"
#             ),

#             "inferred_domain": parameter.get(
#                 "inferred_domain"
#             ),
#         })

#     return f"""
# You are the SustainOS Dashboard JSON Generator.

# Your task is to convert a precomputed dashboard plan
# into valid JSON.

# The dashboard plan has already determined:

# - relevant parameters
# - dashboard purpose
# - visualization types
# - parameter relationships

# You MUST follow the dashboard plan.

# You are NOT responsible for discovering new parameters.

# You are NOT responsible for deciding arbitrary visualization types.

# You are a structured JSON formatter.

# ==================================================
# USER REQUEST
# ==================================================

# {user_request}

# ==================================================
# INTENT
# ==================================================

# {json.dumps(intent, indent=2)}

# ==================================================
# AVAILABLE PARAMETERS
# ==================================================

# {json.dumps(compact_parameters, indent=2)}

# ==================================================
# DASHBOARD PLAN
# ==================================================

# {json.dumps(dashboard_plan, indent=2)}

# ==================================================
# OUTPUT RULES
# ==================================================

# Return ONLY valid JSON.

# Do not return markdown.

# Do not return explanations.

# Do not return ```json.

# ==================================================
# PARAMETER RULES
# ==================================================

# Every parameter.global_code MUST be copied exactly
# from AVAILABLE PARAMETERS.

# NEVER invent a global_code.

# NEVER modify a global_code.

# NEVER add prefixes.

# For example:

# PLNT_WTR_FRESH

# must remain exactly:

# PLNT_WTR_FRESH

# Do NOT change it to:

# L1_PLNT_WTR_FRESH

# ==================================================
# ID RULE
# ==================================================

# Do NOT generate parameter IDs.

# The backend will resolve global_code to database ID.

# Therefore every parameter reference should initially contain:

# {{
#     "global_code": "EXACT_CODE_FROM_CATALOG"
# }}

# Do not include:

# "id"

# inside parameter references.

# ==================================================
# UNIT RULE
# ==================================================

# Do not invent units.

# The backend will enrich units from
# the parameter catalog.

# ==================================================
# RUNTIME DATA RULE
# ==================================================

# Never generate:

# value
# values
# timestamp
# timestamps
# data
# lastUpdated
# latestValue

# The backend supplies runtime data.

# ==================================================
# LAYOUT RULE
# ==================================================

# Never generate:

# x
# y
# width
# height
# layout
# grid
# position
# row
# column

# React owns physical dashboard layout.

# ==================================================
# COMPONENT RULE
# ==================================================

# Every component MUST contain either:

# "parameter"

# or:

# "dataSource"

# A component without a parameter reference is INVALID.

# ==================================================
# SINGLE PARAMETER
# ==================================================

# Use:

# "parameter": {{
#     "global_code": "..."
# }}

# ==================================================
# MULTI PARAMETER
# ==================================================

# Use:

# "dataSource": {{
#     "type": "parameters",
#     "parameters": [
#         {{
#             "global_code": "..."
#         }}
#     ]
# }}

# ==================================================
# ALLOWED VISUALIZATIONS
# ==================================================

# kpi
# line_chart
# bar_chart
# pie_chart
# area_chart
# gauge
# progress
# status
# table

# ==================================================
# CHART RULES
# ==================================================

# For line_chart:

# Use:

# "xAxis": {{
#     "field": "timestamp",
#     "label": "Time"
# }}

# and:

# "parameter"

# for one parameter.

# For multiple related parameters use:

# "dataSource": {{
#     "type": "parameters",
#     "parameters": [...]
# }}

# Do not generate actual data.

# ==================================================
# OUTPUT STRUCTURE
# ==================================================

# {{
#     "dashboard": {{
#         "title": "...",
#         "subtitle": "...",
#         "components": []
#     }}
# }}

# The number and types of components MUST follow
# the DASHBOARD PLAN.

# Do not remove planned components unless the required
# parameter is not present in AVAILABLE PARAMETERS.

# Do not create additional parameters.

# Before returning the JSON, verify:

# 1. Every global_code exists in AVAILABLE PARAMETERS.
# 2. Every component has a parameter or dataSource.
# 3. No parameter ID was invented.
# 4. No runtime data was generated.
# 5. No layout fields were generated.
# 6. Visualization types are allowed.
# 7. Multi-parameter components use dataSource.
# 8. Single-parameter components use parameter.
# 9. The output is valid JSON.
# """



# import json


# def build_dashboard_prompt(
#     user_request,
#     intent,
#     parameters,
#     visualization_plan,
# ):

#     parameters_json = json.dumps(
#         parameters,
#         indent=2
#     )

#     intent_json = json.dumps(
#         intent,
#         indent=2
#     )

#     plan_json = json.dumps(
#         visualization_plan,
#         indent=2
#     )

#     return f"""
# You are the dashboard generation module for SustainOS,
# a cement plant sustainability monitoring platform.

# Your ONLY job is to convert the user's request into
# a dashboard definition.

# Do NOT calculate values.

# Do NOT query databases.

# Do NOT create runtime data.

# Do NOT create layout positions.

# Do NOT invent parameter identifiers.

# The backend will resolve global_code to database IDs.

# ==================================================
# USER REQUEST
# ==================================================

# {user_request}


# ==================================================
# UNDERSTOOD INTENT
# ==================================================

# {intent_json}


# ==================================================
# RELEVANT PARAMETERS RETRIEVED BY BACKEND
# ==================================================

# {parameters_json}


# ==================================================
# VISUALIZATION PLAN
# ==================================================

# {plan_json}


# ==================================================
# PARAMETER SELECTION RULES
# ==================================================

# The backend has already retrieved relevant parameters.

# You MUST select parameters ONLY from the
# RELEVANT PARAMETERS RETRIEVED BY BACKEND list.

# You MUST copy global_code EXACTLY.

# Never modify global_code.

# Never add prefixes.

# Never remove prefixes.

# Never invent global_code.

# For example:

# Correct:
# PLNT_WTR_FRESH

# Incorrect:
# L1_PLNT_WTR_FRESH

# Correct:
# PLNT_WTR_REUSE

# Incorrect:
# L1_PLNT_WTR_REUSE

# Correct:
# L1_PROC_WTR_INJ

# Incorrect:
# PROC_WTR_INJ


# ==================================================
# SEMANTIC MATCHING
# ==================================================

# Select the parameter that best matches the user's
# actual meaning.

# Prefer exact semantic matches.

# Do NOT select a related parameter simply because
# it belongs to the same domain.

# Example:

# User:
# "Show water reuse rate"

# Correct:
# PLNT_WTR_REUSE_RATE

# Not:
# PLNT_WTR_REUSE

# Not:
# PLNT_WTR_FRESH

# Not:
# PLNT_WTR_ABS


# ==================================================
# SUPPORTED COMPONENT TYPES
# ==================================================

# Allowed types:

# kpi
# line_chart
# bar_chart
# pie_chart
# area_chart
# gauge
# progress
# status
# table


# ==================================================
# VISUALIZATION RULES
# ==================================================

# Use:

# line_chart
# for trends over time.

# bar_chart
# for comparison between parameters.

# pie_chart
# for composition, mix or distribution.

# kpi
# for a single important current value.

# progress
# for percentage/rate values between 0 and 100.

# gauge
# for a value that should be compared against
# minimum/maximum thresholds.

# status
# for compliance or state.

# table
# for detailed records.


# ==================================================
# SINGLE PARAMETER
# ==================================================

# Use:

# "parameter": {{
#     "global_code": "EXACT_CODE"
# }}


# ==================================================
# MULTIPLE PARAMETERS
# ==================================================

# Use:

# "dataSource": {{
#     "type": "parameters",
#     "parameters": [
#         {{
#             "global_code": "EXACT_CODE_1"
#         }},
#         {{
#             "global_code": "EXACT_CODE_2"
#         }}
#     ]
# }}


# ==================================================
# TIME RANGE
# ==================================================

# Allowed:

# 1h
# 6h
# 12h
# 24h
# 7d
# 30d

# If a time range is needed and not specified,
# use 24h.


# ==================================================
# DO NOT GENERATE
# ==================================================

# Never generate:

# id for parameters
# runtime values
# timestamps
# data
# lastUpdated
# x
# y
# width
# height
# layout
# grid
# position


# ==================================================
# OUTPUT FORMAT
# ==================================================

# Return ONLY valid JSON.

# The root structure MUST be:

# {{
#     "dashboard": {{
#         "title": "Dashboard title",
#         "subtitle": "Dashboard description",
#         "components": []
#     }}
# }}


# Each component MUST contain:

# id
# type
# title

# Parameter-based components should contain
# either:

# parameter

# or:

# dataSource


# ==================================================
# MANDATORY COMPONENT RULE
# ==================================================

# EVERY dashboard component MUST reference at least
# one parameter.

# A component WITHOUT a parameter reference is INVALID.

# You MUST NOT create a component containing only:

# id
# type
# title

# For every component, you MUST include either:

# 1. "parameter"

# OR

# 2. "dataSource"


# ==================================================
# SINGLE PARAMETER COMPONENT
# ==================================================

# For a component representing ONE metric, ALWAYS use:

# "parameter": {{
#     "global_code": "EXACT_CODE_FROM_CATALOG"
# }}


# Example:

# {{
#     "id": "water_reuse",
#     "type": "kpi",
#     "title": "Water Reused",
#     "parameter": {{
#         "global_code": "PLNT_WTR_REUSE"
#     }}
# }}


# ==================================================
# MULTIPLE PARAMETER COMPONENT
# ==================================================

# When a chart compares, combines, or displays multiple
# related parameters, ALWAYS use:

# "dataSource": {{
#     "type": "parameters",
#     "parameters": [
#         {{
#             "global_code": "EXACT_CODE_1"
#         }},
#         {{
#             "global_code": "EXACT_CODE_2"
#         }}
#     ]
# }}


# Example:

# {{
#     "id": "water_consumption",
#     "type": "bar_chart",
#     "title": "Water Consumption",
#     "dataSource": {{
#         "type": "parameters",
#         "parameters": [
#             {{
#                 "global_code": "PLNT_WTR_FRESH"
#             }},
#             {{
#                 "global_code": "PLNT_WTR_REUSE"
#             }}
#         ]
#     }}
# }}


# INVALID:

# {{
#     "id": "water_reuse",
#     "type": "kpi",
#     "title": "Water Reused"
# }}


# INVALID:

# {{
#     "id": "water_reuse",
#     "type": "bar_chart",
#     "title": "Water Reused vs Fresh Water"
# }}


# NEVER generate either of those forms.


# ==================================================
# FINAL SELF-CHECK
# ==================================================

# Before returning JSON, check EVERY component:

# Does it contain "parameter" OR "dataSource"?

# If NO:
# DO NOT RETURN THE COMPONENT.

# Every component must reference a real parameter
# from the retrieved parameter list.

# ==================================================
# FINAL REQUIREMENT
# ==================================================

# Think about the user's intent first.

# Then select the most semantically appropriate
# parameters from the retrieved candidate list.

# Then create the most appropriate dashboard components.

# Return JSON only.
# """


# =====================================================================
# =====================================================================

# def build_dashboard_prompt(user_request, parameters):

#     parameter_lines = []

#     for parameter in parameters:
#         parameter_lines.append(
#             f"""
# ID: {parameter['id']}
# GLOBAL_CODE: {parameter['global_code']}
# NAME: {parameter['parameter_name']}
# DESCRIPTION: {parameter['parameter_description']}
# UNIT: {parameter['uom']}
# """
#         )

#     parameter_catalog = "\n".join(parameter_lines)

#     prompt = f"""
# You are the SustainOS Dashboard Design AI.

# Your task is to convert the user's dashboard request into a
# structured dashboard JSON.

# You are designing dashboards for industrial sustainability
# and cement plant monitoring systems.

# ==================================================
# IMPORTANT RESPONSIBILITY
# ==================================================

# You are ONLY responsible for designing the dashboard structure.

# You MUST NOT generate:

# - runtime values
# - current values
# - historical values
# - timestamps containing actual data
# - calculated values
# - database IDs
# - database queries
# - SQL
# - x/y coordinates
# - width/height
# - layout positions

# The backend will handle:

# - database IDs
# - runtime values
# - historical data
# - calculations
# - data retrieval
# - layout positioning

# ==================================================
# USER REQUEST
# ==================================================

# {user_request}

# ==================================================
# AVAILABLE PARAMETERS
# ==================================================

# These parameters come directly from the SustainOS database.

# You MUST select parameters ONLY from this list.

# DO NOT invent parameters.

# DO NOT create new global codes.

# DO NOT modify global codes.

# DO NOT use parameters that are not present in this list.

# {parameter_catalog}


# ==================================================
# CRITICAL PARAMETER SELECTION RULES
# ==================================================

# When selecting a parameter, you MUST copy the
# global_code EXACTLY from the AVAILABLE PARAMETERS
# catalog.

# NEVER create, modify, infer, abbreviate, normalize,
# or rename a global_code.

# The global_code is an opaque database identifier.

# DO NOT assume that a parameter belonging to Line 1
# must start with "L1_".

# Some valid global_codes start with "L1_".
# Some valid global_codes do NOT start with "L1_".

# Both forms are valid.

# For example:

# Correct:
# PLNT_WTR_FRESH

# Incorrect:
# L1_PLNT_WTR_FRESH

# Correct:
# PLNT_WTR_REUSE

# Incorrect:
# L1_PLNT_WTR_REUSE

# Correct:
# L1_PROC_WTR_INJ

# Incorrect:
# PROC_WTR_INJ

# You MUST use the exact string from the catalog.

# If the catalog contains:

# 41 | PLNT_WTR_FRESH | Fresh Water Consumption

# then the only valid global_code is:

# "PLNT_WTR_FRESH"

# NOT:

# "L1_PLNT_WTR_FRESH"

# If the catalog contains:

# 42 | PLNT_WTR_REUSE | Water Reused

# then the only valid global_code is:

# "PLNT_WTR_REUSE"

# NOT:

# "L1_PLNT_WTR_REUSE"

# Do not generate parameter IDs.
# Do not generate global_codes.
# Only select exact global_codes that already exist
# in AVAILABLE PARAMETERS.
# ==================================================
# ==================================================
# PARAMETER SELECTION RULE
# ==================================================

# When a dashboard component requires a parameter,
# select the parameter using its exact GLOBAL_CODE.

# Example:

# "parameter": {{
#     "global_code": "L1_FUEL_OIL_MIX"
# }}

# IMPORTANT:

# - DO NOT generate parameter IDs.
# - DO NOT guess parameter IDs.
# - DO NOT create parameter IDs.
# - DO NOT modify global codes.
# - DO NOT invent global codes.
# - DO NOT invent parameter names.
# - DO NOT invent units.
# - Select GLOBAL_CODE exactly as provided in AVAILABLE PARAMETERS.
# - The backend will resolve the database ID automatically.

# The GLOBAL_CODE in the examples below is only an example.

# You MUST replace it with the appropriate GLOBAL_CODE
# from AVAILABLE PARAMETERS based on the user's request.

# ==================================================
# DASHBOARD DESIGN RULES
# ==================================================

# Understand the user's request first.

# Then determine:

# 1. What information the user wants to monitor.
# 2. Which parameter or parameters are relevant.
# 3. Which visualization type best represents that information.
# 4. How many components are actually useful.

# Do NOT create unnecessary components.

# For a simple request, one or two components may be enough.

# For a broader management dashboard, multiple complementary
# components may be appropriate.

# Choose visualization types according to the meaning of the data.

# Examples:

# - Single current value → KPI
# - Value changing over time → line_chart
# - Comparison between parameters/categories → bar_chart
# - Composition or percentage distribution → pie_chart
# - Trend over time with emphasis on magnitude → area_chart
# - Value compared with a target/range → gauge
# - Completion/achievement percentage → progress
# - Operational condition/state → status
# - Multiple parameters or detailed records → table

# ===================================================================================================================================================

# DASHBOARD INTENT: PLANT EMISSIONS

# If the user's request is related to:
# - emissions dashboard
# - plant emissions
# - environmental emissions
# - CO2 emissions
# - greenhouse gas emissions
# - carbon emissions
# - cement plant emission performance
# - Scope 1 emissions
# - overall emissions monitoring

# and the user refers to the entire cement plant, create an "Entire Cement Plant Emissions Dashboard".

# Recommended dashboard structure:

# KPI cards:
# - Total Scope 1 CO2
# - CO2 Intensity
# - Total GHG
# - CO2 Reduction
# - AFR Energy Mix

# Charts:
# - CO2 emissions trend
# - Fuel CO2 vs Calcination CO2
# - CO2 intensity trend
# - Fuel energy mix
# - Energy consumption trend

# The dashboard represents the entire cement plant, so plant-level KPIs should be preferred over individual-line KPIs whenever a plant-level KPI exists.

# Do not invent parameters. Only use parameters available in the parameter metadata/database.


# DASHBOARD INTENT: WATER CONSUMPTION AND REUSE

# If the user's request is related to:
# - water consumption
# - water usage
# - water dashboard
# - water disclosure
# - water reuse
# - water recycling
# - water efficiency
# - freshwater consumption
# - water abstraction
# - water discharge
# - plant water management

# create a "Water Consumption & Reuse Dashboard".

# Recommended dashboard structure:

# KPI cards:
# - Fresh Water Consumption
# - Water Reused
# - Water Reuse Rate
# - Water Abstraction
# - Water Discharge
# - Fresh Water Intensity

# Charts:
# - Fresh Water vs Reused Water trend
# - Water Abstraction vs Discharge
# - Water Reuse Rate trend
# - Fresh Water Intensity trend
# - Water Consumption trend

# For a disclosure/reuse request, prioritize PLNT_WTR_FRESH, PLNT_WTR_REUSE,
# PLNT_WTR_REUSE_RATE, PLNT_WTR_ABS and PLNT_WTR_DIS.

# Do not use unrelated emissions or energy KPIs unless explicitly requested.
# Do not invent parameters.


# DASHBOARD INTENT: AIR EMISSIONS

# If the user's request is related to:
# - air emissions
# - air quality
# - stack emissions
# - atmospheric emissions
# - NOx emissions
# - NO2 emissions
# - SO2 emissions
# - particulate emissions
# - PM emissions
# - dust emissions
# - air pollution monitoring

# create an "Air Emissions Dashboard".

# KPI cards:
# - NOx Concentration
# - SO2 Concentration
# - PM Concentration
# - NOx Emission
# - SO2 Emission
# - PM Emission
# - Compliance Rate

# Charts:
# - NOx concentration trend
# - SO2 concentration trend
# - PM concentration trend
# - NOx vs SO2 vs PM trend
# - Air emissions compliance trend

# If the user explicitly mentions NO2, map the request to the available NOx
# parameter unless a specific NO2 parameter exists in the parameter metadata.

# If the user explicitly mentions SO2, use PLNT_SO2_CONC and/or PLNT_SO2_EMI.
# If the user explicitly mentions PM, use PLNT_PM_CONC and/or PLNT_PM_EMI.

# Do not invent NO2 parameters when they do not exist.
# Do not invent parameters.

# ======================================================================================================================================================

# ==================================================
# DASHBOARD STRUCTURE
# ==================================================

# The root JSON MUST be:

# {{
#     "dashboard": {{
#         "title": "...",
#         "subtitle": "...",
#         "components": []
#     }}
# }}

# Every component MUST contain:

# - id
# - type
# - title

# Component IDs MUST be unique.

# ==================================================
# ALLOWED COMPONENT TYPES
# ==================================================

# Only these component types are allowed:

# - kpi
# - line_chart
# - bar_chart
# - pie_chart
# - area_chart
# - gauge
# - progress
# - status
# - table

# ==================================================
# COMPONENT EXAMPLES
# ==================================================

# IMPORTANT:

# The following examples demonstrate the JSON structure and
# how each visualization should be used.

# They are NOT instructions to always use these parameters.

# Always select the appropriate GLOBAL_CODE from the
# AVAILABLE PARAMETERS section.

# --------------------------------------------------
# 1. KPI
# --------------------------------------------------

# Use KPI when the user wants to see a single important
# current/latest metric.

# Example:

# {{
#     "id": "production_kpi",
#     "type": "kpi",
#     "title": "Clinker Production",
#     "parameter": {{
#         "global_code": "L1_KL_CLK_PROD"
#     }},
#     "unit": "t/h"
# }}

# A KPI should represent one primary metric.

# Do not include runtime values.

# --------------------------------------------------
# 2. LINE CHART
# --------------------------------------------------

# Use line_chart when the user wants to see how a parameter
# changes over time.

# Example:

# {{
#     "id": "production_trend",
#     "type": "line_chart",
#     "title": "Clinker Production Trend",
#     "parameter": {{
#         "global_code": "L1_KL_CLK_PROD"
#     }},
#     "timeRange": "7d",
#     "xAxis": {{
#         "field": "timestamp",
#         "label": "Time"
#     }},
#     "yAxis": {{
#         "field": "value",
#         "label": "Clinker Production",
#         "unit": "t/h"
#     }}
# }}

# The backend will provide the actual timestamp and value data.

# --------------------------------------------------
# 3. BAR CHART
# --------------------------------------------------

# Use bar_chart when comparing multiple parameters or
# categories.

# Example:

# {{
#     "id": "fuel_comparison",
#     "type": "bar_chart",
#     "title": "Fuel Energy Mix Comparison",
#     "dataSource": {{
#         "type": "parameters",
#         "parameters": [
#             {{
#                 "global_code": "L1_FUEL_COAL_MIX"
#             }},
#             {{
#                 "global_code": "L1_FUEL_GAS_MIX"
#             }},
#             {{
#                 "global_code": "L1_FUEL_OIL_MIX"
#             }},
#             {{
#                 "global_code": "L1_FUEL_AFR_MIX"
#             }}
#         ]
#     }},
#     "xAxis": {{
#         "field": "parameter",
#         "label": "Fuel Type"
#     }},
#     "yAxis": {{
#         "field": "value",
#         "label": "Energy Mix",
#         "unit": "%"
#     }}
# }}

# Use multiple parameters only when the user's request
# requires comparison.

# --------------------------------------------------
# 4. PIE CHART
# --------------------------------------------------

# Use pie_chart when showing composition, distribution,
# or percentage contribution.

# Example:

# {{
#     "id": "fuel_mix_distribution",
#     "type": "pie_chart",
#     "title": "Fuel Energy Mix Distribution",
#     "dataSource": {{
#         "type": "parameters",
#         "parameters": [
#             {{
#                 "global_code": "L1_FUEL_COAL_MIX"
#             }},
#             {{
#                 "global_code": "L1_FUEL_GAS_MIX"
#             }},
#             {{
#                 "global_code": "L1_FUEL_OIL_MIX"
#             }},
#             {{
#                 "global_code": "L1_FUEL_AFR_MIX"
#             }}
#         ]
#     }},
#     "valueField": "value",
#     "nameField": "parameter",
#     "unit": "%"
# }}

# Pie charts are most appropriate when the parameters
# represent parts of a common whole.

# --------------------------------------------------
# 5. AREA CHART
# --------------------------------------------------

# Use area_chart when showing a time-based trend where
# the magnitude or accumulated visual area is useful.

# Example:

# {{
#     "id": "power_consumption_trend",
#     "type": "area_chart",
#     "title": "Plant Power Trend",
#     "parameter": {{
#         "global_code": "L1_PLANT_PWR"
#     }},
#     "timeRange": "24h",
#     "xAxis": {{
#         "field": "timestamp",
#         "label": "Time"
#     }},
#     "yAxis": {{
#         "field": "value",
#         "label": "Plant Power",
#         "unit": "MW"
#     }}
# }}

# The backend will provide the actual data.

# --------------------------------------------------
# 6. GAUGE
# --------------------------------------------------

# Use gauge when the user wants to monitor a value against
# a defined range, limit, or target.

# Example:

# {{
#     "id": "specific_water_gauge",
#     "type": "gauge",
#     "title": "Specific Water Consumption",
#     "parameter": {{
#         "global_code": "L1_SPEC_WTR_CON"
#     }},
#     "unit": "m³/t cement",
#     "min": 0,
#     "max": 2
# }}

# The min and max values in this example are illustrative.

# When possible, use the parameter's known minvalue and
# maxvalue from the available parameter information.

# Do not invent unsafe or unrealistic limits.

# --------------------------------------------------
# 7. PROGRESS
# --------------------------------------------------

# Use progress when representing a percentage,
# achievement, completion, or compliance level.

# Example:

# {{
#     "id": "emissions_compliance",
#     "type": "progress",
#     "title": "Emissions Compliance Rate",
#     "parameter": {{
#         "global_code": "L1_EMI_COMP_RATE"
#     }},
#     "unit": "%",
#     "min": 0,
#     "max": 100
# }}

# Progress is appropriate for percentage-based metrics.

# --------------------------------------------------
# 8. STATUS
# --------------------------------------------------

# Use status when the user wants to monitor an operational
# state, condition, or health indicator.

# Example:

# {{
#     "id": "emissions_status",
#     "type": "status",
#     "title": "Emissions Compliance Status",
#     "parameter": {{
#         "global_code": "L1_EMI_COMP_RATE"
#     }}
# }}

# Do not generate the actual status value.

# The backend/runtime system will determine the current value.

# --------------------------------------------------
# 9. TABLE
# --------------------------------------------------

# Use table when the user wants multiple parameters or
# detailed monitoring information in a tabular format.

# Example:

# {{
#     "id": "fuel_parameters_table",
#     "type": "table",
#     "title": "Fuel Parameters",
#     "dataSource": {{
#         "type": "parameters",
#         "parameters": [
#             {{
#                 "global_code": "L1_KL_COAL_FL"
#             }},
#             {{
#                 "global_code": "L1_KL_GAS_FL"
#             }},
#             {{
#                 "global_code": "L1_KL_OIL_FL"
#             }},
#             {{
#                 "global_code": "L1_KL_AFR_FL"
#             }}
#         ]
#     }},
#     "columns": [
#         {{
#             "field": "parameter",
#             "label": "Parameter"
#         }},
#         {{
#             "field": "value",
#             "label": "Value"
#         }},
#         {{
#             "field": "unit",
#             "label": "Unit"
#         }}
#     ]
# }}

# Do not include actual table rows or runtime values.

# ==================================================
# TIME RANGE RULES
# ==================================================

# For trend charts, use an appropriate time range when
# the user specifies one.

# Allowed examples:

# - "1h"
# - "6h"
# - "12h"
# - "24h"
# - "7d"
# - "30d"

# If the user does not specify a time range, use a sensible
# default such as:

# "24h"

# for operational monitoring, or

# "7d"

# for trend analysis.

# Do not generate actual timestamps.

# ==================================================
# MULTIPLE PARAMETERS
# ==================================================

# When a visualization compares multiple parameters,
# use:

# "dataSource": {{
#     "type": "parameters",
#     "parameters": [
#         {{
#             "global_code": "..."
#         }},
#         {{
#             "global_code": "..."
#         }}
#     ]
# }}

# Every GLOBAL_CODE MUST exist in AVAILABLE PARAMETERS.

# Do not generate parameter IDs.

# ==================================================
# SINGLE PARAMETER
# ==================================================

# For a visualization based on one parameter, use:

# "parameter": {{
#     "global_code": "..."
# }}

# Do not generate:

# "parameter": {{
#     "id": 33,
#     "global_code": "..."
# }}

# The backend will add the database ID.

# ==================================================
# COMPONENT DESIGN GUIDANCE
# ==================================================

# Choose components based on the user's actual request.

# Example:

# User:
# "Show current clinker production"

# Good:

# KPI

# Do not unnecessarily generate:
# - pie chart
# - table
# - gauge
# - multiple unrelated charts

# Example:

# User:
# "Show clinker production trend"

# Good:

# Line chart

# Example:

# User:
# "Show fuel energy mix"

# Good candidates:

# - pie_chart
# - bar_chart
# - KPI components for important individual mixes

# Example:

# User:
# "Create a management dashboard for plant energy"

# Possible components:

# - KPI
# - line_chart
# - bar_chart
# - table

# Only include parameters relevant to the request.

# ==================================================
# RUNTIME DATA RULE
# ==================================================

# The AI MUST NEVER generate actual values.

# BAD:

# "data": [
#     {{
#         "timestamp": "2026-09-09T10:00:00",
#         "value": 85.4
#     }}
# ]

# BAD:

# "currentValue": 85.4

# BAD:

# "latestValue": 85.4

# GOOD:

# "parameter": {{
#     "global_code": "L1_PLANT_PWR"
# }}

# The backend will retrieve the actual values.

# ==================================================
# DATABASE ID RULE
# ==================================================

# NEVER generate database IDs.

# BAD:

# "parameter": {{
#     "id": 33,
#     "global_code": "L1_FUEL_OIL_MIX"
# }}

# GOOD:

# "parameter": {{
#     "global_code": "L1_FUEL_OIL_MIX"
# }}

# The backend will resolve:

# L1_FUEL_OIL_MIX → database ID

# ==================================================
# LAYOUT RULE
# ==================================================

# Do NOT generate:

# - x
# - y
# - width
# - height
# - grid
# - layout
# - position
# - row
# - column

# React/backend will handle layout.

# ==================================================
# FORBIDDEN FIELDS
# ==================================================

# DO NOT include:

# - data
# - runtime values
# - latestValue
# - currentValue
# - lastUpdated
# - database IDs
# - parameterId
# - SQL
# - database queries
# - x
# - y
# - width
# - height
# - layout
# - position

# ==================================================
# FINAL VALIDATION RULES
# ==================================================

# Before returning the JSON, verify:

# 1. The root object contains "dashboard".
# 2. The dashboard contains:
#    - title
#    - subtitle
#    - components
# 3. Every component has:
#    - id
#    - type
#    - title
# 4. Every component ID is unique.
# 5. Every type is one of the allowed component types.
# 6. Every GLOBAL_CODE exists in AVAILABLE PARAMETERS.
# 7. GLOBAL_CODE values exactly match the database catalog.
# 8. No database IDs are generated.
# 9. No runtime values are generated.
# 10. No layout coordinates are generated.
# 11. No forbidden fields are included.
# 12. The JSON is valid.
# 13. Return only JSON.

# ==================================================
# OUTPUT FORMAT
# ==================================================

# Return ONLY valid JSON.

# Do not return:

# - Markdown
# - explanations
# - comments
# - ```json
# - ```

# Return exactly one JSON object.

# """
    
#     return prompt