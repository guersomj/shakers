# Shakers Logic Simulation

Logic simulation for shaker cycle control before PLC ladder implementation.

## Purpose

This project is intended to define and test the control logic for a shaker cycle system before implementing it in a PLC and HMI.

The goal is to validate the process behavior in Python first, then translate the confirmed logic into ladder programming.

## Current Scope

The system logic includes:

- Product selection
- Process selection
- Temperature validation before cycle start
- Minimum and maximum cycle timing
- Door latch control
- Agitator control
- Finalize cycle logic
- Alarm/buzzer for maximum time exceeded

## Products

Only one product can be selected at a time:

- HARMONY
- TAVI

## Processes

Only one process can be selected at a time:

- AOA
- BBB

## Temperature Requirement

Temperature must be within the valid range before starting the cycle:

- Minimum: 35.5 °C
- Maximum: 39.5 °C

Once the cycle has started, temperature changes do not interrupt the cycle.

## Recipe Table

| Product | Process | Minimum Time | Maximum Time |
|---|---|---:|---:|
| HARMONY | AOA | 67 h | 72 h |
| HARMONY | BBB | 21 h | 27 h |
| TAVI | AOA | 6 h | 27 h |
| TAVI | BBB | 21 h | 27 h |

## Main Logic Document

The detailed logic plan is located here:

```text
docs/logic_plan.md
