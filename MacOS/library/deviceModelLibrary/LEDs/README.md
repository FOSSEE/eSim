# Light Emitting Diodes (LEDs)

A light-emitting diode (LED) is a semiconductor device that emits light when an electric current flows through it. 
When current passes through an LED, the electrons recombine with holes emitting light in the process.
Just like diode, the process to model blue led is also the same, it is to be noted here
that the forward voltage of the LEDs are higher than the normal diode.
# Red LED
```
.MODEL eSim_RedLED D( Is=1e-10 Rs=0.1 N=4.09 tt=4.0e-6 Cjo=3e-12 M=0.5 Vj=0.7
Bv=5 Ibv=10e-6 Fc=0.5 Isr=0.0 Nr=2.0 Kf=0.0 Af=1.0 Ffe=1.0 Xti=3.0 Eg=1.11
Tbv=0.0 Trs=0.0 )
```
**NOTE: The name of the above LED is set as eSim_Red_LED the same name of the LED must be given to the subcircuit while creating the symbol for LED. While the D is the designator for the diode.**

# Blue LED

```
.MODEL eSim_BlueLED D( Is=1e-10 Rs=0.1 N=6.68 tt=4e-6 Cjo=3e-12 M=0.5 Vj=0.7 Bv=5
Ibv=10e-6 Fc=0.5 Cp=0.0e-12 Isr=0.0 Nr=2.0 Temp=26.85 Kf=0.0 Af=1.0 Ffe=1.0
Xti=3.0 Eg=1.11 Tbv=0.0 Trs=0.0 Ttt1=0.0 Ttt2=0.0 Tm1=0.0 Tm2=0.0 Tnom=26.85
Area=1.0 )
```
