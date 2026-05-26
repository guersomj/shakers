import streamlit as st

from logic.cycle_logic import ShakerCycle


st.set_page_config(
    page_title="Shakers HMI Simulation",
    layout="centered"
)


def init_session():
    if "cycle" not in st.session_state:
        st.session_state.cycle = ShakerCycle()

    if "screen" not in st.session_state:
        st.session_state.screen = "HOME"


def go_to(screen_name):
    st.session_state.screen = screen_name
    st.rerun()


def hmi_header(title):
    st.title(title)
    st.caption("PLC/HMI logic simulation before ladder implementation.")
    st.divider()


def status_badge(label, active_text, inactive_text, active):
    if active:
        st.success(f"{label}: {active_text}")
    else:
        st.info(f"{label}: {inactive_text}")


def show_status_panel(cycle):
    st.subheader("System Status")

    st.write(f"**State:** {cycle.state}")
    st.write(f"**Temperature:** {cycle.temperature_c} °C")
    st.write(f"**Elapsed Time:** {cycle.elapsed_time_hours} h")
    st.write(f"**Cycle Running:** {cycle.cycle_running}")

    col1, col2 = st.columns(2)

    with col1:
        status_badge(
            "Latch",
            "LOCKED",
            "UNLOCKED",
            cycle.latch_locked
        )

        status_badge(
            "Agitator",
            "ON",
            "OFF",
            cycle.agitator_on
        )

    with col2:
        status_badge(
            "Buzzer",
            "ON",
            "OFF",
            cycle.buzzer_on
        )

        status_badge(
            "Finalize",
            "ENABLED",
            "DISABLED",
            cycle.finalize_enabled
        )


def home_screen(cycle):
    hmi_header("SHAKERS CONTROL")

    st.subheader("HOME / INICIO")

    st.info("System is waiting for cycle setup.")

    show_status_panel(cycle)

    if st.button("CONFIGURE CYCLE", use_container_width=True):
        go_to("SETUP")


def setup_screen(cycle):
    hmi_header("CYCLE SETUP")

    st.subheader("Select Product and Process")

    temperature = st.number_input(
        "Current Temperature (°C)",
        min_value=0.0,
        max_value=100.0,
        value=38.0,
        step=0.1
    )

    cycle.set_temperature(temperature)

    product = st.selectbox(
        "Product",
        ["HARMONY", "TAVI"]
    )

    process = st.selectbox(
        "Process",
        ["AOA", "BBB"]
    )

    cycle.select_product(product)
    cycle.select_process(process)

    st.divider()

    if cycle.is_temperature_valid_for_start():
        st.success("Temperature is valid for start.")
    else:
        st.error("Temperature is outside valid start range.")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("BACK", use_container_width=True):
            go_to("HOME")

    with col2:
        if st.button("CONTINUE", use_container_width=True):
            go_to("CONFIRM")


def confirm_screen(cycle):
    hmi_header("CONFIRM CYCLE")

    if not cycle.recipe:
        st.error("No recipe loaded. Return to setup.")
        if st.button("BACK TO SETUP", use_container_width=True):
            go_to("SETUP")
        return

    st.subheader("Recipe Summary")

    st.write(f"**Product:** {cycle.product}")
    st.write(f"**Process:** {cycle.process}")
    st.write(f"**Temperature:** {cycle.temperature_c} °C")
    st.write(f"**Minimum Time:** {cycle.recipe['min_time_hours']} h")
    st.write(f"**Maximum Time:** {cycle.recipe['max_time_hours']} h")

    if cycle.recipe["agitator_required"]:
        st.success("Agitator Required: YES")
    else:
        st.info("Agitator Required: NO")

    st.divider()

    if cycle.is_temperature_valid_for_start():
        st.success("Ready to start.")
    else:
        st.error("Cannot start. Temperature is outside valid range.")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("BACK", use_container_width=True):
            go_to("SETUP")

    with col2:
        if st.button("START CYCLE", use_container_width=True):
            if cycle.start_cycle():
                go_to("RUNNING")
            else:
                st.error("Cycle cannot be started. Check conditions.")


def running_screen(cycle):
    hmi_header("CYCLE RUNNING")

    st.subheader("Cycle in Progress")

    st.write(f"**Product:** {cycle.product}")
    st.write(f"**Process:** {cycle.process}")

    st.write(f"**Elapsed Time:** {cycle.elapsed_time_hours} h")
    st.write(f"**Minimum Time:** {cycle.recipe['min_time_hours']} h")
    st.write(f"**Maximum Time:** {cycle.recipe['max_time_hours']} h")

    st.divider()

    show_status_panel(cycle)

    st.divider()

    hours_to_advance = st.number_input(
        "Advance Time (hours)",
        min_value=0,
        max_value=100,
        value=1,
        step=1
    )

    if st.button("ADVANCE TIME", use_container_width=True):
        cycle.update_time(hours_to_advance)

        if cycle.state == "MAX_TIME_EXCEEDED":
            go_to("ALARM")

        elif cycle.state == "MIN_TIME_REACHED":
            go_to("READY")

        else:
            st.rerun()

    st.button(
        "FINALIZE CYCLE",
        disabled=not cycle.finalize_enabled,
        use_container_width=True
    )


def ready_screen(cycle):
    hmi_header("PRODUCT READY")

    st.success("Minimum time reached. Product is ready for removal.")

    st.write(f"**Product:** {cycle.product}")
    st.write(f"**Process:** {cycle.process}")
    st.write(f"**Elapsed Time:** {cycle.elapsed_time_hours} h")

    remaining_time = cycle.recipe["max_time_hours"] - cycle.elapsed_time_hours

    if remaining_time > 0:
        st.write(f"**Time remaining before alarm:** {remaining_time} h")
    else:
        st.write("**Time remaining before alarm:** 0 h")

    st.divider()

    show_status_panel(cycle)

    st.divider()

    hours_to_advance = st.number_input(
        "Advance Time (hours)",
        min_value=0,
        max_value=100,
        value=1,
        step=1
    )

    if st.button("ADVANCE TIME", use_container_width=True):
        cycle.update_time(hours_to_advance)

        if cycle.state == "MAX_TIME_EXCEEDED":
            go_to("ALARM")
        else:
            st.rerun()

    if st.button("FINALIZE CYCLE", use_container_width=True):
        if cycle.finalize_cycle():
            go_to("HOME")


def alarm_screen(cycle):
    hmi_header("MAX TIME EXCEEDED")

    st.error("Maximum time exceeded. Remove product and finalize cycle.")

    st.write(f"**Product:** {cycle.product}")
    st.write(f"**Process:** {cycle.process}")
    st.write(f"**Elapsed Time:** {cycle.elapsed_time_hours} h")

    st.divider()

    show_status_panel(cycle)

    st.divider()

    if st.button("FINALIZE CYCLE", use_container_width=True):
        if cycle.finalize_cycle():
            go_to("HOME")


init_session()

cycle = st.session_state.cycle
screen = st.session_state.screen

if screen == "HOME":
    home_screen(cycle)

elif screen == "SETUP":
    setup_screen(cycle)

elif screen == "CONFIRM":
    confirm_screen(cycle)

elif screen == "RUNNING":
    running_screen(cycle)

elif screen == "READY":
    ready_screen(cycle)

elif screen == "ALARM":
    alarm_screen(cycle)
