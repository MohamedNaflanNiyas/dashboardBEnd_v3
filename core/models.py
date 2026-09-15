# Create your models here.
from django.db import models


class Plant(models.Model):
    id = models.BigAutoField(primary_key=True)

    plant_code = models.CharField(
        max_length=100,
        unique=True
    )

    plant_name = models.CharField(
        max_length=255
    )

    location = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.plant_name


class Parameter(models.Model):
    id = models.BigAutoField(primary_key=True)

    global_code = models.CharField(
        max_length=150,
        unique=True
    )

    parameter_name = models.CharField(
        max_length=255
    )

    parameter_description = models.TextField(
        blank=True,
        null=True
    )

    uom = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    minvalue = models.FloatField(
        blank=True,
        null=True
    )

    maxvalue = models.FloatField(
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.id} - {self.global_code}"


class ParameterValue(models.Model):

    id = models.BigAutoField(
        primary_key=True
    )

    plant = models.ForeignKey(
        Plant,
        on_delete=models.CASCADE,
        related_name="parameter_values"
    )

    parameter = models.ForeignKey(
        Parameter,
        on_delete=models.CASCADE,
        related_name="values"
    )

    timestamp = models.DateTimeField(
        db_index=True
    )

    value = models.FloatField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "plant",
                    "parameter",
                    "timestamp"
                ],
                name=(
                    "unique_plant_parameter_timestamp"
                )
            )
        ]

        indexes = [

            models.Index(
                fields=[
                    "parameter",
                    "-timestamp"
                ]
            ),

            models.Index(
                fields=[
                    "plant",
                    "parameter",
                    "-timestamp"
                ]
            ),
        ]

    def __str__(self):

        return (
            f"{self.parameter.global_code}: "
            f"{self.value}"
        )


class Dashboard(models.Model):
    id = models.BigAutoField(primary_key=True)

    plant = models.ForeignKey(
        Plant,
        on_delete=models.CASCADE,
        related_name="dashboards"
    )

    dashboard_name = models.CharField(
        max_length=255
    )

    title = models.CharField(
        max_length=255
    )

    subtitle = models.TextField(
        blank=True,
        null=True
    )

    definition = models.JSONField()

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.dashboard_name



class ParameterMetaData(models.Model):
    id = models.BigAutoField(primary_key=True)

    global_code = models.CharField(
        max_length=150,
        unique=True
    )

    parameter_name = models.CharField(
        max_length=255
    )

    parameter_description = models.TextField(
        blank=True,
        null=True
    )

    uom = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    minvalue = models.FloatField(
        blank=True,
        null=True
    )

    maxvalue = models.FloatField(
        blank=True,
        null=True
    )

    # AI / semantic metadata
    
    domain = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    category = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    process = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    asset = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    metric_type = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    keywords = models.JSONField(
        default=list,
        blank=True
    )

    # ---------------------------------------

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.global_code} - {self.parameter_name}"