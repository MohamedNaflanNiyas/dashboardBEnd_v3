DASHBOARD_PATTERNS = {

    "water": {

        "groups": {

            "water_consumption": [
                "PLNT_WTR_FRESH",
                "PLT_FRSH_WTR_INT",
            ],

            "water_reuse": [
                "PLNT_WTR_REUSE",
                "PLNT_WTR_REUSE_RATE",
            ],

            "water_balance": [
                "PLNT_WTR_ABS",
                "PLNT_WTR_FRESH",
                "PLNT_WTR_REUSE",
                "PLNT_WTR_DIS",
            ],
        },

        "visualizations": [
            "summary",
            "reuse",
            "consumption_trend",
            "water_balance_trend",
        ],
    },


    "emissions": {

        "groups": {

            "co2_summary": [
                "SCP1_CO2_EMI",
                "PLNT_CO2_EMI_INT",
                "PLNT_GHG_EMI",
                "PLNT_CO2_RED",
            ],

            "co2_sources": [
                "L1_FUEL_CO2_EMI",
                "L1_CALC_CO2_EMI",
            ],

            "fuel_mix": [
                "L1_FUEL_COAL_MIX",
                "L1_FUEL_GAS_MIX",
                "L1_FUEL_OIL_MIX",
                "L1_FUEL_AFR_MIX",
            ],

            "air_emissions": [
                "PLNT_NOX_CONC",
                "PLNT_SO2_CONC",
                "PLNT_PM_CONC",
            ],

            "air_compliance": [
                "PLNT_AIR_COM",
            ],
        },

        "visualizations": [
            "summary",
            "co2_trend",
            "source_comparison",
            "fuel_mix",
            "air_emissions",
            "compliance",
        ],
    },
}


def get_pattern(domain):

    return DASHBOARD_PATTERNS.get(
        domain,
        {}
    )


def get_pattern_groups(domain):

    pattern = get_pattern(domain)

    return pattern.get(
        "groups",
        {}
    )