from rest_framework import serializers
from core.models import Dashboard


class DashboardSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = Dashboard

        fields = [
            "id",
            "plant",
            "dashboard_name",
            "title",
            "subtitle",
            "definition",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]