# REF102 — Precision +10V Voltage Reference

## Description
The REF102 is a precision +10V voltage reference featuring low
temperature drift and low power consumption. Its internal structure
consists of a buried Zener reference diode combined with an
operational amplifier buffer.

## Key Features
- Nominally rated +10 V reference output
- Input operating range starting above 11.4 V
- Low output dynamic impedance
- Standard 8-pin package layout

## Applications
- ADC reference voltage biasing
- Data acquisition system calibration
- Precision sensor bridge excitation

## Symbol
The component symbol created in eSim is designated as `ref_102d`.
Pin configuration includes input supply pins (Pins 1, 2, 3, 4, 7),
adjustment/feedback pins (Pins 5 and 8), and the output node (Pin 6).

## Internal Subcircuit Architecture
The internal model uses an LM321 operational amplifier subcircuit
(X1) combined with a Zener reference primitive (U2) and associated
biasing passives to model the closed-loop feedback path.

## Simulation Results

### Test 2: DC Line Regulation Sweep
The input voltage was swept from 0V to 35V. The output voltage
remained constant at 10.02V once the input exceeded the minimum
operating threshold (≈11.4V).

### Test 3: Load Regulation Dynamic Current Sweep
With a fixed 15V supply, the load current was swept. The output
voltage maintained 10.02V across the test current range.

## Dependencies
This subcircuit uses the LM321 operational amplifier subcircuit
(contributed separately). LM321 files are bundled in this folder
for simulation completeness.

