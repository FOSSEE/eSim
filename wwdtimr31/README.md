# Windowed Watchdog Timer (wwdtimr31)

## Overview
Designed for high-reliability and mission-critical environments, the Windowed Watchdog Timer (WWDT) offers superior fault detection. It requires the host microcontroller to clear the timer strictly within a specific time window. The IP core tracks internal counters to define upper and lower temporal boundaries; if the "feed" signal is received before the window opens (early clear) or after it closes (late clear), a system reset interrupt is instantly triggered.

## Pinout / I-O Ports
| Port Name   | Direction | Width | Description                   |
|-------------|-----------|-------|-------------------------------|
| clk, rst_n  | Input     | 1-bit | System clock and reset        |
| feed        | Input     | 1-bit | The timer clear/feed signal   |
| reset_out   | Output    | 1-bit | System reset interrupt signal |

## Block Diagram
```
             +-----------------------+
             |   Time-Base Counter   |
 [clk] ----->|   (Free Running)      |----+
             +-----------------------+    |    +------------------+
                                          +--->| Window Bounds    |--> [reset_out]
 [feed] ------------------------------------->| (Early/Late Check)|
                                               +------------------+
```
## Designer Contact
Designer: Sreekrishna K Sasidharan
Email: sreekrishnaksasidharan@gmail.com
Domain: Mission-Critical Aerospace & Automotive Safety