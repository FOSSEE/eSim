# SN75468 — High-Voltage, High-Current Darlington Array

## Description
The SN75468 is a high-voltage 7-channel Darlington driver array
rated for collector breakdown voltages up to 100V per channel,
featuring 2.7kΩ input resistors for direct 3.3V/5V logic control.

## Key Features
- 100 V output breakdown voltage rating
- 500 mA current handling per channel
- Integrated flyback clamp diodes
- 2.7kΩ series base resistors

## Applications
- High-voltage solenoid and contactor switching
- High-voltage display driving
- Industrial logic interface buffering

## Symbol
Packaged 16-pin symbol.

## Internal Subcircuit Architecture

### Single-Channel Primitive
Each channel primitive contains the Darlington pair (Q1, Q2), base
resistors (R1 = 2.7kΩ, R2 = 7.2kΩ, R3 = 3kΩ), and protection
diodes.

### Multi-Channel Synthesis
Seven single-channel primitives combined in a parallel subcircuit
instantiation.

## Test Circuit
A 0V ↔ 5V input pulse (v1) is applied, with the output pulled up
through R1 = 1kΩ to a 50V supply rail (v3). Common clamp Pin 7 is
tied to a 50V DC source (v2).

## Simulation Results

### Test 1: Transient Analysis Under High-Voltage Loading
With a 50V pull-up rail, the output switched between 50V (off) and
0.8V (on).

### Test 2: Voltage Transfer Characteristic (VTC) Threshold Profile
DC input sweep from 0V to 10V confirmed turn-on at 1.4V–1.5V under
50V loading.

### Test 3: Load Regulation – Sinking Load Current Sweep
Current sweep up to 1.0A showed saturation voltage rising from
0.7V to 1.11V.
