import streamlit as st

from logic.cycle_logic import ShakerCycle


st.set_page_config(
    page_title="Shakers Logic Simulation",
    layout="centered"
)

st.title("Shakers Logic Simulation")
st.write("PLC/HMI logic simulation before ladder implementation.")

# Keep cycle object in Streamlit memory
if "cycle" not in st.session_state:
    st.session_state.cycle = ShakerCycle()

cycle = st.session_state.cycle

st.divider()

st.header("Cycle Setup")

temperature = st.number_input(
    "Current Temperature (°C)",
    min_value=0.0,
    max_value=100.0,
    value=38.0,
    step=0.1
)

cycle.set_temperature(temperature)

product = st.selectbox(
    "Select Product",
    ["HARMONY", "TAVI"]
)

process = st.selectbox(
    "Select Process",
    ["AOA", "BBB"]
)

cycle.select_product(product)
cycle.select_process(process)

st.divider()

st.header("Recipe Loaded")

if cycle.recipe:
    st.write(f"**Product:** {cycle.product}")
    st.write(f"**Process:** {cycle.process}")
    st.write(f"**Minimum Time:** {cycle.recipe['min_time_hours']} h")
    st.write(f"**Maximum Time:** {cycle.recipe['max_time_hours']} h")
    st.write(f"**Agitator Required:** {cycle.recipe['agitator_required']}")

st.divider()

st.header("Controls")

if cycle.is_temperature_valid_for_start():
    st.success("Temperature is valid for start.")
else:
    st.error("Temperature is outside valid start range.")

if st.button("START CYCLE"):
    if cycle.start_cycle():
        st.success("Cycle started successfully.")
    else:
        st.error("Cycle cannot be started. Check conditions.")

hours_to_advance = st.number_input(
    "Advance Time (hours)",
    min_value=0,
    max_value=100,
    value=1,
    step=1
)

if st.button("ADVANCE TIME"):
    cycle.update_time(hours_to_advance)

if st.button("FINALIZE CYCLE"):
    if cycle.finalize_cycle():
        st.success("Cycle finalized. System returned to IDLE.")
    else:
        st.warning("Finalize Cycle is not available yet.")

st.divider()

st.header("System Status")

st.write(f"**State:** {cycle.state}")
st.write(f"**Temperature:** {cycle.temperature_c} °C")
st.write(f"**Elapsed Time:** {cycle.elapsed_time_hours} h")
st.write(f"**Cycle Running:** {cycle.cycle_running}")
st.write(f"**Latch Locked:** {cycle.latch_locked}")
st.write(f"**Agitator ON:** {cycle.agitator_on}")
st.write(f"**Buzzer ON:** {cycle.buzzer_on}")
st.write(f"**Finalize Enabled:** {cycle.finalize_enabled}")
