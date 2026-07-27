# LM129 — Precision 6.9V Temperature-Compensated Monolithic Reference

## Description
The LM129 is a monolithic 6.9V shunt reference designed to maintain
temperature stability over operating currents from 0.6 mA to 15 mA.
The internal active circuit combines a breakdown Zener diode with
active transistor compensation.

## Key Features
- 6.90 V nominal shunt reference output
- Active temperature-compensation circuitry
- 0.6 mA to 15 mA operating current range
- Dynamic impedance below 1 Ω
- 2-terminal passive symbol representation

## Applications
- Precision ADC and DAC references
- Digital voltmeter voltage baselines
- Calibrated current sources

## Symbol
2-terminal symbol — Pin 1: Cathode, Pin 2: Anode.

## Internal Subcircuit Architecture
The subcircuit consists of eight transistors (Q1–Q8), an internal
Zener diode (U1), compensation capacitors (C1 = 15 pF, C2 = 30 pF),
and biasing resistors (R1–R7).

## Test Circuit
Cathode powered from DC source V1 through resistor R1 = 1 kΩ, with
the anode grounded.

## Simulation Results

### Test 1: Transient Response Under Constant Drive
With Vin = 12V DC, the output cathode voltage held steady at 6.90V
with no transient overshoot.

### Test 2: DC Line Sweep Regulation
Sweeping input voltage from 0V to 15V shows linear output tracking
below 6.9V, followed by clamping at 6.90V once breakdown occurs.

### Test 3: Load Regulation Current Sweep
Sweeping load current from 0A to 10mA shows regulation maintained at
6.90V up to 5 mA. Above 5 mA, the voltage drops due to current
starvation through the 1 kΩ series resistor.
