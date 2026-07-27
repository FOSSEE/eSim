# ULN2004 — High-Voltage, High-Current Darlington Array (CMOS-Compatible)

## Description
The ULN2004 is a 7-channel Darlington driver array designed for
higher-voltage control logic (6–15V CMOS). Each channel incorporates
a 10.5kΩ input resistor to reduce input base loading.

## Key Features
- 7 open-collector Darlington output stages
- 10.5kΩ input base resistors for CMOS compatibility
- Integral flyback clamp diodes
- 500 mA rating per channel

## Applications
- High-voltage CMOS logic load driving
- Relay and lamp matrix activation
- Industrial control interfaces

## Symbol
Inputs (Pins 1–7), Ground (Pin 8), Protection Cathodes (Pin 9), and
Collector Outputs (Pins 10–16).

## Internal Subcircuit Architecture

### Single-Channel Primitive
Each channel primitive uses R1 = 10.5kΩ, R2 = 7.2kΩ, and
R3 = 3.0kΩ driving two NPN transistors (Q1, Q2).

### Multi-Channel Synthesis
Seven single-channel primitives are combined into the final array
block.

## Simulation Results

### Test 1: Transient Analysis Under Pulsed CMOS Input
The input pulse (0V ↔ 5V) was applied with a 12V output pull-up
rail. The output transitioned cleanly between 12V (off) and 1.35V
(saturated on).

