# SHAKERS - Logic Plan

## Objective

Create a logic simulation for shaker cycle control before PLC ladder implementation.

The purpose of this project is to define, test, and validate the process logic in a simple software environment before implementing it in a PLC and HMI.

---

## Main Process Flow

1. System starts in idle state.
2. Temperature is validated before allowing the cycle to start.
3. Operator selects one product.
4. Operator selects one process.
5. System loads the preset minimum and maximum cycle times.
6. Operator starts the cycle.
7. Door latch is locked during the cycle.
8. If process is AOA, the agitator is activated.
9. If process is BBB, the agitator remains off.
10. When minimum time is reached, the latch is unlocked.
11. The FINALIZE CYCLE button becomes available.
12. If maximum time is exceeded, buzzer/alarm is activated.
13. Operator presses FINALIZE CYCLE.
14. System returns to idle state.

---

## Temperature Rule

Temperature is only validated before starting the cycle.

Valid temperature range:

- Minimum: 35.5 °C
- Maximum: 39.5 °C

If temperature is outside this range, the system must not allow the cycle to start.

Once the cycle has started, temperature changes must not interrupt the cycle.

---

## Product Selection

Only one product can be selected at a time.

Available products:

- HARMONY
- TAVI

The system must not allow both products to be selected at the same time.

---

## Process Selection

Only one process can be selected at a time.

Available processes:

- AOA
- BBB

The system must not allow both processes to be selected at the same time.

---

## Recipe Time Table

| Product | Process | Minimum Time | Maximum Time |
|---|---|---:|---:|
| HARMONY | AOA | 67 h | 72 h |
| HARMONY | BBB | 21 h | 27 h |
| TAVI | AOA | 6 h | 27 h |
| TAVI | BBB | 21 h | 27 h |

---

## Door Latch Logic

At cycle start:

- Door latch locks.

Before minimum time:

- Door latch remains locked.
- FINALIZE CYCLE button remains disabled.

When minimum time is reached:

- Door latch unlocks.
- FINALIZE CYCLE button becomes enabled.
- System displays that product is ready for removal.

If maximum time is exceeded:

- Door latch remains unlocked.
- FINALIZE CYCLE button remains enabled.
- Buzzer/alarm activates.

---

## Agitator Logic

The agitator output depends on the selected process.

If selected process is AOA:

- Agitator turns ON during the active cycle.

If selected process is BBB:

- Agitator remains OFF during the active cycle.

When the cycle is finalized:

- Agitator turns OFF.

---

## Finalize Cycle Logic

The FINALIZE CYCLE button is only active when minimum time has been reached.

If operator presses FINALIZE CYCLE after minimum time:

- Cycle ends.
- Timer resets.
- Alarm/buzzer turns off.
- Agitator turns off.
- Product selection clears.
- Process selection clears.
- System returns to idle state.

---

## Current System States

Proposed states:

1. IDLE
2. READY_TO_START
3. RUNNING
4. MIN_TIME_REACHED
5. MAX_TIME_EXCEEDED
6. CYCLE_COMPLETE
7. ALARM
