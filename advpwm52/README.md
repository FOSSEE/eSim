# Advanced PWM Controller with Dead-Time (advpwm52)

## Overview
The Advanced PWM IP core provides a highly configurable square wave output used to control average power delivery to inductive loads. It utilizes a free-running N-bit counter and a digital comparator to determine logic states. Beyond basic PWM, this module is enhanced with asynchronous dead-time insertion logic to prevent shoot-through in H-Bridges, and a hardware trip-zone fault input for instantaneous shutdown.

## Pinout / I-O Ports
| Port Name   | Direction | Width  | Description                   |
|-------------|-----------|--------|-------------------------------|
| clk, rst_n  | Input     | 1-bit  | System clock and reset        |
| duty_cycle  | Input     | 16-bit | Desired duty cycle threshold  |
| period      | Input     | 16-bit | PWM frequency max count       |
| dead_time   | Input     | 8-bit  | Shoot-through delay parameter |
| pwm_h       | Output    | 1-bit  | High-side gate drive          |
| pwm_l       | Output    | 1-bit  | Low-side gate drive           |

## Block Diagram
```
 [duty, period] ->+-------------------+    +------------------+--> [pwm_h]
                  | Time-Base Counter |--->| Dead-Time &      |
 [dead_time] ---->| & Comparator      |    | Fault Trip Logic |--> [pwm_l]
                  +-------------------+    +------------------+
```
## Designer Contact
Designer: Sreekrishna K Sasidharan
Email: sreekrishnaksasidharan@gmail.com
Domain: Switch-Mode Power Supplies (SMPS) & Lightings