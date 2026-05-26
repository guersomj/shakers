# Preset recipe times for shaker cycle simulation.
# Times are defined in hours.

RECIPES = {
    ("HARMONY", "AOA"): {
        "min_time_hours": 67,
        "max_time_hours": 72,
        "agitator_required": True,
    },
    ("HARMONY", "BBB"): {
        "min_time_hours": 21,
        "max_time_hours": 27,
        "agitator_required": False,
    },
    ("TAVI", "AOA"): {
        "min_time_hours": 6,
        "max_time_hours": 27,
        "agitator_required": True,
    },
    ("TAVI", "BBB"): {
        "min_time_hours": 21,
        "max_time_hours": 27,
        "agitator_required": False,
    },
}


VALID_PRODUCTS = ["HARMONY", "TAVI"]

VALID_PROCESSES = ["AOA", "BBB"]

MIN_START_TEMPERATURE_C = 35.5
MAX_START_TEMPERATURE_C = 39.5
