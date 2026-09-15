# This file contains functions that are used to retrieve data from the database for the dashboard API. 
# The functions are used in the dashboard_api app to get the latest parameter values and parameter history for a 
# given plant and parameter.

from core.models import ParameterValue

# This function retrieves the latest parameter value for a given plant and parameter. 
# It returns the latest ParameterValue object or None if no value is found.
def get_latest_parameter_value(
    plant_id,
    parameter_id
):

    return (
        ParameterValue.objects
        .filter(
            plant_id=plant_id,
            parameter_id=parameter_id
        )
        .order_by("-timestamp")
        .first()
    )

#  This function retrieves the parameter history for a given plant and parameter.
# It returns a list of dictionaries containing the timestamp and value for each ParameterValue object,
# ordered by timestamp in ascending order. The number of values returned is limited by the limit parameter. 
def get_parameter_history(
    plant_id,
    parameter_id,
    limit=100
):

    values = (
        ParameterValue.objects
        .filter(
            plant_id=plant_id,
            parameter_id=parameter_id
        )
        .order_by("-timestamp")[:limit]
    )

    values = list(values)

    values.reverse()

    return [
        {
            "timestamp":
                value.timestamp.isoformat(),

            "value":
                value.value
        }
        for value in values
    ]