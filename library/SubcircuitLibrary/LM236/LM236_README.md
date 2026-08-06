# LM236-2.5 — Precision 2.5V Voltage Reference (Shunt Regulator Diode)

## Description
The LM236-2.5 is a 2.5V precision shunt reference diode. It operates
as a Zener-like breakdown reference with active transistor circuitry
to achieve low dynamic impedance.

## Key Features
- 2.50 V nominal shunt breakdown reference
- Low dynamic impedance across operating current range
- 3-terminal package with third pin for trim adjustment

## Applications
- Portable equipment voltage referencing
- 5V system bias networks
- Instrumentation calibration paths

## Symbol
3-terminal symbol labeled `LM236`.

## Internal Subcircuit Architecture
The internal transistor schematic incorporates 14 transistors,
comprising eSim NPN and eSim PNP primitives configured as
differential pairs, current mirrors, and biasing elements.

## Test Circuit
Cathode (Pin 1) driven through a 1kΩ current-limiting resistor (R1)
from a 10V supply (v1), with Pin 2 connected to ground.

## Simulation Results

### Test 1: Transient Analysis Under Fixed Supply
With Vin = 10V, the cathode voltage stabilized at 2.50V DC.

