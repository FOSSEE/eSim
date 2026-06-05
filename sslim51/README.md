# Soft-Start Inrush Limiter (sslim51)

## Overview
This IP core is a digital ramp generator designed to restrict the initial surge of current when powering up capacitive loads or high-torque electric motors. Uncontrolled inrush currents can severely degrade power supply components and induce mechanical stress. This IP gradually increases the duty cycle of the output drive signal over a configurable startup period, safely spinning up the motor load and keeping peak transient currents within operational limits.

## Pinout / I-O Ports
| Port Name       | Direction | Width | Description                           |
|-----------------|-----------|-------|---------------------------------------|
| clk             | Input     | 1-bit | System clock                          |
| rst_n           | Input     | 1-bit | Active-low asynchronous reset         |
| enable          | Input     | 1-bit | Hardware enable switch                |
| target_duty     | Input     | 8-bit | The final desired duty cycle          |
| ramp_rate_delay | Input     | 8-bit | Delay parameter to control ramp speed |
| safe_duty_out   | Output    | 8-bit | Safely ramping duty cycle output      |

## Block Diagram
```
                  +-------------------------+
 [target_duty] -->|                         |
                  |     Digital Ramp        |
 [ramp_rate] ---->|      Generator          |--> [safe_duty_out]
                  |     (Accumulator)       |
 [clk, rst, en] ->|                         |
                  +-------------------------+
```

## Designer Contact
Designer: Sreekrishna K Sasidharan
Email: sreekrishnaksasidharan@gmail.com
Domain: Heavy Power Electronics & Industrial Drives