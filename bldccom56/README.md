# BLDC Closed-Loop Commutator (bldccom56)

## Overview
This IP core provides continuous rotor position feedback to electronically commutate the stator phases of Brushless DC (BLDC) motors. It decodes digital signals from three 120-degree electrically spaced Hall-effect sensors and utilizes a lookup table to generate the standard 6-step commutation sequence. The logic drives three high-side and three low-side inverter switches and includes dead-time insertion to prevent shoot-through faults.

## Pinout / I-O Ports
| Port Name  | Direction | Width | Description                        |
|------------|-----------|-------|------------------------------------|
| clk        | Input     | 1-bit | System clock                       |
| rst_n      | Input     | 1-bit | Active-low asynchronous reset      |
| hall_a/b/c | Input     | 1-bit | 120-degree Hall sensor inputs (x3) |
| gate_u_h/l | Output    | 1-bit | Phase U High/Low drives            |
| gate_v_h/l | Output    | 1-bit | Phase V High/Low drives            |
| gate_w_h/l | Output    | 1-bit | Phase W High/Low drives            |

## Block Diagram
```
 [hall_a] -->+-------------------+    +-----------------+--> [Phase U H/L]
 [hall_b] -->| Hall State Decoder|--->| 6-Step LUT &    |--> [Phase V H/L]
 [hall_c] -->| (120-deg spaced)  |    | Dead-Time Logic |--> [Phase W H/L]
             +-------------------+    +-----------------+
```

## Designer Contact
Designer: Sreekrishna K Sasidharan
Email: sreekrishnaksasidharan@gmail.com
Domain: Consumer Power Tools & E-Mobility