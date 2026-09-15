# TL317 — 3-Terminal Adjustable Positive Voltage Regulator

## Description
The TL317 is an adjustable 3-terminal positive voltage regulator
rated to supply up to 100 mA. The internal control loop maintains a
nominal 1.25V reference between the Output and Adjustment terminals.

## Key Features
- Adjustable output voltage via external resistor ratio
- 100 mA continuous output current rating
- Internal current-limiting and thermal protection primitives
- Standard 3-terminal package layout

## Applications
- Local on-card regulation
- Programmable power supplies
- Constant current regulators

## Symbol
The eSim symbol is labeled `TL317`. Pin 1: Input, Pin 2: Adjustment
(Adj), Pin 3: Output.

## Internal Subcircuit Architecture
The subcircuit combines an LM321 operational amplifier primitive
(X1), a 1.25V DC reference source (v2), a 50µA bias current source
(I1), and an NPN Darlington output pair (Q1, Q2).

## Test Circuit
Powered by a 15V DC source (v1). Resistor R1 = 240Ω is connected
between Output (Pin 3) and Adjustment (Pin 2), while R2 = 720Ω is
placed between Adjustment (Pin 2) and Ground. Load resistor
R3 = 1kΩ is connected to the output.

The theoretical output voltage is calculated as:

    Vout = Vref × (1 + R2/R1) + Iadj × R2

Ignoring Iadj ≈ 50µA for first-order evaluation:

    Vout = 1.25V × (1 + 720Ω/240Ω) = 1.25V × 4 = 5.00V

## Simulation Results

### Test 1: Transient Analysis Under Fixed Supply
With Vin = 15V, the output voltage settled at 5.00V DC without
overshoot or visible ripple, matching the theoretical calculated
value.

### Test 2: Supply Voltage Line Sweep Regulation
The input supply was swept from 0V to 20V. The output voltage
tracks the input until reaching dropout headroom (≈6.5V input),
after which it holds steady at 5.00V.

## Dependencies
This subcircuit uses the LM321 operational amplifier subcircuit
(contributed separately). LM321 files are bundled in this folder
for simulation completeness.

## Contact
(optional)