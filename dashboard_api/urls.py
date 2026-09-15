from django.urls import path

from .views import (
    GenerateDashboardView,
    DashboardDetailView,
    DashboardDataView
)


urlpatterns = [

    path(
        "generate/",
        GenerateDashboardView.as_view(),
        name="generate-dashboard"
    ),

    path(
        "<int:dashboard_id>/",
        DashboardDetailView.as_view(),
        name="dashboard-detail"
    ),

    path(
        "<int:dashboard_id>/data/",
        DashboardDataView.as_view(),
        name="dashboard-data"
    ),
]