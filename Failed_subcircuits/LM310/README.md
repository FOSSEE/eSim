
# LM310 Voltage Follower IC

The LM310 is a Voltage Follwer IC obtained by internally connecting an operational amplifier with unity gain as in a non inverting amplifier.


## Usage/Examples

Low Pass Active Filter

High Pass Active Filter

BandPass/Notch Filter

Simulated Inductor

Sample Holds


## Documentation

To know the details of LM310 IC please refer to this link [LM310_datasheet.](https://www.farnell.com/datasheets/105178.pdf)

## Error Observed

According to the Frequency response,the HPF using LM310 as mentioned in its datasheet is working fine. But the LPF as mentioned in the datasheet is behaving as HPF with the expected cutoff frequency. If I exchange the capacitors with the resistors, then I am obtaining the desired LPF response, but then I have changed the LPF circuit which is mentioned in the datasheet.  I don't know if its an error in this circuit itself or possibly an error in the test circuit given in datasheet.

## Possible Solution

The designer is suggested to check and test this circuit with different model files and verify the output. Also the designer may re-verify the subcircuit and the test circuits of the IC in accordance with the datasheet.

## Contributor

Name: Arpit Sharma  
Email: arpitniraliya306@gmail.com  
Year: 2022  
Position: FOSSEE Summer Fellowship Intern 2022