# Micro-stepping Stepper Indexer (stepidx44)

## Overview
The Stepper Indexer IP core abstracts the complex phase sequencing required to drive bipolar stepper motors. It translates high-level "Step" and "Direction" digital pulses into proportional excitation signals. The internal logic utilizes a bidirectional phase accumulator synchronized to the step input clock. By querying internal Sine and Cosine Look-Up Tables (LUT), it generates exact microstepping duty cycles to provide precise open-loop position control and eliminate low-speed mechanical resonance.

### External IP Dependencies & eSim Compiler Caveats
This IP core does not contain its own PWM generators. To function correctly in a mixed-signal environment, it relies on two external Verilog modules:

1. H-Bridge Router (`hbridge_router.v`): A mandatory steering matrix included in this directory. It decodes the raw PWM signals and direction bits to correctly steer pulses to the High-Side (PMOS) and Low-Side (NMOS) gates of physical dual H-Bridges.
2. Advanced PWM Controller (`advpwm52` IP): The indexer requires two external instances of the Advanced PWM Controller (one for Coil A / Sine, one for Coil B / Cosine). You must link or import the `advanced_pwm.v` file from the `advpwm52` IP folder. 

Ngveri Dual-Instantiation Fix: Due to how the Ngveri compiler translates Verilog into XSPICE C++ models, instantiating the exact same module name twice can cause static memory contention and crash the simulation. To fix this, you must create a renamed clone of the PWM Verilog file (e.g., `advanced_pwm_B.v`) for the second instance. This forces the eSim compiler to treat them as two completely isolated memory models.

## Pinout / I-O Ports
| Port Name    | Direction | Width  | Description                    |
|--------------|-----------|--------|--------------------------------|
| clk, rst_n   | Input     | 1-bit  | System clock and reset         |
| step         | Input     | 1-bit  | Pulse input to advance phase   |
| coil_a_duty  | Output    | 16-bit | Coil A (Sine) PWM duty cycle   |
| coil_a_dir   | Output    | 1-bit  | Coil A H-Bridge polarity       |
| coil_b_duty  | Output    | 16-bit | Coil B (Cosine) PWM duty cycle |
| coil_b_dir   | Output    | 1-bit  | Coil B H-Bridge polarity       |

## System Block Diagram
```
 [step, dir] -->+-------------------+ 
                | Phase Accumulator | 
 [clk, rst] --->| & Sine/Cosine LUT | 
                +-------------------+ 
                  |               |
         (Sine Duty Cycle)   (Cosine Duty Cycle)
                  |               |
        +------------------+  +------------------+
        | External IP Core |  | External IP Core | <-- (Requires advpwm52 clone 
        | (advpwm52)       |  | (advpwm52_B)     |      for isolated eSim memory)
        +------------------+  +------------------+
                  |               |
                  V               V
                +-------------------+
                |  H-Bridge Router  | <-- (Included local IP: hbridge_router.v)
                |  Steering Matrix  |
                +-------------------+
                  |               |
             [Gate Drives]   [Gate Drives]
             (To Coil A)     (To Coil B)
```

## Designer Contact
Designer: Sreekrishna K Sasidharan
Email: sreekrishnaksasidharan@gmail.com
Domain: Precision Additive Manufacturing & Robotics