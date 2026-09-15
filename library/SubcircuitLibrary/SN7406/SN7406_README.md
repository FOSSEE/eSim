# SN7406 — Hex Inverter Buffer/Driver with High-Voltage Open-Collector Outputs

## Description
The SN7406 contains six independent inverting buffer/drivers with
open-collector outputs rated up to 30V and sinking currents up to
40mA per channel. This configuration allows level translation from
5V TTL logic to higher voltage levels without discrete interface
transistors.

## Key Features
- 6 open-collector inverting driver channels
- Output voltage rating up to 30V
- 40mA sinking current capacity per gate
- 5V TTL input compatibility

## Applications
- Voltage level shifting from 5V TTL to 15V/24V/30V buses
- Driving relays, lamps, and discrete power stages
- Wire-OR logic implementations

## Symbol
14-pin layout: Inputs (Pins 1, 3, 5, 9, 11, 13), Open Collector
outputs (Pins 2, 4, 6, 8, 10, 12), Ground (Pin 7), and VCC (Pin 14).

## Internal Subcircuit Architecture

### Single-Gate Primitive
Each inverter gate includes a TTL phase splitter (Q1, R1 = 6kΩ), a
driver stage (Q2, R4 = 1.4kΩ, R2 = 100Ω), active turn-off
transistors (Q3, Q4), and an uncommitted NPN output transistor (Q5)
without internal collector pull-up.

### Multi-Gate Package
Six single-gate subcircuits are instantiated in parallel, sharing
Pin 14 (VCC = 5V) and Pin 7 (GND).

## Test Circuit
Pin 1 receives a 0V ↔ 5V input pulse (V1), Pin 14 is connected to
VCC = 5V, and Output Pin 2 is connected through pull-up resistor
R1 = 1kΩ to external supply V2.

## Simulation Results

### Test 1: Standard 5V Logic Inversion
With V2 = 5V: when Vin = 0V, Q5 is cut off and Vout = 5.00V. When
Vin = 5V, Q5 saturates, bringing Vout to VOL ≈ 0.05V.

### Test 2: High-Voltage Level Shifting (30V Output Swing)
With V2 = 30V and VCC = 5V, a 0V ↔ 5V input pulse resulted in an
output swing from 0V to 30V, demonstrating level translation
without breakdown.

