# 3-Phase Space Vector PWM (SVPWM) Controller (svpwm46)

## Overview
Space Vector Pulse Width Modulation (SVPWM) is an advanced algorithm essential for the efficient control of 3-Phase AC Induction and Brushless DC (BLDC) motors. By treating the three-phase inverter as a single 8-state space vector hexagon, SVPWM increases the maximum utilization of the DC bus voltage by 15.4% and significantly reduces Total Harmonic Distortion (THD).

###  Sub-Module Architecture & SoC Integration
This IP operates as a complete System-on-Chip (SoC) and is heavily modularized for eSim/Ngspice mixed-signal verification. It utilizes one external module and four internal sub-modules:

The External Reference Generator (`svpwm_ref_gen.v`): Acts as a Direct Digital Synthesis (DDS) engine. It queries a 64-point Q15 Sine Look-Up Table (LUT) to internally generate orthogonal stationary reference vectors (`v_alpha` and `v_beta`)[cite: 4023]. This bypasses computationally expensive Analog-to-Digital (ADC) bridging in eSim.
The Main Core (`svpwm.v`): This is the mathematical brain that receives the vectors and routes them through 4 internal sub-modules:
    1.  Sector ID (`svpwm_sector_id.v`): Maps the alpha/beta coordinates to one of six physical 60-degree sectors.
    2.  Dwell Time (`svpwm_dwell_time.v`): Calculates precise active (T1, T2) and zero-vector (T0) durations.
    3.  PWM Generator (`svpwm_pwm_gen.v`): Generates ideal, symmetrical center-aligned duty cycles.
    4.  Dead-Time Router (`svpwm_dead_time.v`): Enforces a strict 3-clock-cycle (600ns) hardware safety delay to physically prevent shoot-through cross-conduction in the H-Bridges.

## Pinout / I-O Ports (Main Core)
| Port Name  | Direction | Width  | Description                             |
|------------|-----------|--------|-----------------------------------------|
| clk        | Input     | 1-bit  | System clock (5 MHz base)               |
| rst_n      | Input     | 1-bit  | Active-low asynchronous reset           |
| v_alpha    | Input     | 16-bit | Stationary reference vector (from DDS)  |
| v_beta     | Input     | 16-bit | Orthogonal reference vector (from DDS)  |
| u_high/low | Output    | 1-bit  | Phase U High/Low MOSFET gate drives     |
| v_high/low | Output    | 1-bit  | Phase V High/Low MOSFET gate drives     |
| w_high/low | Output    | 1-bit  | Phase W High/Low MOSFET gate drives     |

## System Block Diagram
```
 [clk, rst_n]
      |
      V
 +-------------------------+     v_alpha   +---------------------------------------------------+
 | External DDS Engine     |     v_beta    | Internal svpwm.v Core                             |
 | (svpwm_ref_gen.v)       |==============>|                                                   |
 | - 64-Point Q15 LUT      |               |  [Sector ID] -> [Dwell Time] -> [PWM Generator]   |
 | - Phase Accumulator     |               |                                         |         |
 +-------------------------+               |                                         V         |
                                           |                                [Dead-Time Router] |
                                           |                                 |       |       | |
                                           +---------------------------------|-------|-------|-+
                                                                             V       V       V
                                                                  [Phase U, Phase V, Phase W Gates]
```

## Designer Contact
Designer: Sreekrishna K Sasidharan
Email: sreekrishnaksasidharan@gmail.com
Domain: Electric Vehicle (EV) Traction & Drone Propulsion