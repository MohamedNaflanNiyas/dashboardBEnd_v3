from django.core.management.base import BaseCommand

from core.models import Parameter
from core.models import ParameterMetaData


PARAMETER_METADATA = {

    # KILN / PRODUCTION

    "L1_KL_CLK_PROD": {
        "domain": "production",
        "category": "production",
        "process": "kiln",
        "asset": "kiln",
        "metric_type": "quantity",
        "keywords": [
            "clinker production",
            "clinker",
            "production",
            "kiln production",
            "output"
        ],
    },

    "L1_KL_COAL_FL": {
        "domain": "energy",
        "category": "fuel",
        "process": "kiln",
        "asset": "kiln",
        "metric_type": "flow",
        "keywords": [
            "coal flow",
            "coal consumption",
            "kiln coal",
            "fuel"
        ],
    },

    "L1_KL_GAS_FL": {
        "domain": "energy",
        "category": "fuel",
        "process": "kiln",
        "asset": "kiln",
        "metric_type": "flow",
        "keywords": [
            "gas flow",
            "gas consumption",
            "kiln gas",
            "fuel"
        ],
    },

    "L1_KL_OIL_FL": {
        "domain": "energy",
        "category": "fuel",
        "process": "kiln",
        "asset": "kiln",
        "metric_type": "flow",
        "keywords": [
            "oil flow",
            "oil consumption",
            "kiln oil",
            "fuel"
        ],
    },

    "L1_KL_AFR_FL": {
        "domain": "energy",
        "category": "alternative_fuel",
        "process": "kiln",
        "asset": "kiln",
        "metric_type": "flow",
        "keywords": [
            "AFR",
            "alternative fuel",
            "alternative fuel flow",
            "fuel substitution"
        ],
    },

    "L1_KL_TCOAL_FL": {
        "domain": "energy",
        "category": "fuel",
        "process": "kiln",
        "asset": "kiln",
        "metric_type": "flow",
        "keywords": [
            "total coal",
            "coal flow",
            "total coal consumption"
        ],
    },

    "L1_KL_TGAS_FL": {
        "domain": "energy",
        "category": "fuel",
        "process": "kiln",
        "asset": "kiln",
        "metric_type": "flow",
        "keywords": [
            "total gas",
            "gas flow",
            "gas consumption"
        ],
    },

    "L1_KL_GAS_CV": {
        "domain": "energy",
        "category": "fuel_quality",
        "process": "kiln",
        "asset": "kiln",
        "metric_type": "calorific_value",
        "keywords": [
            "gas calorific value",
            "gas CV",
            "gas energy value"
        ],
    },

    "L1_KL_COAL_CV": {
        "domain": "energy",
        "category": "fuel_quality",
        "process": "kiln",
        "asset": "kiln",
        "metric_type": "calorific_value",
        "keywords": [
            "coal calorific value",
            "coal CV",
            "coal energy value"
        ],
    },

    "L1_KL_OIL_CV": {
        "domain": "energy",
        "category": "fuel_quality",
        "process": "kiln",
        "asset": "kiln",
        "metric_type": "calorific_value",
        "keywords": [
            "oil calorific value",
            "oil CV",
            "oil energy value"
        ],
    },

    "L1_KL_AFR_CV": {
        "domain": "energy",
        "category": "fuel_quality",
        "process": "kiln",
        "asset": "kiln",
        "metric_type": "calorific_value",
        "keywords": [
            "AFR calorific value",
            "alternative fuel CV",
            "alternative fuel energy value"
        ],
    },

    "L1_KL_SHC": {
        "domain": "energy",
        "category": "efficiency",
        "process": "kiln",
        "asset": "kiln",
        "metric_type": "intensity",
        "keywords": [
            "specific heat consumption",
            "thermal energy",
            "thermal efficiency",
            "kiln energy",
            "heat consumption"
        ],
    },

    "L1_KL_TOT_PWR": {
        "domain": "energy",
        "category": "electricity",
        "process": "kiln",
        "asset": "kiln",
        "metric_type": "consumption",
        "keywords": [
            "kiln power",
            "kiln electricity",
            "total kiln power"
        ],
    },

    # CEMENT MILL
  
    "L1_CM1_TOT_FL": {
        "domain": "production",
        "category": "cement",
        "process": "cement_mill",
        "asset": "cement_mill",
        "metric_type": "flow",
        "keywords": [
            "cement mill feed",
            "cement production",
            "cement feed",
            "mill feed"
        ],
    },

    "L1_CM1_BLAINE": {
        "domain": "production",
        "category": "quality",
        "process": "cement_mill",
        "asset": "cement_mill",
        "metric_type": "quality",
        "keywords": [
            "blaine",
            "cement fineness",
            "cement quality",
            "fineness"
        ],
    },

    # CO2 / EMISSIONS

    "L1_FUEL_CO2_EMI": {
        "domain": "emissions",
        "category": "co2",
        "process": "kiln",
        "asset": "kiln",
        "metric_type": "emission",
        "keywords": [
            "fuel CO2",
            "fuel carbon dioxide",
            "fuel emissions",
            "CO2 emissions from fuel"
        ],
    },

    "L1_CALC_CO2_EMI": {
        "domain": "emissions",
        "category": "co2",
        "process": "kiln",
        "asset": "kiln",
        "metric_type": "emission",
        "keywords": [
            "calcination CO2",
            "calcination emissions",
            "process CO2",
            "calcination"
        ],
    },

    "L1_SCP1_CO2_EMI": {
        "domain": "emissions",
        "category": "scope_1",
        "process": "kiln",
        "asset": "plant",
        "metric_type": "emission",
        "keywords": [
            "scope 1",
            "scope 1 CO2",
            "CO2 emission",
            "direct emissions"
        ],
    },

    "L1_CLK_CO2_EMI": {
        "domain": "emissions",
        "category": "co2",
        "process": "kiln",
        "asset": "kiln",
        "metric_type": "intensity",
        "keywords": [
            "specific CO2",
            "CO2 intensity",
            "clinker CO2",
            "specific emission"
        ],
    },

    # FUEL MIX

    "L1_FUEL_COAL_MIX": {
        "domain": "energy",
        "category": "fuel_mix",
        "process": "kiln",
        "asset": "kiln",
        "metric_type": "percentage",
        "keywords": [
            "coal energy mix",
            "coal mix",
            "fuel mix",
            "energy mix",
            "coal percentage"
        ],
    },

    "L1_FUEL_GAS_MIX": {
        "domain": "energy",
        "category": "fuel_mix",
        "process": "kiln",
        "asset": "kiln",
        "metric_type": "percentage",
        "keywords": [
            "gas energy mix",
            "gas mix",
            "fuel mix",
            "energy mix",
            "gas percentage"
        ],
    },

    "L1_FUEL_OIL_MIX": {
        "domain": "energy",
        "category": "fuel_mix",
        "process": "kiln",
        "asset": "kiln",
        "metric_type": "percentage",
        "keywords": [
            "oil energy mix",
            "oil mix",
            "fuel mix",
            "energy mix",
            "oil percentage"
        ],
    },

    "L1_FUEL_AFR_MIX": {
        "domain": "energy",
        "category": "fuel_mix",
        "process": "kiln",
        "asset": "kiln",
        "metric_type": "percentage",
        "keywords": [
            "AFR energy mix",
            "alternative fuel mix",
            "fuel mix",
            "energy mix",
            "AFR percentage"
        ],
    },

    # ELECTRICITY

    "L1_SPEC_ELEC": {
        "domain": "energy",
        "category": "electricity",
        "process": "plant",
        "asset": "plant",
        "metric_type": "intensity",
        "keywords": [
            "specific electrical energy",
            "specific electricity",
            "electricity intensity",
            "electrical energy"
        ],
    },

    "L1_PLANT_PWR": {
        "domain": "energy",
        "category": "electricity",
        "process": "plant",
        "asset": "plant",
        "metric_type": "power",
        "keywords": [
            "plant power",
            "plant electricity",
            "total power",
            "electric power"
        ],
    },

    # PROCESS EFFICIENCY

    "L1_CLK_CEM_FACT": {
        "domain": "production",
        "category": "efficiency",
        "process": "cement",
        "asset": "plant",
        "metric_type": "ratio",
        "keywords": [
            "clinker cement ratio",
            "clinker to cement ratio",
            "clinker factor"
        ],
    },

    "L1_SCM_SUB_RATE": {
        "domain": "production",
        "category": "sustainability",
        "process": "cement",
        "asset": "plant",
        "metric_type": "percentage",
        "keywords": [
            "SCM substitution",
            "SCM rate",
            "supplementary cementitious material",
            "cement substitution"
        ],
    },

    "L1_RM_MIX_EFF": {
        "domain": "production",
        "category": "efficiency",
        "process": "raw_material",
        "asset": "raw_mill",
        "metric_type": "efficiency",
        "keywords": [
            "raw material mix efficiency",
            "raw material efficiency",
            "mix efficiency"
        ],
    },

    # WATER

    "L1_PROC_WTR_INJ": {
        "domain": "water",
        "category": "process_water",
        "process": "kiln",
        "asset": "kiln",
        "metric_type": "consumption",
        "keywords": [
            "process water",
            "water injection",
            "kiln water",
            "water consumption"
        ],
    },

    "L1_SPEC_WTR_CON": {
        "domain": "water",
        "category": "efficiency",
        "process": "plant",
        "asset": "plant",
        "metric_type": "intensity",
        "keywords": [
            "specific water consumption",
            "water intensity",
            "water consumption intensity"
        ],
    },

    # COMPLIANCE

    "L1_EMI_COMP_RATE": {
        "domain": "emissions",
        "category": "compliance",
        "process": "plant",
        "asset": "plant",
        "metric_type": "percentage",
        "keywords": [
            "emissions compliance",
            "compliance rate",
            "emission compliance"
        ],
    },

    "L1_EMI_EXC_EVT": {
        "domain": "emissions",
        "category": "compliance",
        "process": "plant",
        "asset": "plant",
        "metric_type": "count",
        "keywords": [
            "emission exceedance",
            "exceedance events",
            "emission violations"
        ],
    },

    "L1_EMI_EXC_DUR": {
        "domain": "emissions",
        "category": "compliance",
        "process": "plant",
        "asset": "plant",
        "metric_type": "duration",
        "keywords": [
            "emission exceedance duration",
            "exceedance duration",
            "emission violation duration"
        ],
    },

    # BAGHOUSE

    "L1_KL_BH_O2": {
        "domain": "emissions",
        "category": "air_quality",
        "process": "kiln",
        "asset": "baghouse",
        "metric_type": "concentration",
        "keywords": [
            "baghouse oxygen",
            "baghouse O2",
            "outlet oxygen",
            "O2"
        ],
    },

    # PLANT LEVEL

    "SCP1_CO2_EMI": {
        "domain": "emissions",
        "category": "scope_1",
        "process": "plant",
        "asset": "plant",
        "metric_type": "emission",
        "keywords": [
            "total scope 1",
            "plant scope 1",
            "total CO2",
            "plant CO2 emissions"
        ],
    },

    "PLNT_CO2_EMI_INT": {
        "domain": "emissions",
        "category": "co2",
        "process": "plant",
        "asset": "plant",
        "metric_type": "intensity",
        "keywords": [
            "CO2 intensity",
            "plant CO2 intensity",
            "carbon intensity",
            "emission intensity"
        ],
    },

    "PLNT_GHG_EMI": {
        "domain": "emissions",
        "category": "ghg",
        "process": "plant",
        "asset": "plant",
        "metric_type": "emission",
        "keywords": [
            "GHG",
            "greenhouse gas",
            "total GHG",
            "greenhouse gas emissions"
        ],
    },

    "PLNT_CO2_RED": {
        "domain": "emissions",
        "category": "reduction",
        "process": "plant",
        "asset": "plant",
        "metric_type": "reduction",
        "keywords": [
            "CO2 reduction",
            "carbon reduction",
            "emission reduction",
            "carbon savings"
        ],
    },

    # PLANT WATER

    "PLNT_WTR_ABS": {
        "domain": "water",
        "category": "consumption",
        "process": "plant",
        "asset": "plant",
        "metric_type": "consumption",
        "keywords": [
            "water abstraction",
            "water withdrawal",
            "water consumption",
            "total water"
        ],
    },

    "PLNT_WTR_FRESH": {
        "domain": "water",
        "category": "fresh_water",
        "process": "plant",
        "asset": "plant",
        "metric_type": "consumption",
        "keywords": [
            "fresh water",
            "freshwater consumption",
            "fresh water consumption",
            "water consumption"
        ],
    },

    "PLNT_WTR_REUSE": {
        "domain": "water",
        "category": "reuse",
        "process": "plant",
        "asset": "plant",
        "metric_type": "consumption",
        "keywords": [
            "water reuse",
            "water reused",
            "recycled water",
            "reused water",
            "water recycling"
        ],
    },

    "PLNT_WTR_REUSE_RATE": {
        "domain": "water",
        "category": "reuse",
        "process": "plant",
        "asset": "plant",
        "metric_type": "percentage",
        "keywords": [
            "water reuse rate",
            "water recycling rate",
            "reuse percentage",
            "recycled water percentage"
        ],
    },

    "PLNT_WTR_DIS": {
        "domain": "water",
        "category": "discharge",
        "process": "plant",
        "asset": "plant",
        "metric_type": "discharge",
        "keywords": [
            "water discharge",
            "wastewater discharge",
            "water released"
        ],
    },

    "PLT_FRSH_WTR_INT": {
        "domain": "water",
        "category": "efficiency",
        "process": "plant",
        "asset": "plant",
        "metric_type": "intensity",
        "keywords": [
            "fresh water intensity",
            "freshwater intensity",
            "water intensity"
        ],
    },
    
    # AIR EMISSIONS

    "PLNT_NOX_CONC": {
        "domain": "air_emissions",
        "category": "nox",
        "process": "plant",
        "asset": "stack",
        "metric_type": "concentration",
        "keywords": [
            "NOx",
            "NO2",
            "nitrogen oxides",
            "NOx concentration",
            "air emissions"
        ],
    },

    "PLNT_SO2_CONC": {
        "domain": "air_emissions",
        "category": "so2",
        "process": "plant",
        "asset": "stack",
        "metric_type": "concentration",
        "keywords": [
            "SO2",
            "sulfur dioxide",
            "SO2 concentration",
            "air emissions"
        ],
    },

    "PLNT_PM_CONC": {
        "domain": "air_emissions",
        "category": "pm",
        "process": "plant",
        "asset": "stack",
        "metric_type": "concentration",
        "keywords": [
            "PM",
            "particulate matter",
            "dust",
            "PM concentration",
            "air emissions"
        ],
    },

    "PLNT_NOX_EMI": {
        "domain": "air_emissions",
        "category": "nox",
        "process": "plant",
        "asset": "stack",
        "metric_type": "emission",
        "keywords": [
            "NOx emission",
            "NO2 emission",
            "nitrogen oxide emissions"
        ],
    },

    "PLNT_SO2_EMI": {
        "domain": "air_emissions",
        "category": "so2",
        "process": "plant",
        "asset": "stack",
        "metric_type": "emission",
        "keywords": [
            "SO2 emission",
            "sulfur dioxide emissions"
        ],
    },

    "PLNT_PM_EMI": {
        "domain": "air_emissions",
        "category": "pm",
        "process": "plant",
        "asset": "stack",
        "metric_type": "emission",
        "keywords": [
            "PM emission",
            "particulate emissions",
            "dust emissions"
        ],
    },

    "PLNT_AIR_COM": {
        "domain": "air_emissions",
        "category": "compliance",
        "process": "plant",
        "asset": "stack",
        "metric_type": "percentage",
        "keywords": [
            "air emissions compliance",
            "air compliance",
            "emission compliance rate"
        ],
    },
}


class Command(BaseCommand):

    help = "Populate ParameterMetaData from existing Parameter records and AI semantic metadata."

    def handle(self, *args, **options):

        created_count = 0
        updated_count = 0
        missing_metadata_count = 0

        parameters = Parameter.objects.all()

        self.stdout.write(
            self.style.NOTICE(
                f"Found {parameters.count()} existing parameters."
            )
        )

        for parameter in parameters:

            global_code = parameter.global_code

            metadata = PARAMETER_METADATA.get(global_code)

            if metadata is None:

                missing_metadata_count += 1

                self.stdout.write(
                    self.style.WARNING(
                        f"No semantic metadata found for: {global_code}"
                    )
                )

                # Still create/update the record using the
                # existing parameter information.
                metadata = {
                    "domain": None,
                    "category": None,
                    "process": None,
                    "asset": None,
                    "metric_type": None,
                    "keywords": [],
                }

            obj, created = ParameterMetaData.objects.update_or_create(

                global_code=global_code,

                defaults={
                    "parameter_name": parameter.parameter_name,
                    "parameter_description": parameter.parameter_description,
                    "uom": parameter.uom,
                    "minvalue": parameter.minvalue,
                    "maxvalue": parameter.maxvalue,

                    "domain": metadata.get("domain"),
                    "category": metadata.get("category"),
                    "process": metadata.get("process"),
                    "asset": metadata.get("asset"),
                    "metric_type": metadata.get("metric_type"),
                    "keywords": metadata.get("keywords", []),

                    "is_active": parameter.is_active,
                },
            )

            if created:
                created_count += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created: {global_code}"
                    )
                )

            else:
                updated_count += 1

                self.stdout.write(
                    self.style.NOTICE(
                        f"Updated: {global_code}"
                    )
                )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Created: {created_count}"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Updated: {updated_count}"
            )
        )

        self.stdout.write(
            self.style.WARNING(
                f"Missing semantic metadata: {missing_metadata_count}"
            )
        )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "Parameter metadata population completed."
            )
        )

# class Command(BaseCommand):

#     help = "Populate AI semantic metadata for parameters"

#     def handle(self, *args, **options):

#         updated = 0
#         missing = 0

#         for global_code, metadata in PARAMETER_METADATA.items():

#             try:
#                 parameter = ParameterMetaData.objects.get(
#                     global_code=global_code
#                 )
#             except ParameterMetaData.DoesNotExist:
#                 self.stdout.write(
#                     self.style.WARNING(
#                         f"Missing parameter: {global_code}"
#                     )
#                 )
#                 missing += 1
#                 continue

#             for field, value in metadata.items():
#                 setattr(parameter, field, value)

#             parameter.save()

#             updated += 1

#             self.stdout.write(
#                 self.style.SUCCESS(
#                     f"Updated: {global_code}"
#                 )
#             )

#         self.stdout.write("")
#         self.stdout.write(
#             self.style.SUCCESS(
#                 f"Updated {updated} parameters."
#             )
#         )

#         if missing:
#             self.stdout.write(
#                 self.style.WARNING(
#                     f"{missing} parameters were not found."
#                 )
#             )