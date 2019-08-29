# Code Documentation (GHDL Side)

This documentation will help you to know about the code written for communication between server and Digital logic written in VHDL

## Files generated automatically for GHDL side

* modelname_tb.vhdl
* Note: where modelname will be the name of your model

## modelname_tb.vhdl  

* This is a testbench created to send and receive values from server and gives the input values to the digital design.
* It uses VHPI library of VHDL, by including this library we can use functions written in C program, in VHDL.
* In this test bench there are two processes used.
* First process is used to initialize, listen server and sending the output to server.
* Second process is used to giving inputs from server to digital design and taking the values to send through the server.

### C functions used in modelname_tb.vhdl
#### Vhpi_Initialize
* This function is used to create the port and initialize the server.  

#### Vhpi_Listen
* This function is used to start communication between client and server.

#### Vhpi_Send
* This function is used to send the values to client.

#### Pack_String_To_Vhpi_String
* As we are sending values along with there variable name, we are using this function which convert the vhdl string to VHPI string.

#### Vhpi_Get_Port_Value
* This function takes input values from server, when Vhpi_Listen called, and give it to digital design.

#### Vhpi_Set_Port_Value
* This function is used to takes output values from digital design and send it through server when Vhpi_Send called.
