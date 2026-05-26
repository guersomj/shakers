# Core logic for shaker cycle simulation.

from data.recipes import (
    RECIPES,
    VALID_PRODUCTS,
    VALID_PROCESSES,
    MIN_START_TEMPERATURE_C,
    MAX_START_TEMPERATURE_C,
)


class ShakerCycle:
    def __init__(self):
        self.state = "IDLE"

        self.product = None
        self.process = None
        self.recipe = None

        self.temperature_c = None
        self.elapsed_time_hours = 0

        self.cycle_running = False
        self.latch_locked = False
        self.agitator_on = False
        self.buzzer_on = False
        self.finalize_enabled = False

    def set_temperature(self, temperature_c):
        self.temperature_c = temperature_c

    def is_temperature_valid_for_start(self):
        if self.temperature_c is None:
            return False

        return (
            MIN_START_TEMPERATURE_C
            <= self.temperature_c
            <= MAX_START_TEMPERATURE_C
        )

    def select_product(self, product):
        product = product.upper()

        if product not in VALID_PRODUCTS:
            raise ValueError("Invalid product selected.")

        self.product = product
        self.load_recipe_if_ready()

    def select_process(self, process):
        process = process.upper()

        if process not in VALID_PROCESSES:
            raise ValueError("Invalid process selected.")

        self.process = process
        self.load_recipe_if_ready()

    def load_recipe_if_ready(self):
        if self.product and self.process:
            self.recipe = RECIPES.get((self.product, self.process))

    def can_start_cycle(self):
        return (
            self.is_temperature_valid_for_start()
            and self.product is not None
            and self.process is not None
            and self.recipe is not None
            and not self.cycle_running
        )

    def start_cycle(self):
        if not self.can_start_cycle():
            self.state = "NOT_READY"
            return False

        self.state = "RUNNING"
        self.cycle_running = True
        self.elapsed_time_hours = 0

        self.latch_locked = True
        self.finalize_enabled = False
        self.buzzer_on = False

        self.agitator_on = self.recipe["agitator_required"]

        return True

    def update_time(self, hours):
        if not self.cycle_running:
            return

        self.elapsed_time_hours += hours

        min_time = self.recipe["min_time_hours"]
        max_time = self.recipe["max_time_hours"]

        if self.elapsed_time_hours >= min_time:
            self.finalize_enabled = True
            self.latch_locked = False
            self.state = "MIN_TIME_REACHED"

        if self.elapsed_time_hours >= max_time:
            self.buzzer_on = True
            self.state = "MAX_TIME_EXCEEDED"

    def finalize_cycle(self):
        if not self.finalize_enabled:
            return False

        self.reset_cycle()
        return True

    def reset_cycle(self):
        self.state = "IDLE"

        self.product = None
        self.process = None
        self.recipe = None

        self.elapsed_time_hours = 0

        self.cycle_running = False
        self.latch_locked = False
        self.agitator_on = False
        self.buzzer_on = False
        self.finalize_enabled = False
