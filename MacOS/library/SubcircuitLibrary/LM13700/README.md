
# LM13700 Operational Transconductance Amplifier IC

The LM13700 is a current controlled, additional output buffer-equipped, differential input, transconductance amplifier with two channels. The two amplifiers operate independently, sharing a common supply. It makes use of linearizing diodes, using which higher input levels are permitted with less distortion. It has improved SNR also.


## Usage/Examples

VCA (Voltage Controlled Amplifier)

ACG (Automatic Gain Contol) Amplifier

VCO (Voltage controlled Oscillator)

PLL (Phase Locked loop)

Four Quadrant Multiplier

Amplitude Modulator

## Documentation

To know the details of LM13700 IC please refer to this link [LM13700_datasheet.](https://www.ti.com/lit/ds/symlink/lm13700.pdf)

## Comments/Notes

Please note this is a complete analog IC. Due to the improper modeling of Darlington pair at the output terminals, this IC is producing improper output. The shape of the output waveform is fine but the output is highly DC shifted & also it's peak to peak value is very low. Therefore it is suggested to use this IC only after replacing the subcircuit with a proper working Darlington pair.

## Contributor

Name: Arpit Sharma  
Email: arpitniraliya306@gmail.com  
Year: 2022  
Position: FOSSEE Summer Fellowship Intern 2022
