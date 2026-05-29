# Transmission Line

Transmision lines are used to carry Radio Frequency(RF) power from one place to
another, and to do this as efficiently as possible.
In this section the lossless and lossy transmission lines will be discussed along
with the simulation results.

## Lossless transmission line
A transmission line having no line resistance or no dielectric loss is said to be a
lossless transmission line. It means that the conductor would behave as a super-
conductor and dielectric would be made of perfect dielectric medium. In a lossless
transmission line, power sent from a generating point would be equal to power re-
ceived at the load end. There is no power dissipation in the line itself.


![tline](https://user-images.githubusercontent.com/43288153/184139198-e25e1e59-3b3f-415c-bf7d-99ebee4eb601.png)<br/>
 fig: Symbol of tline


**NOTE: We have to put one space between Z0=50 and Td=3ns**<br/>

 This can be done in the cir.out file after creating the circuit(s) and converting kiCad
to NgSpice.

## Single Lossy Transmission Line (SLTL)
An appreciable value of series resistance and shunt conductance make up a lossy
transmission line, which allows different frequencies to transmit at various speeds.
In contrast, on a lossless transmission line, wave propagation rates are constant
across all frequencies. As waves move towards the load end of the lossy transmission
line, distortion is caused by a change in speed.
The symbol for Single Lossy Transmission Lines(SLTL) is shown below-

![ymod](https://user-images.githubusercontent.com/43288153/184139539-ed4eac77-934a-423c-8f7b-2cba4daf42d1.png)<br/>
fig: Symbol of SLTL
