# Integration of IHP OpenPDK with eSim

## Overview

This contribution demonstrates the integration of the IHP OpenPDK with eSim
to enable CMOS circuit design and simulation using open-source EDA tools.

## Objective

- Integrate IHP OpenPDK MOSFET SPICE models with eSim
- Design and simulate a CMOS inverter
- Perform DC sweep and transient analysis
- Validate inverter switching behavior

## Tools Used

- eSim (KiCad + NgSpice)
- IHP OpenPDK
- NgSpice

## Circuit Implemented

- CMOS Inverter using IHP NMOS and PMOS models
- Supply voltage: 1.8V

## Simulations Performed

### Transient Analysis

- `.tran 0.1ns 20ns`
- Verified correct logical inversion

### DC Sweep Analysis

- `.dc VIN 0 1.8 0.01`
- Verified voltage transfer characteristics

## Results

- Correct inverter operation observed
- Threshold voltage near mid-supply
- Stable transient and DC behavior

## Notes

- Absolute paths were used for SPICE model inclusion
- Convergence issues resolved by reducing timestep

## Report and Demo

The detailed report and demonstration video are provided via links
in the corresponding GitHub Pull Request.
