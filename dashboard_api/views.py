# Create your views here.
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import traceback

from core.models import (
    Dashboard,
    Plant,
    ParameterValue
)

from .serializers import DashboardSerializer

from ai_dashboard.service import (
    generate_dashboard_from_request
)
from .definition_utils import (
    get_dashboard_parameter_ids
)

from .runtime_service import (
    get_latest_parameter_value,
    get_parameter_history
)

class GenerateDashboardView(APIView):

    def post(self, request):

        # Get request data
        user_request = request.data.get("request")

        if not user_request:

            return Response(
                {
                    "error": "request is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            plant_id = request.data.get("plant_id")

            if not plant_id:
                return Response(
                    {
                        "error": "plant_id is required."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            plant = get_object_or_404(
                Plant,
                id=plant_id
            )

            # Generate dashboard using AI
            dashboard = (
                generate_dashboard_from_request(
                    user_request
                )
            )

            definition = dashboard["dashboard"]

            saved_dashboard = Dashboard.objects.create(
                plant=plant,
                dashboard_name=definition["title"],
                title=definition["title"],
                subtitle=definition.get(
                    "subtitle",
                    ""
                ),
                definition=dashboard
            )

            return Response(
                DashboardSerializer(
                    saved_dashboard
                ).data,
                status=status.HTTP_201_CREATED
            )
        

        except ValueError as error:

            return Response(
                {
                    "error": str(error)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            print("Dashboard generation error:", e)
            traceback.print_exc()

            return Response(
                {
                    "error": (
                        "Unexpected error while "
                        "generating dashboard."
                    )
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# class GenerateDashboardView(APIView):

#     def post(self, request):

#         plant_id = request.data.get(
#             "plant_id"
#         )

#         user_request = request.data.get(
#             "request"
#         )

#         if not plant_id:
#             return Response(
#                 {
#                     "error": "plant_id is required"
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         if not user_request:
#             return Response(
#                 {
#                     "error": "request is required"
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         plant = get_object_or_404(
#             Plant,
#             id=plant_id
#         )

#         try:

#             dashboard = (
#                 generate_dashboard_from_request(
#                     user_request
#                 )
#             )

#         except Exception as error:

#             return Response(
#                 {
#                     "error": str(error)
#                 },
#                 status=(
#                     status.HTTP_500_INTERNAL_SERVER_ERROR
#                 )
#             )

        # definition = dashboard["dashboard"]

        # saved_dashboard = Dashboard.objects.create(
        #     plant=plant,
        #     dashboard_name=definition["title"],
        #     title=definition["title"],
        #     subtitle=definition.get(
        #         "subtitle",
        #         ""
        #     ),
        #     definition=dashboard
        # )

        # return Response(
        #     DashboardSerializer(
        #         saved_dashboard
        #     ).data,
        #     status=status.HTTP_201_CREATED
        # )


class DashboardDetailView(APIView):

    def get(self, request, dashboard_id):

        dashboard = get_object_or_404(
            Dashboard,
            id=dashboard_id,
            is_active=True
        )

        return Response(
            dashboard.definition
        )

# This is where DB values are exposed to React.
class DashboardDataView(APIView):

    def get(
        self,
        request,
        dashboard_id
    ):

        dashboard = get_object_or_404(
            Dashboard,
            id=dashboard_id,
            is_active=True
        )

        parameter_ids = (
            get_dashboard_parameter_ids(
                dashboard.definition
            )
        )

        result = {}

        for parameter_id in parameter_ids:

            latest = (
                get_latest_parameter_value(
                    dashboard.plant_id,
                    parameter_id
                )
            )

            history = (
                get_parameter_history(
                    dashboard.plant_id,
                    parameter_id
                )
            )

            result[str(parameter_id)] = {

                "current": (
                    latest.value
                    if latest
                    else None
                ),

                "timestamp": (
                    latest.timestamp.isoformat()
                    if latest
                    else None
                ),

                "history": history
            }

        return Response(
            {
                "dashboard_id":
                    dashboard.id,

                "plant_id":
                    dashboard.plant_id,

                "parameters":
                    result
            }
        )