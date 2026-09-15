# MC1413 — High-Voltage, High-Current Darlington Transistor Array

## Description
The MC1413 consists of seven NPN Darlington transistor channels with
open-collector outputs and common-cathode flyback suppression
diodes. Each channel includes a 2.7kΩ series input base resistor for
direct interfacing to 5V TTL logic.

## Key Features
- 7 independent open-collector sinking channels
- 500 mA continuous collector current capacity per channel
- 50 V collector-emitter breakdown rating
- 2.7kΩ base resistors for TTL logic levels

## Applications
- Solenoid and relay driving
- Stepper motor phase control
- LED matrix column driving

## Symbol
16 terminals: Inputs (Pins 1–7), Ground (Pins 8 and 9), Open
Collector outputs (Pins 10–16), and Common Cathode clamp (Pin 9).

## Internal Subcircuit Architecture

### Single-Channel Primitive
Each channel consists of a Darlington pair (Q1, Q2), an input
resistor (R1 = 2.7kΩ), base-emitter discharge resistors
(R2 = 7.2kΩ, R3 = 3kΩ), and a free-wheeling diode (D3).

### Multi-Channel Synthesis
Seven single-channel subcircuit blocks (U2–U8) are connected in
parallel, sharing ground plane VEE and common diode cathode node
VCC.

