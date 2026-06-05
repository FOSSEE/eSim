# First-Order Digital Sigma-Delta Modulator (fsdmod31)

## Overview
This IP core is the backbone of high-resolution, low-frequency Analog-to-Digital and Digital-to-Analog Converter. The architecture oversamples the input signal and shapes the quantization noise, pushing it into higher frequency bands. By utilizing an internal accumulator and a 1-bit comparator in a feedback loop, it generates a high-frequency 1-bit Pulse-Density Modulated (PDM) bitstream that corresponds to varying DC input levels.

## Pinout / I-O Ports
| Port Name  | Direction | Width | Description                              |
|------------|-----------|-------|------------------------------------------|
| clk        | Input     | 1-bit | System clock                             |
| rst_n      | Input     | 1-bit | Active-low asynchronous reset            |
| digital_in | Input     | 8-bit | Digital value to be converted            |
| pdm_out    | Output    | 1-bit | Pulse-Density Modulated output bitstream |

## Block Diagram
```
                 +-----------------------+
                 |    Sigma-Delta Core   |
 [digital_in] -->|  [+] --> Accumulator  |--+--> [pdm_out] (MSB/Carry)
                 |   ^          |        |  |
                 |   |__________|        |  |
 [clk, rst_n] -->|                       |  |
                 +-----------------------+  |
                   (To Analog RC Filter) <--+
```

## Designer Contact
Designer: Sreekrishna K Sasidharan
Email: sreekrishnaksasidharan@gmail.com
Domain: Precision Metrology & High-Fidelity Audio