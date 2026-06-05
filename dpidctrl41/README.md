# Digital PID Controller (dpidctrl41)

## Overview
The discrete-time digital PID IP core is a foundational algorithm for closed-loop dynamic systems. It continuously samples a digital error signal, applying proportional, integral, and derivative gains via a purely digital fixed-point arithmetic engine. The internal 32-bit integral accumulator safely accumulates while strictly obeying anti-windup bounds, preventing runaway during massive mechanical or thermal plant lags. The output is saturated to a 16-bit limit to prevent bit-rollover inversions.

## Pinout / I-O Ports (Core Interface)
| Port Name     | Direction | Width  | Description                       |
|---------------|-----------|--------|-----------------------------------|
| clk, rst_n    | Input     | 1-bit  | System clock and active-low reset |
| enable        | Input     | 1-bit  | Active-high compute enable        |    
| kp, ki, kd    | Input     | 8-bit  | Fractional tuning parameters      |
| setpoint      | Input     | 16-bit | Target reference value            |
| feedback      | Input     | 16-bit | Process variable measurement      |
| control_out   | Output    | 16-bit | Corrective control output         |

## Implementation Notes & Best Practices

### Creating Project-Specific Wrappers (eSim Mitigation)
The provided `dpidctrl41.v` is the raw, highly parameterized core. Exposing all 75 pins (including full 16-bit and 32-bit buses) directly to the eSim `adc_bridge` parser can cause severe memory limits and GUI crashes during SPICE translation. 

Best Practice: When integrating this IP into a larger mixed-signal project (such as a thermal control system), it is highly recommended to write a custom "Wrapper" Verilog module. This wrapper should instantiate the core, hardcode the `kp`, `ki`, and `kd` values specific to your project, and truncate the external I/O to purely 8-bit MSB buses. This drastically reduces the pin count and guarantees a stable Ngspice simulation.

### Troubleshooting: Zero/Dead Output at Low PID Values
This IP utilizes a fractional scaling pipeline to avoid massive floating-point ALUs. The raw summation of the P, I, and D terms (`pid_total`) is bit-shifted to the right by a `SHIFT_VAL` of 8 (effectively dividing the result by 256) before reaching the output.

If you tune your kp, ki, and kd values too low, and the system error is small, the raw `pid_total` may evaluate to a number less than 256. Due to digital integer truncation, right-shifting a number smaller than 256 by 8 bits results in exactly `0`. 
The Fix: If your controller output is inexplicably dead, your fractional multipliers are too small. You must either scale up your input variables or modify the `SHIFT_VAL` parameter in the Verilog source to suit a smaller fractional range.

## Block Diagram
```
                  [ Fractional Tuning (Kp, Ki, Kd) ]
                                  |
 [setpoint] -->(+)-->[ Error ]--+--> [ Kp * Error ] ---------+
               |               |                            |
 [feedback] --->(-)             +--> [ Ki * Sum(Error) ] --->(+)--> [control_out]
                               |      (Anti-Windup)         |   (Shifted & Saturated)
                               +--> [ Kd * d(Error)/dt ] ---+
```

## Designer Contact
Designer: Sreekrishna K Sasidharan
Email: sreekrishnaksasidharan@gmail.com
Domain: Autonomous Flight & Process Control