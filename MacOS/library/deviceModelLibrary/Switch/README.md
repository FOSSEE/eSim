# Voltage Controlled Switch

The Voltage Controlled Switch block represents the electrical characteristics of a
switch whose state is controlled by the voltage across the input ports (the controlling
voltage).

![sw_edited](https://user-images.githubusercontent.com/43288153/184137917-1e6d4b0e-42a9-4a87-80f1-9d98d2a6dc39.png)
fig: Voltage control switch

This block models either a variable-resistance or a short-transition switch. For
a variable-resistance switch, set the Switch model parameter to Smooth transition
between Von and Voff. For a short-transition switch, set Switch model to Abrupt
transition after delay.

When the controlling voltage is less than the Threshold voltage, VT parameter
value minus the Hysteresis voltage, VH parameter value, the switch is open and has
a resistance equal to the Off resistance, ROFF parameter value.
When the controlling voltage is greater than or less than the Threshold voltage,
VT parameter value by an amount less than or equal to the Hysteresis voltage, VH
parameter value, the voltage is in the crossover region and the state of the switch
remains unchanged

The schematic to test the proposed voltage controlled switch is shown below.
It is a simple circuit where a pulse source is connected to the switch followed by a
resistor.
When the switch is turned ON, then at the Vout the source voltage can be
obtained, however, the switch model is given some value for Ron meaning the amount
of ron will be offered by the switch when it is turned ON.
Similarly, when it is turned off then it will offer the resistance set in roff. 

```
.model switch1 sw( vt=0.05 vh=1 ron=1 roff=1e12 )
```
