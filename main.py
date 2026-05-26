# Main simulation entry point for the shaker cycle control logic.

from logic.cycle_logic import ShakerCycle


def print_status(cycle):
    print("\n--- SYSTEM STATUS ---")
    print(f"State: {cycle.state}")
    print(f"Product: {cycle.product}")
    print(f"Process: {cycle.process}")
    print(f"Temperature: {cycle.temperature_c} °C")
    print(f"Elapsed time: {cycle.elapsed_time_hours} h")
    print(f"Cycle running: {cycle.cycle_running}")
    print(f"Latch locked: {cycle.latch_locked}")
    print(f"Agitator ON: {cycle.agitator_on}")
    print(f"Buzzer ON: {cycle.buzzer_on}")
    print(f"Finalize enabled: {cycle.finalize_enabled}")

    if cycle.recipe:
        print(f"Minimum time: {cycle.recipe['min_time_hours']} h")
        print(f"Maximum time: {cycle.recipe['max_time_hours']} h")

    print("---------------------\n")


def run_demo():
    cycle = ShakerCycle()

    print("SHAKERS LOGIC SIMULATION")

    # 1. Set temperature before start
    cycle.set_temperature(38.0)

    # 2. Select product and process
    cycle.select_product("HARMONY")
    cycle.select_process("AOA")

    print_status(cycle)

    # 3. Try to start cycle
    if cycle.start_cycle():
        print("Cycle started successfully.")
    else:
        print("Cycle could not be started.")

    print_status(cycle)

    # 4. Simulate time before minimum time
    cycle.update_time(50)
    print("50 hours passed.")
    print_status(cycle)

    # 5. Simulate reaching minimum time
    cycle.update_time(17)
    print("67 hours reached.")
    print_status(cycle)

    # 6. Simulate exceeding maximum time
    cycle.update_time(5)
    print("72 hours reached.")
    print_status(cycle)

    # 7. Finalize cycle
    if cycle.finalize_cycle():
        print("Cycle finalized. System returned to IDLE.")
    else:
        print("Cycle cannot be finalized yet.")

    print_status(cycle)


if __name__ == "__main__":
    run_demo()
